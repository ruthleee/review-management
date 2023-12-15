import time
from flask import Flask
from flask_http_middleware import MiddlewareManager, BaseHTTPMiddleware

app = Flask(__name__)

class MetricsMiddleware(BaseHTTPMiddleware):
    def __init__(self):
        super().__init__()

    def dispatch(self, request, call_next):
        t0 = time.time()
        response = call_next(request)
        response_time = time.time()-t0
        response.headers.add("response_time", response_time)
        print("response_time = " + str(response_time))
        return response
