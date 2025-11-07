import os
import sys
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, List, Optional
import re

# gspread auth like in google_doc_reader
import gspread
from google.oauth2.service_account import Credentials

DOCX_RELATIVE_PATH = os.path.join(
    os.path.dirname(__file__),
    "1_Inputs",
    "ITSM-S-1002 Datensicherheit v0.5_Cleaned Version_HEAD.docx",
)

# WordprocessingML namespaces
NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    # Replies and extended attributes may appear under w15 in newer docs
    "w15": "http://schemas.microsoft.com/office/word/2012/wordml",
    # Older paraId attributes may appear under w14 on paragraphs
    "w14": "http://schemas.microsoft.com/office/word/2010/wordml",
}

def _get_text_from_paragraphs(element: ET.Element) -> str:
    """Concatenate all text within comment paragraphs."""
    texts: List[str] = []
    for p in element.findall(".//w:p", NS):
        # collect texts inside runs
        parts: List[str] = []
        for t in p.findall(".//w:t", NS):
            if t.text:
                parts.append(t.text)
        # Handle soft line breaks within a paragraph (w:br) as newlines
        br_count = len(p.findall(".//w:br", NS))
        para_text = "".join(parts)
        if br_count > 0:
            # This is a conservative approach; without exact position of br, append newlines
            para_text = para_text + ("\n" * br_count)
        if para_text:
            texts.append(para_text)
    return "\n".join(texts).strip()

def _parse_datetime(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    try:
        # Word usually stores ISO-like timestamps
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return dt.isoformat()
    except Exception:
        return value  # fallback to raw if unknown format

class Comment:
    def __init__(
        self,
        cid: int,
        text: str,
        author: Optional[str],
        date_str: Optional[str],
        parent_id: Optional[int],
    ):
        self.id = cid
        self.text = text
        self.author = author
        self.date_str = date_str
        self.parent_id = parent_id
        self.replies: List["Comment"] = []
        # Anchor paragraph text for the comment's referenced range
        self.anchor_paragraph_text: Optional[str] = None
        self.anchor_paragraph_text_marked: Optional[str] = None
        # Nearest heading found when traversing backwards from comment
        self.nearest_heading: Optional[str] = None
        # Requirement ID (DSSxxx format) found between comment and heading
        self.requirement_ID: Optional[str] = None

    def __repr__(self) -> str:
        return f"Comment(id={self.id}, author={self.author}, parent_id={self.parent_id})"

class DiscussionReply(Comment):
    """A reply that belongs to a discussion (nested comment via parentId)."""
    pass

def extract_comments_threads(docx_path: str) -> List[Comment]:
    if not os.path.exists(docx_path):
        raise FileNotFoundError(f"File not found: {docx_path}")

    with zipfile.ZipFile(docx_path, "r") as zf:
        # comments are stored in word/comments.xml
        try:
            with zf.open("word/comments.xml") as f:
                tree = ET.parse(f)
                root = tree.getroot()
        except KeyError:
            # No comments in the document
            return []

    comments_nodes = root.findall("w:comment", NS)
    comments: List[Comment] = []
    by_id: Dict[int, Comment] = {}
    id_to_para: Dict[int, Optional[str]] = {}

    for node in comments_nodes:
        # id
        id_attr = node.get(f"{{{NS['w']}}}id")
        if id_attr is None:
            # try w15:id if ever present (very unlikely)
            id_attr = node.get(f"{{{NS['w15']}}}id")
        if id_attr is None:
            # skip malformed entries
            continue

        try:
            cid = int(id_attr)
        except ValueError:
            # Some rare docs could have non-int ids; skip safely
            continue

        # parentId for replies (may be w or w15)
        parent_attr = node.get(f"{{{NS['w']}}}parentId")
        if parent_attr is None:
            parent_attr = node.get(f"{{{NS['w15']}}}parentId")
        parent_id = None
        if parent_attr is not None:
            try:
                parent_id = int(parent_attr)
            except ValueError:
                parent_id = None

        author = node.get(f"{{{NS['w']}}}author")
        if author is None:
            # sometimes stored as w:initials or other fields; keep None if not present
            author = node.get(f"{{{NS['w']}}}initials")

        date_raw = node.get(f"{{{NS['w']}}}date")
        date_str = _parse_datetime(date_raw)

        # capture paraId from the first paragraph inside the comment (w14/w15)
        first_p = node.find(".//w:p", NS)
        para_id = None
        if first_p is not None:
            para_id = first_p.get(f"{{{NS['w15']}}}paraId") or first_p.get(f"{{{NS['w14']}}}paraId")

        text = _get_text_from_paragraphs(node)

        # Use DiscussionReply subclass for comments that are replies (have parentId)
        comment_cls = DiscussionReply if parent_id is not None else Comment
        c = comment_cls(
            cid=cid,
            text=text,
            author=author,
            date_str=date_str,
            parent_id=parent_id,
        )
        comments.append(c)
        by_id[cid] = c
        id_to_para[cid] = para_id

    # Build threads: attach replies to their parent
    top_level: List[Comment] = []
    for c in comments:
        if c.parent_id is None:
            top_level.append(c)
        else:
            parent = by_id.get(c.parent_id)
            if parent is not None:
                parent.replies.append(c)
            else:
                # Orphan reply — treat as top-level to avoid losing it
                top_level.append(c)

    # Fallback threading using commentsExtended.xml (w15:paraIdParent) if parentId missing
    try:
        with zipfile.ZipFile(docx_path, "r") as zf:
            with zf.open("word/commentsExtended.xml") as f:
                ext_tree = ET.parse(f)
                ext_root = ext_tree.getroot()
                # Build paraId -> commentId map
                para_to_id: Dict[str, int] = {}
                for cid, pid in id_to_para.items():
                    if pid:
                        para_to_id[pid] = cid
                # Iterate extended comment entries
                for ex in ext_root.findall("w15:commentEx", NS):
                    child_para = ex.get(f"{{{NS['w15']}}}paraId")
                    parent_para = ex.get(f"{{{NS['w15']}}}paraIdParent")
                    if not child_para or not parent_para:
                        continue
                    child_id = para_to_id.get(child_para)
                    parent_id_from_para = para_to_id.get(parent_para)
                    if child_id is None or parent_id_from_para is None:
                        continue
                    child_comment = by_id.get(child_id)
                    parent_comment = by_id.get(parent_id_from_para)
                    if not child_comment or not parent_comment:
                        continue
                    # If not already threaded via w:parentId, attach now
                    if child_comment.parent_id is None:
                        child_comment.parent_id = parent_comment.id
                        parent_comment.replies.append(child_comment)
                        if child_comment in top_level:
                            top_level.remove(child_comment)
    except Exception:
        # If the extended file doesn't exist or can't be parsed, ignore silently
        pass

    # Build map of comment id -> (anchor paragraph text, marked text) from document.xml
    try:
        with zipfile.ZipFile(docx_path, "r") as zf:
            with zf.open("word/document.xml") as f:
                doc_tree = ET.parse(f)
                doc_root = doc_tree.getroot()

        def render_paragraph_with_marker(p_elem: ET.Element, target_id: int) -> (str, str):
            plain_parts: List[str] = []
            marked_parts: List[str] = []
            in_range = False
            inserted = False
            target = str(target_id)
            for elem in p_elem.iter():
                tag = elem.tag.split("}")[-1]
                if tag == "commentRangeStart" and elem.get(f"{{{NS['w']}}}id") == target:
                    in_range = True
                    continue
                if tag == "commentRangeEnd" and elem.get(f"{{{NS['w']}}}id") == target:
                    in_range = False
                    continue
                if tag == "t":
                    txt = elem.text or ""
                    plain_parts.append(txt)
                    if in_range and not inserted:
                        marked_parts.append("[1]")
                        inserted = True
                    marked_parts.append(txt)
                elif tag == "br":
                    plain_parts.append("\n")
                    marked_parts.append("\n")
            return ("".join(plain_parts).strip(), "".join(marked_parts).strip())

        # Locate all paragraphs that contain comment range starts and map id -> paragraph
        anchor_map: Dict[int, tuple] = {}
        for p in doc_root.findall('.//w:p', NS):
            # Find all commentRangeStart under this paragraph
            for crs in p.findall('.//w:commentRangeStart', NS):
                id_attr = crs.get(f"{{{NS['w']}}}id")
                if not id_attr:
                    continue
                try:
                    cid_int = int(id_attr)
                except ValueError:
                    continue
                # Only compute once per id
                if cid_int in anchor_map:
                    continue
                plain, marked = render_paragraph_with_marker(p, cid_int)
                anchor_map[cid_int] = (plain, marked)

        # Attach anchors to comments (top-level and replies independently)
        for c in comments:
            if c.id in anchor_map:
                c.anchor_paragraph_text, c.anchor_paragraph_text_marked = anchor_map[c.id]

        # Build list of all paragraphs in document order with heading info
        def extract_paragraph_text(p_elem: ET.Element) -> str:
            parts: List[str] = []
            for t in p_elem.findall(".//w:t", NS):
                if t.text:
                    parts.append(t.text)
            return "".join(parts).strip()

        def is_heading(p_elem: ET.Element) -> tuple:
            """Check if paragraph is a heading. Returns (is_heading, level, text)."""
            p_pr = p_elem.find("w:pPr", NS)
            if p_pr is None:
                return (False, 0, "")
            p_style = p_pr.find("w:pStyle", NS)
            if p_style is None:
                return (False, 0, "")
            style_val = p_style.get(f"{{{NS['w']}}}val", "")
            level = 0
            if style_val.startswith("Heading"):
                try:
                    level = int(style_val.replace("Heading", ""))
                except ValueError:
                    pass
            if level in (1, 2, 3):
                text = extract_paragraph_text(p_elem)
                return (True, level, text)
            return (False, 0, "")

        # Build ordered list of paragraphs with their positions and heading info
        all_paragraphs: List[tuple[ET.Element, int, bool, int, str]] = []
        para_index = 0
        for p in doc_root.findall('.//w:p', NS):
            is_h, h_level, h_text = is_heading(p)
            all_paragraphs.append((p, para_index, is_h, h_level, h_text))
            para_index += 1

        # Map comment ID to paragraph index (where commentRangeStart appears)
        comment_to_para_index: Dict[int, int] = {}
        for idx, (p, _, _, _, _) in enumerate(all_paragraphs):
            for crs in p.findall('.//w:commentRangeStart', NS):
                id_attr = crs.get(f"{{{NS['w']}}}id")
                if not id_attr:
                    continue
                try:
                    cid_int = int(id_attr)
                    if cid_int not in comment_to_para_index:
                        comment_to_para_index[cid_int] = idx
                except ValueError:
                    continue

        # For each comment, traverse backwards to find nearest heading and DSSxxx
        dss_pattern = re.compile(r'DSS\d{1,3}', re.IGNORECASE)
        for c in comments:
            if c.id not in comment_to_para_index:
                continue
            comment_para_idx = comment_to_para_index[c.id]
            nearest_heading: Optional[tuple[int, int, str]] = None  # (index, level, text)
            requirement_id: Optional[str] = None

            # Traverse backwards from comment paragraph
            for i in range(comment_para_idx, -1, -1):
                p_elem, p_idx, is_h, h_level, h_text = all_paragraphs[i]
                distance = comment_para_idx - p_idx
                
                if is_h and h_level in (1, 2, 3):
                    # Found a heading - check if it's closer than previous
                    if nearest_heading is None:
                        nearest_heading = (p_idx, h_level, h_text)
                    else:
                        prev_distance = comment_para_idx - nearest_heading[0]
                        # If closer, or same distance but higher level (h1 > h2 > h3)
                        if distance < prev_distance or (distance == prev_distance and h_level < nearest_heading[1]):
                            nearest_heading = (p_idx, h_level, h_text)
                
                # Search for DSSxxx pattern in this paragraph's text (only between comment and heading)
                if requirement_id is None:
                    para_text = extract_paragraph_text(p_elem)
                    match = dss_pattern.search(para_text)
                    if match:
                        requirement_id = match.group(0).upper()

            if nearest_heading:
                c.nearest_heading = nearest_heading[2]
            if requirement_id:
                c.requirement_ID = requirement_id

    except Exception:
        # If document.xml isn't readable, skip anchors silently
        pass

    # Preserve original order as in comments.xml for top-level threads
    id_order = [c.id for c in comments if c.parent_id is None]
    top_level.sort(key=lambda c: id_order.index(c.id) if c.id in id_order else 10**9)

    return top_level

def _print_replies_recursive(comment: Comment, depth: int = 1) -> None:
    if not comment.replies:
        return
    # Label for nested subconversations
    indent = "  " * depth
    print(f"\n{indent}Subconversation (level {depth}):")
    for idx, r in enumerate(comment.replies, start=1):
        r_author = r.author or "Unknown"
        r_date = r.date_str or "Unknown date"
        label = "Reply" if isinstance(r, DiscussionReply) else "Comment"
        print(f"{indent}  [{idx}] {label} ID {r.id}")
        print(f"{indent}      Author: {r_author}")
        print(f"{indent}      Date:   {r_date}")
        print(f"{indent}      Text:")
        body = r.text if r.text else "(no text)"
        for line in (body.splitlines() or ["(no text)"]):
            print(f"{indent}        {line}")
        # Recurse for deeper nested replies
        _print_replies_recursive(r, depth + 1)

def print_first_n_threads(threads: List[Comment], n: int = 5) -> None:
    count = 0
    for thread in threads:
        if count >= n:
            break
        print("=" * 80)
        header = f"Thread #{count + 1} - Comment ID {thread.id}"
        print(header)
        print("-" * len(header))
        author = thread.author or "Unknown"
        date_display = thread.date_str or "Unknown date"
        print(f"Author: {author}")
        print(f"Date:   {date_display}")
        print("Comment:")
        print(thread.text if thread.text else "(no text)")

        if thread.anchor_paragraph_text_marked:
            print("\nAnchor paragraph (with marker):")
            for line in thread.anchor_paragraph_text_marked.splitlines():
                print(f"  {line}")

        # Print replies recursively as subconversations
        _print_replies_recursive(thread, depth=1)
        count += 1

    if count == 0:
        print("No comments found.")
    else:
        print("=" * 80)

def _extract_sheet_id(url: str) -> Optional[str]:
    pattern = r'/spreadsheets/d/([a-zA-Z0-9\-_]+)'
    m = re.search(pattern, url)
    return m.group(1) if m else None

def _setup_gspread_client() -> Optional[gspread.Client]:
    try:
        credentials_path = os.getenv('GOOGLE_CREDENTIALS_PATH')
        if not credentials_path:
            possible_paths = [
                '/Users/vasilenkoilya/Documents/7 GitHub Cursor/cms-assistant/.vscode/client_secret_1049835516666-5v9s988evv40904gof6p0i7l93f57go7.apps.googleusercontent.com.json',
                'credentials.json',
                'client_secret.json',
                os.path.expanduser('~/.config/gspread/credentials.json'),
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    credentials_path = path
                    break

        if credentials_path and os.path.exists(credentials_path):
            try:
                authorized_user_paths = [
                    '.vscode/authorized_user.json',
                    'authorized_user.json',
                    os.path.expanduser('~/.config/gspread/authorized_user.json'),
                ]
                authorized_user_path = None
                for path in authorized_user_paths:
                    if os.path.exists(path):
                        authorized_user_path = path
                        break
                return gspread.oauth(
                    credentials_filename=credentials_path,
                    authorized_user_filename=authorized_user_path,
                )
            except Exception:
                # Fallback to service account
                try:
                    scope = [
                        'https://spreadsheets.google.com/feeds',
                        'https://www.googleapis.com/auth/drive',
                    ]
                    creds = Credentials.from_service_account_file(credentials_path, scopes=scope)
                    return gspread.authorize(creds)
                except Exception:
                    pass

        # Default oauth (interactive cached)
        try:
            return gspread.oauth()
        except Exception:
            return None
    except Exception:
        return None

def _format_thread_text(thread: Comment) -> str:
    lines: List[str] = []
    # First line: [1] Author: Comment
    author = thread.author or 'Unknown'
    body = thread.text or ''
    lines.append(f"[1] {author}: {body}")
    # Replies lines
    def walk(c: Comment):
        for r in c.replies:
            r_author = r.author or 'Unknown'
            r_body = r.text or ''
            lines.append(f"{r_author}: {r_body}")
            walk(r)
    walk(thread)
    return "\n".join(lines)

def export_threads_to_gsheet(threads: List[Comment], spreadsheet_url: str) -> bool:
    client = _setup_gspread_client()
    if not client:
        print("Warning: Could not authenticate to Google Sheets; skipping export.")
        return False
    sheet_id = _extract_sheet_id(spreadsheet_url)
    if not sheet_id:
        print(f"Warning: Could not parse sheet ID from URL: {spreadsheet_url}")
        return False
    try:
        ss = client.open_by_key(sheet_id)
        ws = ss.get_worksheet(0)  # first worksheet (gid=0)
        if ws is None:
            print("Warning: First worksheet (gid=0) not found.")
            return False
        # Build rows: A=heading, B=requirement_ID, C=anchor, D=thread
        rows: List[List[str]] = []
        for thread in threads:
            heading = thread.nearest_heading or ''
            req_id = thread.requirement_ID or ''
            anchor = thread.anchor_paragraph_text_marked or thread.anchor_paragraph_text or ''
            thread_text = _format_thread_text(thread)
            rows.append([heading, req_id, anchor, thread_text])
        # Overwrite existing data
        ws.clear()
        if rows:
            ws.update('A1', rows, value_input_option='RAW')
        print(f"Exported {len(rows)} threads to Google Sheet (first sheet).")
        return True
    except Exception as e:
        print(f"Failed to export to Google Sheets: {e}")
        return False

def main():
    # Allow optional CLI override of the path
    if len(sys.argv) > 1:
        docx_path = sys.argv[1]
    else:
        docx_path = DOCX_RELATIVE_PATH

    try:
        threads = extract_comments_threads(docx_path)
    except FileNotFoundError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
    except zipfile.BadZipFile:
        print("The specified file is not a valid .docx (zip) file.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Failed to read comments: {e}", file=sys.stderr)
        sys.exit(1)

    print_first_n_threads(threads, n=5)

    # Export all threads to the specified Google Sheet (first worksheet)
    export_url = 'https://docs.google.com/spreadsheets/d/1dIdHfVIDn_YQo6F93SyN5e8JddLR1muHZgYyv6MAWRA/edit?gid=0#gid=0'
    export_threads_to_gsheet(threads, export_url)

if __name__ == "__main__":
    main()