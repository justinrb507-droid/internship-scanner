import os
import re
from urllib.parse import urlparse
from ..models import Job


def search(cfg, session):
    key, cx = os.getenv("GOOGLE_API_KEY"), os.getenv("GOOGLE_CSE_ID")
    if not key or not cx:
        return []
    queries = cfg["search_queries"]
    n = min(int(cfg["scanner"].get("google_queries_per_run", 6)), len(queries))
    # Rotate by day-of-year so the free quota is spread across the full query set.
    from datetime import date
    start = date.today().timetuple().tm_yday % len(queries)
    chosen = [queries[(start+i) % len(queries)] for i in range(n)]
    jobs = []
    for q in chosen:
        r = session.get("https://www.googleapis.com/customsearch/v1", params={"key": key, "cx": cx, "q": q, "num": 10}, timeout=20)
        r.raise_for_status()
        for item in r.json().get("items", []):
            title = item.get("title", "")
            snippet = item.get("snippet", "")
            link = item.get("link", "")
            display = item.get("displayLink", "")
            company = re.sub(r"\s*(careers?|jobs?)\s*[-|:].*$", "", title, flags=re.I).strip() or display
            jobs.append(Job(title=title, company=company, location=snippet, description=snippet,
                            source="Google Custom Search", source_url=link))
    return jobs
