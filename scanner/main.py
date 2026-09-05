import argparse, logging, yaml
from .database import connect, insert_job, all_rows
from .filtering import classify
from .http import session
from .sources import SOURCES
from .dashboard import build
from .sheets import sync
from .emailer import send

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def run(config_path="config/config.yaml", dry_run=False):
    with open(config_path, encoding="utf-8") as f: cfg=yaml.safe_load(f)
    s=session(cfg); conn=connect(); new=[]
    for source in SOURCES:
        try:
            found=source.search(cfg,s); logging.info("%s returned %d candidates",source.__name__,len(found))
            for job in found:
                status=classify(job,cfg)
                if not status: continue
                job.status=status
                if insert_job(conn,job):
                    row=conn.execute("SELECT * FROM internships WHERE job_id=?",(job.job_id,)).fetchone(); new.append(row)
        except Exception as exc: logging.exception("Source failed: %s: %s",source.__name__,exc)
    rows=all_rows(conn); build(rows)
    if not dry_run:
        try: sync(rows)
        except Exception: logging.exception("Google Sheets sync failed")
        try: send(new)
        except Exception: logging.exception("Email digest failed")
    logging.info("Done: %d new, %d total",len(new),len(rows)); return len(new)

if __name__=="__main__":
    p=argparse.ArgumentParser(); p.add_argument("--config",default="config/config.yaml"); p.add_argument("--dry-run",action="store_true"); a=p.parse_args(); run(a.config,a.dry_run)
