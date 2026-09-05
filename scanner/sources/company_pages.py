"""Conservative company-page discovery.

Career sites frequently use JavaScript/ATS APIs and change without notice. This adapter
indexes visible links only; Google CSE queries cover the same companies more reliably.
It never bypasses access controls or robots protections.
"""
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from ..models import Job


def search(cfg, session):
    jobs = []
    for company in cfg.get("companies", []):
        try:
            r = session.get(company["careers_url"], timeout=20)
            if r.status_code != 200: continue
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.find_all("a", href=True):
                text = " ".join(a.stripped_strings)
                context = " ".join(a.parent.stripped_strings) if a.parent else text
                combined = f"{text} {context}"
                low = combined.lower()
                if "intern" in low and "2027" in low:
                    jobs.append(Job(title=text or "Summer 2027 Internship", company=company["name"],
                                    location=context, description=context, source="Company careers page",
                                    source_url=urljoin(company["careers_url"], a["href"])))
        except Exception:
            continue
    return jobs
