import tempfile
from scanner.models import Job
from scanner.database import connect, insert_job, all_rows
from scanner.filtering import classify

def cfg():
    return {"reject_keywords":["seniors only","graduate students only"],"locations":{"accepted_keywords":["new york","remote"]},"preferred_keywords":["mechanical engineering","robotics","manufacturing"],"other_engineering_keywords":["engineering intern"]}

def test_stable_id():
    a=Job("Mechanical Engineering Intern","Acme","New York","x","https://example.com/job/1")
    b=Job("Changed title","Acme","Remote","x","https://example.com/job/1")
    assert a.job_id==b.job_id

def test_filter():
    j=Job("Summer 2027 Mechanical Engineering Intern","Acme","New York, NY","x","https://e/x")
    assert classify(j,cfg())=="new"
    j2=Job("Summer 2027 Engineering Intern","Acme","Remote","x","https://e/y")
    assert classify(j2,cfg())=="other"

def test_db_dedup():
    with tempfile.NamedTemporaryFile(suffix='.db') as f:
        c=connect(f.name); j=Job("Summer 2027 Robotics Intern","Acme","Remote","x","https://e/1")
        assert insert_job(c,j); assert not insert_job(c,j); assert len(all_rows(c))==1
