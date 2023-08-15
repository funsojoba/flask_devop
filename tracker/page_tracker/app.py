"""
    This is the home function for the app
"""

import os
from functools import cache

from flask import Flask
from redis import Redis, RedisError

app = Flask(__name__)
# redis = Redis()


def connect_to_redis():
    """
    Connects to the Redis server
    """
    return Redis.from_url(os.getenv("REDIS_URL", "redis://redis:6379"))  # Using the service name 'redis'



@app.get("/")
def home():
    """
        The home function, returns the view count of the page.
    """
    try:
        page_count = connect_to_redis().incr("page_count")
    except RedisError:
        app.logger.exception("Redis error")
        return "Sorry, something went wrong \N{pensive face}", 500
    times = "times" if page_count > 1 else "time"
    return f"This page has been viewed {page_count} {times}"



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
