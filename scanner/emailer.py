import os, smtplib, html
from email.message import EmailMessage
from datetime import date

def send(new_rows):
    addr, pwd = os.getenv("GMAIL_ADDRESS"), os.getenv("GMAIL_APP_PASSWORD")
    if not addr or not pwd: return False
    msg=EmailMessage(); msg['From']=addr; msg['To']=addr; msg['Subject']=f"Internship Scanner — {len(new_rows)} new — {date.today().isoformat()}"
    if not new_rows:
        msg.set_content("No new matching Summer 2027 internships were found today.")
        msg.add_alternative("<p>No new matching <strong>Summer 2027</strong> internships were found today.</p>",subtype='html')
    else:
        msg.set_content("\n".join(f"{r['title']} — {r['company']} — {r['source_url']}" for r in new_rows))
        trs=''.join(f"<tr><td>{html.escape(r['title'])}</td><td>{html.escape(r['company'])}</td><td>{html.escape(r['location'])}</td><td>{html.escape(r['deadline'])}</td><td>{r['paid']}</td><td>{r['cover_letter_required']}</td><td><a href=\"{html.escape(r['source_url'],quote=True)}\">View</a></td></tr>" for r in new_rows)
        msg.add_alternative(f"<h2>{len(new_rows)} new internship(s)</h2><table border='1' cellpadding='6' cellspacing='0'><tr><th>Title</th><th>Company</th><th>Location</th><th>Deadline</th><th>Paid</th><th>Cover Letter Required</th><th>Link</th></tr>{trs}</table>",subtype='html')
    with smtplib.SMTP_SSL("smtp.gmail.com",465) as s: s.login(addr,pwd); s.send_message(msg)
    return True
