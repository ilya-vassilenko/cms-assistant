import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple


_TS_RE = re.compile(r"^(?P<prefix>\d{4}-\d{2}-\d{2} \d{2}_\d{2})")


@dataclass(frozen=True)
class LatestOutputPick:
    path: Path
    prefix: str  # YYYY-MM-dd HH_mm
    timestamp: datetime


class LatestOutputPicker:
    """
    Picks the latest article markdown from an Output folder based on filename prefix:
    YYYY-MM-dd HH_mm
    """

    def __init__(self, timestamp_format: str = "%Y-%m-%d %H_%M"):
        self.timestamp_format = timestamp_format

    def pick_latest(self, output_dir: Path) -> LatestOutputPick:
        if not output_dir.exists() or not output_dir.is_dir():
            raise FileNotFoundError(f"Output folder not found: {output_dir}")

        candidates: List[LatestOutputPick] = []
        for p in output_dir.glob("*.md"):
            if not p.is_file():
                continue
            m = _TS_RE.match(p.name)
            if not m:
                continue
            prefix = m.group("prefix")
            try:
                ts = datetime.strptime(prefix, self.timestamp_format)
            except ValueError:
                continue
            candidates.append(LatestOutputPick(path=p, prefix=prefix, timestamp=ts))

        if not candidates:
            raise FileNotFoundError(
                f"No timestamped .md files found in Output folder (expected prefix 'YYYY-MM-dd HH_mm'): {output_dir}"
            )

        candidates.sort(key=lambda x: x.timestamp)
        return candidates[-1]

