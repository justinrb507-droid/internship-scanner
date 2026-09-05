import time
import requests


def session(cfg):
    s = requests.Session()
    s.headers.update({"User-Agent": cfg["scanner"]["user_agent"]})
    return s


def get(s, url, cfg, **kwargs):
    time.sleep(float(cfg["scanner"].get("request_delay_seconds", 1)))
    r = s.get(url, timeout=int(cfg["scanner"].get("request_timeout_seconds", 20)), **kwargs)
    r.raise_for_status()
    return r
