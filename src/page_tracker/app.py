import os
from flask import Flask
from functools import cache
from redis import Redis, RedisError


app = Flask(__name__)
# redis = Redis()


@app.get("/")
def home():
    try:
        page_count = redis().incr("page_count")
    except RedisError:
        app.logger.exception("Redis error")
        return "Sorry, something went wrong \N{pensive face}", 500
    else:
        times = "times" if page_count > 1 else "time"
        return f"This page has been viewed {page_count} {times}"



@cache
def redis():
    return Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))


if __name__ == "__main__":
    app.run(debug=True)