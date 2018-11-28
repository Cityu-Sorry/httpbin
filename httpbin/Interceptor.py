# -*- coding: utf-8 -*-

from flask import (
    request, jsonify as flask_jsonify,
)
from httpbin.helpers import (
    H
)
import time


def get_request_sha(url, data):
    url_byte = H(url.encode("utf-8"), algorithm='SHA-256')
    data_byte = H("data_content_abc123".encode("utf-8"), algorithm='SHA-256')
    if isinstance(data, str):
        data = data.encode("utf-8")
    if data is not None:
        data_byte = H(data, algorithm='SHA-256')

    md5 = H((url_byte.__add__(data_byte)).encode("utf-8"), algorithm='SHA-256')
    return md5


class TimeInterceptor:
    time_list = dict()

    def end_intercept(self, my_request):
        if my_request.url.endswith('timecost'):
            return
        md5 = get_request_sha(my_request.url, my_request.data)
        time_result = self.time_list[md5]
        time_result.end_ts = time.time()
        print(time_result.get_duration())

    def start_intercept(self, my_request):
        if my_request.url.endswith('timecost'):
            return
        md5 = get_request_sha(my_request.url, my_request.data)
        time_result = TimeResult(start_ts=time.time(), url=my_request.base_url)
        self.time_list[md5] = time_result


class TimeResult:
    def __init__(self, start_ts, url):
        self.start_ts = start_ts
        self.url = url
        self.end_ts = 0

    def get_duration(self):
        return self.end_ts - self.start_ts
