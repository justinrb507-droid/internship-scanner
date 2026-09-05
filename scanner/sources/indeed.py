"""Best-effort placeholder for Indeed.

Indeed does not provide a universally available anonymous public jobs feed suitable for
this project. We intentionally do not scrape protected search pages. Indeed listings can
still be discovered by Google Custom Search. This adapter remains isolated so a documented
feed/API can be added later without changing the scanner.
"""
def search(cfg, session):
    return []
