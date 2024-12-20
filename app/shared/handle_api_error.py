from flask import jsonify

from exceptions import ApiException


def handle_error(apex: ApiException):
    return jsonify(apex.msg), apex.status_code


def handle_msg_error(apex: ApiException):
    return jsonify({"msg": apex.msg}), apex.status_code
