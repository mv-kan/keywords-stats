from fastapi.testclient import TestClient
import os
os.environ["KEYWORDS_STATS_REDIS_URL"] = "redis://localhost:6379"

from .main import app
import time

client = TestClient(app)

def test_main():
    res = client.post("/api/v1/events", content='Avanan is a leading Enterprise Solution\nfor Cloud Email and Collaboration Security')
    assert res.status_code == 200
    res = client.post("/api/v1/events", content='CheckPoint Research have been\nobserving an enormous rise in email attacks since the beginning of 2020')
    assert res.status_code == 200
    res = client.get("/api/v1/stats?interval=1")
    assert res.status_code == 200
    assert res.json() == {"checkpoint":1,"avanan":1,"email":2,"security":1}
    time.sleep(1)
    
    res = client.get("/api/v1/stats?interval=1")
    assert res.status_code == 200
    assert res.json() == {"checkpoint":0,"avanan":0,"email":0,"security":0}
    