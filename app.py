from flask import Flask, request
from prometheus_client import Counter, generate_latest, Gauge, CONTENT_TYPE_LATEST
import random

app = Flask(__name__)

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint'])

MY_GAUGE = Gauge('my_gauge', 'description')
MY_GAUGE.set(123)

@app.before_request
def before_request_func():
    REQUEST_COUNT.labels(method=request.method, endpoint=request.path).inc()

@app.route("/")
def hello_world():
    MY_GAUGE.inc()
    return "Hello, world!"

@app.route("/health")
def health_check():
    return "API is available!"

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type':'text/plain; version=0.0.4; charset=utf-8'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 8299)
