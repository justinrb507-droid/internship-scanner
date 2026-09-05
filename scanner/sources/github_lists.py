import re
from urllib.parse import urlparse
from ..models import Job

LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")


def raw_url(url):
    if "github.com" in url and "/blob/" in url:
        return url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
    return url


def search(cfg, session):
    jobs = []
    for url in cfg.get("github_lists", []):
        try:
            r = session.get(raw_url(url), timeout=20); r.raise_for_status()
        except Exception:
            continue
        for line in r.text.splitlines():
            low = line.lower()
            if "intern" not in low or "2027" not in low:
                continue
            links = LINK.findall(line)
            target = links[-1][1] if links else url
            cells = [re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", x).strip(" *`\t") for x in line.strip("| ").split("|")]
            cells = [c for c in cells if c and c != "-"]
            title = next((c for c in cells if "intern" in c.lower()), "Summer 2027 Engineering Internship")
            company = cells[0] if cells else urlparse(url).netloc
            location = next((c for c in cells if any(k in c.lower() for k in ["new york","nyc","remote","long island","brooklyn","queens","manhattan"])), "")
            jobs.append(Job(title=title, company=company, location=location, description=line,
                            source="GitHub list", source_url=target))
    return jobs
