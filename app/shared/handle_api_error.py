from flask import jsonify

from exceptions import ApiException


def handle_error(apex: ApiException):
    return jsonify(apex.msg), apex.status_code
