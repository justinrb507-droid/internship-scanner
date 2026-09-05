from dataclasses import dataclass
from hashlib import sha256
import re


def _norm(value: str) -> str:
    return re.sub(r"\s+", " ", (value or "").strip().lower())


@dataclass
class Job:
    title: str
    company: str
    location: str
    source: str
    source_url: str
    description: str = ""
    deadline: str = "unknown"
    paid: str = "unknown"
    cover_letter_required: str = "unknown"
    upstream_id: str = ""
    status: str = "new"

    @property
    def job_id(self) -> str:
        if self.upstream_id:
            raw = f"{self.source}|{self.upstream_id}"
        elif self.source_url:
            raw = self.source_url.split("#", 1)[0].rstrip("/")
        else:
            raw = "|".join(map(_norm, [self.company, self.title, self.location]))
        return sha256(raw.encode("utf-8")).hexdigest()[:32]
