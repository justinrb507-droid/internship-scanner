def _contains(text, keywords):
    low = (text or "").lower()
    return any(k.lower() in low for k in keywords)


def classify(job, cfg):
    text = " ".join([job.title, job.location, job.description]).lower()
    # Season must be explicit. Avoid silently mixing 2026/2028 opportunities.
    if "2027" not in text or "summer" not in text:
        return None
    if _contains(text, cfg["reject_keywords"]):
        return None
    if not _contains(job.location + " " + job.description, cfg["locations"]["accepted_keywords"]):
        return None
    if _contains(text, cfg["preferred_keywords"]):
        return "new"
    if _contains(text, cfg["other_engineering_keywords"]):
        return "other"
    return None
