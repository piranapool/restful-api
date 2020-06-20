import pytest
import requests
from integration import *


# CREATE RECORD: POST
def create_record(route, req_body, exp_resp_body, exp_status):
    route = route
    resp = requests.post(route, json=req_body)
    resp_body = resp.json()

    assert exp_status == resp.status_code, \
        frmt_msg_invalid_status_code(exp_status, resp.status_code)
    assert ordered(exp_resp_body) == ordered(resp_body), \
        frmt_msg_invalid_response_body(exp_resp_body, resp_body)


# DELETE RECORD: DELETE
def delete_record(route, key, exp_status):
    route += "/" + key
    resp = requests.delete(route)

    assert exp_status == resp.status_code, \
        frmt_msg_invalid_status_code(exp_status, resp.status_code)


# FETCH RECORD: GET
def fetch_record(route, key, exp_resp_body, exp_status):
    route += "/" + key
    resp = requests.get(route)
    resp_body = resp.json()

    assert exp_status == resp.status_code, \
        frmt_msg_invalid_status_code(exp_status, resp.status_code)
    assert ordered(exp_resp_body) == ordered(resp_body), \
        frmt_msg_invalid_response_body(exp_resp_body, resp_body)


# UPDATE RECORD: PUT
def update_record(route, key, req_body, exp_resp_body, exp_status):
    route += "/" + key
    resp = requests.put(route, json=req_body)
    resp_body = resp.json()

    assert exp_status == resp.status_code, \
        frmt_msg_invalid_status_code(exp_status, resp.status_code)
    assert ordered(exp_resp_body) == ordered(resp_body), \
        frmt_msg_invalid_response_body(exp_resp_body, resp_body)
