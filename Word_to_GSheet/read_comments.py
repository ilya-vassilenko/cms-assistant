import os
import sys
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, List, Optional

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

        # capture paraId to map to commentsExtended threading info (if present)
        para_id = node.get(f"{{{NS['w15']}}}paraId")

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

        # Print replies recursively as subconversations
        _print_replies_recursive(thread, depth=1)
        count += 1

    if count == 0:
        print("No comments found.")
    else:
        print("=" * 80)

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

if __name__ == "__main__":
    main()