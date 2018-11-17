# -*- coding: utf-8 -*-

from flask import (
    request, jsonify as flask_jsonify,
)
from httpbin.helpers import (
    H
)
import time


def get_request_md5():
    url_byte = H(request.base_url.encode("utf-8"), algorithm='SHA-256')
    data_byte = H(request.data, algorithm='SHA-256')
    md5 = H((url_byte.__add__(data_byte)).encode("utf-8"), algorithm='SHA-256')
    return md5


class TimeInterceptor:
    time_list = dict()

    def end_intercept(self):
        url = request.base_url
        if url.endswith('timecost'):
            return
        md5 = get_request_md5()
        time_result = self.time_list[md5]
        time_result.end_ts = time.time()
        print(time_result.get_duration())

    def start_intercept(self):
        url = request.base_url
        if url.endswith('timecost'):
            return
        md5 = get_request_md5()
        time_result = TimeResult(start_ts=time.time(), url=url)
        self.time_list[md5] = time_result


class TimeResult:
    def __init__(self, start_ts, url):
        self.start_ts = start_ts
        self.url = url
        self.end_ts = 0

    def get_duration(self):
        return self.end_ts - self.start_ts
