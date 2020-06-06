import pytest
from .base_rest_tests import *


# (1) CREATE GROUP: SUCCESSFULLY
@pytest.mark.parametrize("req_body, exp_resp_body, exp_status", [
    ({"name": "a"}, {"name": "a"}, 201),
    ({"name": "twentyletterslonggrp"}, {"name": "twentyletterslonggrp"}, 201),
    ({"name": "admins"}, {"name": "admins"}, 201),
    ({"name": "A"}, {"name": "A"}, 201),
    ({"name": "TWENTYLETTERSLONGGRP"}, {"name": "TWENTYLETTERSLONGGRP"}, 201),
    ({"name": "ADMINS"}, {"name": "ADMINS"}, 201),
    ({"name": "Admins"}, {"name": "Admins"}, 201),
    ({"name": "users"}, {"name": "users"}, 201),
    ({"name": "partners"}, {"name": "partners"}, 201),
    ({"name": "associates"}, {"name": "associates"}, 201)
])
def test_create_group_successfully(
    groups_route, req_body, exp_resp_body, exp_status):

    create_record(groups_route, req_body, exp_resp_body, exp_status)


# (2) CREATE GROUP: ERRONEOUSLY
@pytest.mark.parametrize("req_body, exp_resp_body, exp_status", [
    (None, {"errors":{"request":["invalid request body"]}}, 400),
    (1, {"errors":{"request":["invalid request body"]}}, 400),
    ("", {"errors":{"request":["invalid request body"]}}, 400),
    ([], {"errors":{"request":["invalid request body"]}}, 400),
    ({}, {"errors":{"name":["required field"]}}, 400),
    ({"group_name": "admins"}, {"errors":
        {"group_name":["unknown field"],"name":["required field"]}}, 400),
    ({"name": "helpers", "state": "California"},
        {"errors":{"state":["unknown field"]}}, 400),
    ({"name": ""}, {"errors":{"name":
        ["must contain only letters, and be 1 to 20 characters long"]}}, 400),
    ({"name": "groupnameismuchtoolong"}, {"errors":{"name":
        ["must contain only letters, and be 1 to 20 characters long"]}}, 400),
    ({"name": "1"}, {"errors":{"name":
        ["must contain only letters, and be 1 to 20 characters long"]}}, 400),
    ({"name": "sandiego-ca"}, {"errors":{"name":
        ["must contain only letters, and be 1 to 20 characters long"]}}, 400),
    ({"name": "admins"},
        {"errors":{"name":["group 'admins' already exists"]}}, 409)
])
def test_create_group_erroneously(
    groups_route, req_body, exp_resp_body, exp_status):

    create_record(groups_route, req_body, exp_resp_body, exp_status)


# (3) CREATE USER: SUCCESSFULLY
@pytest.mark.parametrize("req_body, exp_resp_body, exp_status", [
    ({
        "first_name": "Mickey",
        "last_name": "Mouse",
        "userid": "mic619",
        "groups": ["admins", "users"]
    }, {
        "first_name": "Mickey",
        "last_name": "Mouse",
        "userid": "mic619",
        "groups": ["admins", "users"]
    }, 201),
    ({
        "first_name": "Minnie",
        "last_name": "Mouse",
        "userid": "min2020",
        "groups": ["users"]
    }, {
        "first_name": "Minnie",
        "last_name": "Mouse",
        "userid": "min2020",
        "groups": ["users"]
    }, 201),
    ({
        "first_name": "Donald",
        "last_name": "Duck",
        "userid": "dd415",
        "groups": ["users", "partners"]
    }, {
        "first_name": "Donald",
        "last_name": "Duck",
        "userid": "dd415",
        "groups": ["users", "partners"]
    }, 201),
    ({
        "first_name": "Snow",
        "last_name": "White",
        "userid": "snowW1",
        "groups": []
    }, {
        "first_name": "Snow",
        "last_name": "White",
        "userid": "snowW1",
        "groups": []
    }, 201),
    ({
        "first_name": "John",
        "last_name": "Lennon",
        "userid": "jlLetItBe",
        "groups": ["associates"]
    }, {
        "first_name": "John",
        "last_name": "Lennon",
        "userid": "jlLetItBe",
        "groups": ["associates"]
    }, 201),
    ({
        "first_name": "Paul",
        "last_name": "McCarney",
        "userid": "pmOoo",
        "groups": ["partners", "associates"]
    }, {
        "first_name": "Paul",
        "last_name": "McCarney",
        "userid": "pmOoo",
        "groups": ["associates", "partners"]
    }, 201),
    ({
        "first_name": "George",
        "last_name": "Harrison",
        "userid": "ghStrum1",
        "groups": ["associates", "users"]
    }, {
        "first_name": "George",
        "last_name": "Harrison",
        "userid": "ghStrum1",
        "groups": ["associates", "users"]
    }, 201),
    ({
        "first_name": "Ringo",
        "last_name": "Star",
        "userid": "ringOstr",
        "groups": ["associates"]
    }, {
        "first_name": "Ringo",
        "last_name": "Star",
        "userid": "ringOstr",
        "groups": ["associates"]
    }, 201)
])
def test_create_user_successfully(
    users_route, req_body, exp_resp_body, exp_status):

    create_record(users_route, req_body, exp_resp_body, exp_status)


# (4) CREATE USER: ERRONEOUSLY
@pytest.mark.parametrize("req_body, exp_resp_body, exp_status", [
    (None, {"errors":{"request":["invalid request body"]}}, 400),
    (1, {"errors":{"request":["invalid request body"]}}, 400),
    ("", {"errors":{"request":["invalid request body"]}}, 400),
    ([], {"errors":{"request":["invalid request body"]}}, 400),
    ({}, {"errors":{"first_name":["required field"],
        "groups":["required field"],"last_name":["required field"],
        "userid":["required field"]}}, 400),
    ({
        "first_name": "",
        "last_name": "groupnameismuchtoolong",
        "userid": "",
        "groups": ["admins", "users"]
    }, {"errors":{"first_name":
        ["must contain only letters, and be 1 to 20 characters long"],
        "last_name":["must contain only letters, and "
        "be 1 to 20 characters long"],"userid":["must contain only letters "
        "and numbers, and be 5 to 12 characters long"]}}, 400),
    ({
        "first_name": "John",
        "last_name": "Wayne",
        "userid": "jw",
        "groups": ["users"]
    }, {"errors":{"userid":["must contain only letters and numbers, "
        "and be 5 to 12 characters long"]}}, 400),
    ({
        "first_name": "Mickey",
        "last_name": "Mouse",
        "userid": "mic619",
        "groups": ["admins", "users"]
    }, {"errors":{"userid":["user 'mic619' already exists"]}}, 409),
    ({
        "first_name": "Bruce",
        "last_name": "Lee",
        "userid": "bl415",
        "groups": ["kf"]
    }, {"errors":{"name":["group 'kf' not found"]}}, 400)
])
def test_create_user_erroneously(
    users_route, req_body, exp_resp_body, exp_status):

    create_record(users_route, req_body, exp_resp_body, exp_status)


# (5) UPDATE GROUP: SUCCESSFULLY
@pytest.mark.parametrize("key, req_body, exp_resp_body, exp_status", [
    ("admins", {"userids": ["min2020", "mic619"]},
        {"userids": ["min2020", "mic619"]}, 200),
    ("users", {"userids": ["snowW1", "dd415", "min2020", "mic619"]},
        {"userids": ["snowW1", "dd415", "min2020", "mic619"]}, 200),
    ("partners", {"userids": []}, {"userids": []}, 200),
    ("associates", {"userids": ["mic619", "min2020", "dd415"]},
        {"userids": ["mic619", "min2020", "dd415"]}, 200)
])
def test_update_group_successfully(
    groups_route, key, req_body, exp_resp_body, exp_status):

    update_record(groups_route, key, req_body, exp_resp_body, exp_status)


# (6) UPDATE GROUP: ERRONEOUSLY
@pytest.mark.parametrize("key, req_body, exp_resp_body, exp_status", [
    ("members", {"userids": []},
        {"errors":{"name":["group 'members' not found"]}}, 404),
    ('admins', None, {"errors":{"request":["invalid request body"]}}, 400),
    ('admins', 1, {"errors":{"request":["invalid request body"]}}, 400),
    ('admins', "", {"errors":{"request":["invalid request body"]}}, 400),
    ('admins', [], {"errors":{"request":["invalid request body"]}}, 400),
    ('admins', {}, {"errors":{"userids":["required field"]}}, 400),
    ('admins', {"userids": None},
        {"errors":{"userids":
        ["must be a list of userids containing only letters "
        "and numbers (each 5 to 12 characters long)",
        "null value not allowed"]}}, 400),
    ('admins', {"userids": ""},
        {"errors":{"userids":["must be of list type"]}}, 400),
    ('admins', {"userids": {}},
        {"errors":{"userids":["must be of list type"]}}, 400),
    ('admins', {"userids": ["x"]},
        {"errors":{"userids":
        ["must be a list of userids containing only letters "
        "and numbers (each 5 to 12 characters long)"]}}, 400),
    ('admins', {"userids": ["animals"]},
        {"errors":{"userid":["user 'animals' not found"]}}, 400)
])
def test_update_group_erroneously(
    groups_route, key, req_body, exp_resp_body, exp_status):

    update_record(groups_route, key, req_body, exp_resp_body, exp_status)


# (7) UPDATE USER: SUCCESSFULLY
@pytest.mark.parametrize("key, req_body, exp_resp_body, exp_status", [
    ("mic619", {
        "first_name": "Mic",
        "last_name": "Mouse",
        "userid": "mic619",
        "groups": ["admins", "users", "associates"]
    }, {
        "first_name": "Mic",
        "last_name": "Mouse",
        "userid": "mic619",
        "groups": ["admins", "users", "associates"]
    }, 200),
    ("mic619", {
        "first_name": "Mic",
        "last_name": "Mousey",
        "userid": "mic619",
        "groups": ["admins", "users", "associates"]
    }, {
        "first_name": "Mic",
        "last_name": "Mousey",
        "userid": "mic619",
        "groups": ["admins", "users", "associates"]
    }, 200),
    ("mic619", {
        "first_name": "Mic",
        "last_name": "Mousey",
        "userid": "mic619ms",
        "groups": ["admins", "users", "associates"]
    }, {
        "first_name": "Mic",
        "last_name": "Mousey",
        "userid": "mic619ms",
        "groups": ["admins", "users", "associates"]
    }, 200),
    ("mic619ms", {
        "first_name": "Mickey",
        "last_name": "Mouse",
        "userid": "mic619",
        "groups": ["admins", "users", "associates"]
    }, {
        "first_name": "Mickey",
        "last_name": "Mouse",
        "userid": "mic619",
        "groups": ["admins", "users", "associates"]
    }, 200),
    ("mic619", {
        "first_name": "Mickey",
        "last_name": "Mouse",
        "userid": "mic619",
        "groups": ["admins", "associates", "partners"]
    }, {
        "first_name": "Mickey",
        "last_name": "Mouse",
        "userid": "mic619",
        "groups": ["admins", "associates", "partners"]
    }, 200),
    ("mic619", {
        "first_name": "Mickey",
        "last_name": "Mouse",
        "userid": "mic619",
        "groups": []
    }, {
        "first_name": "Mickey",
        "last_name": "Mouse",
        "userid": "mic619",
        "groups": []
    }, 200),
    ("mic619", {
        "first_name": "Mickey",
        "last_name": "Mouse",
        "userid": "mic619",
        "groups": ["admins", "users", "associates"]
    }, {
        "first_name": "Mickey",
        "last_name": "Mouse",
        "userid": "mic619",
        "groups": ["admins", "users", "associates"]
    }, 200)
])
def test_update_user_successfully(
    users_route, key, req_body, exp_resp_body, exp_status):

    update_record(users_route, key, req_body, exp_resp_body, exp_status)


# (8) UPDATE USER: ERRONEOUSLY
@pytest.mark.parametrize("key, req_body, exp_resp_body, exp_status", [
    ("mickey", None,
        {"errors":{"userid":["user 'mickey' not found"]}}, 404),
    ("min2020", None, {"errors":{"request":["invalid request body"]}}, 400),
    ("min2020", 1, {"errors":{"request":["invalid request body"]}}, 400),
    ("min2020", "", {"errors":{"request":["invalid request body"]}}, 400),
    ("min2020", [], {"errors":{"request":["invalid request body"]}}, 400),
    ("min2020", {}, {"errors":{"first_name":["required field"],
        "groups":["required field"],"last_name":["required field"],
        "userid":["required field"]}}, 400),
    ("min2020", {
        "first_name": "",
        "last_name": "groupnameismuchtoolong",
        "userid": "",
        "groups": ["admins", "users"]
    }, {"errors":{"first_name":
        ["must contain only letters, and be 1 to 20 characters long"],
        "last_name":["must contain only letters, and "
        "be 1 to 20 characters long"],"userid":["must contain only letters "
        "and numbers, and be 5 to 12 characters long"]}}, 400),
    ("min2020", {
        "first_name": "John",
        "last_name": "Wayne",
        "userid": "jw",
        "groups": ["users"]
    }, {"errors":{"userid":["must contain only letters and numbers, "
        "and be 5 to 12 characters long"]}}, 400),
    ("min2020", {
        "first_name": "Mickey",
        "last_name": "Mouse",
        "userid": "mic619",
        "groups": ["admins", "users"]
    }, {"errors":{"userid":["user 'mic619' already exists"]}}, 409),
    ("min2020", {
        "first_name": "Bruce",
        "last_name": "Lee",
        "userid": "bl415",
        "groups": ["kf"]
    }, {"errors":{"name":["group 'kf' not found"]}}, 400)
])
def test_update_user_erroneously(
    users_route, key, req_body, exp_resp_body, exp_status):

    update_record(users_route, key, req_body, exp_resp_body, exp_status)


# (9) DELETE GROUP: SUCCESSFULLY
@pytest.mark.parametrize("key, exp_status", [
     ("a", 204),
     ("twentyletterslonggrp", 204),
     ("A", 204),
     ("TWENTYLETTERSLONGGRP", 204),
     ("ADMINS", 204),
     ("Admins", 204)
])
def test_delete_group_successfully(groups_route, key, exp_status):
    delete_record(groups_route, key, exp_status)


# (10) DELETE GROUP: ERRONEOUSLY
@pytest.mark.parametrize("key, exp_status", [
     ("a", 404),
     ("twentyletterslonggrp", 404),
     ("A", 404),
     ("TWENTYLETTERSLONGGRP", 404),
     ("ADMINS", 404),
     ("Admins", 404)
])
def test_delete_group_erroneously(groups_route, key, exp_status):
    delete_record(groups_route, key, exp_status)


# (11) DELETE USER: SUCCESSFULLY
@pytest.mark.parametrize("key, exp_status", [
     ("jlLetItBe", 204),
     ("pmOoo", 204),
     ("ghStrum1", 204),
     ("ringOstr", 204)
])
def test_delete_user_successfully(users_route, key, exp_status):
    delete_record(users_route, key, exp_status)


# (12) DELETE USER: ERRONEOUSLY
@pytest.mark.parametrize("key, exp_status", [
     ("jlLetItBe", 404),
     ("pmOoo", 404),
     ("ghStrum1", 404),
     ("ringOstr", 404)
])
def test_delete_user_erroneously(users_route, key, exp_status):
    delete_record(users_route, key, exp_status)


# (13) FETCH GROUP: SUCCESSFULLY
@pytest.mark.parametrize("key, exp_resp_body, exp_status", [
     ("admins", {"userids":["mic619", "min2020"]}, 200),
     ("users", {"userids":["dd415","mic619","min2020", "snowW1"]}, 200),
     ("partners", {"userids":[]}, 200),
     ("associates", {"userids":["dd415","mic619","min2020"]}, 200)
])
def test_fetch_group_successfully(
    groups_route, key, exp_resp_body, exp_status):

    fetch_record(groups_route, key, exp_resp_body, exp_status)


# (14) FETCH GROUP: ERRONEOUSLY
@pytest.mark.parametrize("key, exp_resp_body, exp_status", [
    ("1", {"errors":{"name":["group '1' not found"]}}, 404),
    ("[]", {"errors":{"name":["group '[]' not found"]}}, 404),
    ("{}", {"errors":{"name":["group '{}' not found"]}}, 404),
    ("()", {"errors":{"name":["group '()' not found"]}}, 404),
    ("<>", {"errors":{"name":["group '<>' not found"]}}, 404),
    ("managers-1", {"errors":{"name":["group 'managers-1' not found"]}}, 404),
    ("oranges", {"errors":{"name":["group 'oranges' not found"]}}, 404),
    ("apples", {"errors":{"name":["group 'apples' not found"]}}, 404),
    ("bananas", {"errors":{"name":["group 'bananas' not found"]}}, 404)
])
def test_fetch_group_erroneously(
    groups_route, key, exp_resp_body, exp_status):

    fetch_record(groups_route, key, exp_resp_body, exp_status)


# (15) FETCH USER: SUCCESSFULLY
@pytest.mark.parametrize("key, exp_resp_body, exp_status", [
    ("mic619", {
        "first_name": "Mickey",
        "last_name": "Mouse",
        "userid": "mic619",
        "groups": ["admins", "users", "associates"]
    }, 200),
    ("min2020", {
        "first_name": "Minnie",
        "last_name": "Mouse",
        "userid": "min2020",
        "groups": ["admins", "users", "associates"]
    }, 200),
    ("dd415", {
        "first_name": "Donald",
        "last_name": "Duck",
        "userid": "dd415",
        "groups": ["users", "associates"]
    }, 200),
    ("snowW1", {
        "first_name": "Snow",
        "last_name": "White",
        "userid": "snowW1",
        "groups": ["users"]
    }, 200)
])
def test_fetch_user_successfully(
    users_route, key, exp_resp_body, exp_status):

    fetch_record(users_route, key, exp_resp_body, exp_status)


# (16) FETCH USER: ERRONEOUSLY
@pytest.mark.parametrize("key, exp_out, exp_status", [
    ("1", {"errors":{"userid":["user '1' not found"]}}, 404),
    ("[]", {"errors":{"userid":["user '[]' not found"]}}, 404),
    ("{}", {"errors":{"userid":["user '{}' not found"]}}, 404),
    ("()", {"errors":{"userid":["user '()' not found"]}}, 404),
    ("<>", {"errors":{"userid":["user '<>' not found"]}}, 404),
    ("batman-1", {"errors":{"userid":["user 'batman-1' not found"]}}, 404),
    ("robin", {"errors":{"userid":["user 'robin' not found"]}}, 404),
    ("pluto858", {"errors":{"userid":["user 'pluto858' not found"]}}, 404),
    ("cinderella", {"errors":{"userid":["user 'cinderella' not found"]}}, 404)
])
def test_fetch_user_erroneously(
    users_route, key, exp_out, exp_status):

    fetch_record(users_route, key, exp_out, exp_status)
