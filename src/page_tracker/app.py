
from flask import Flask
from redis import Redis
from functools import cache

app = Flask(__name__)
# redis = Redis()


@app.get("/")
def home():
    page_count = redis().incr("page_count")
    times = "times" if page_count > 1 else "time"
    return f"This page has been viewed {page_count} {times}"


@cache
def redis():
    return Redis()


if __name__ == "__main__":
    app.run(debug=True)