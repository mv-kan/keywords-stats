from fastapi import FastAPI
import redis
from pydantic import BaseModel
from fastapi.responses import Response
from fastapi.requests import Request
import time

redis_url = "redis://redis:6379"
app = FastAPI()
redis_conn = redis.from_url(redis_url, decode_responses=True)
redis_ts = redis_conn.ts()
keywords = ["checkpoint", "avanan", "email", "security"]
keywords_ts_prefix = "ts_"
for keyword in keywords:
    redis_ts.create(keywords_ts_prefix+keyword)

class StatsResponse(BaseModel):
    checkpoint: int
    avanan: int
    email: int
    security: int

@app.post("/api/v1/events", response_class=Response)
async def events(text: Request):
    text = await text.body()
    text = text.decode('ascii').lower()
    for keyword in keywords:
        count = text.count(keyword)
        redis_ts.add(keywords_ts_prefix+keyword, "*", count)

@app.get("/api/v1/stats")
async def stats(interval: int = 1) -> StatsResponse:
    timestamp = round(time.time() * 1000)
    interval *= 1000
    result = StatsResponse(checkpoint=0, avanan=0, email=0, security=0)
    for keyword in keywords:
        ts = keywords_ts_prefix+keyword
        lower = timestamp - interval
        sum = redis_ts.range(ts, lower, timestamp, aggregation_type='sum', bucket_size_msec=interval, empty=True)
        if len(sum) > 0:
            setattr(result, keyword, int(sum[0][1]))
    return result

import uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)