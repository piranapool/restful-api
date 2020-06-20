import re
from flask import jsonify, request
from cerberus import Validator
from api import app, db
from .models import Group, User


'''
    CREATE GROUP:
    Creates an empty group. POSTs to an existing group are treated as
    errors and flagged with the appropriate HTTP status code (409).
    The body should contain a `name` parameter.
'''
@app.route('/groups', methods=['POST'])
def create_group():
    # validate data
    data = request.get_json()

    if not isinstance(data, dict):
        return ErrorResponse.invalid_request_body()

    invalid = DataValidator.is_valid(data, DataValidator.SCHEMA_GROUP)
    if invalid:
        return invalid

    name = data['name']

    # group MUST NOT exist
    if Group.get_group(name):
        return ErrorResponse.group_exists(name)

    # persist group to db
    group = Group(name=name)
    db.session.add(group)
    db.session.commit()

    return jsonify(group.serialize()), 201


'''
    DELETE GROUP:
    Deletes a group. Returns 404 if the group doesn't exist.
'''
@app.route('/groups/<name>', methods=['DELETE'])
def delete_group(name):
    group = Group.get_group(name)

    # group MUST exist
    if not group:
        return ErrorResponse.group_not_found(name)

    # remove group from db
    db.session.delete(group)
    db.session.commit()

    return '', 204


'''
    FETCH GROUP:
    Returns a JSON list of userids containing the members of that group.
    Returns a 404 if the group doesn't exist.
'''
@app.route('/groups/<name>', methods=['GET'])
def fetch_group(name):
    group = Group.get_group(name)

    # group MUST exist
    if not group:
        return ErrorResponse.group_not_found(name)

    # fetch members
    members = Group.get_members(name)

    return jsonify(members), 200


'''
    UPDATE GROUP:
    Updates the membership list for the group. The body of the request
    should be a JSON list describing the group's members. PUTs to a
    non-existant group return a 404.
'''
@app.route('/groups/<name>', methods=['PUT'])
def update_group(name):
    group = Group.get_group(name)

    # group MUST exist
    if not group:
        return ErrorResponse.group_not_found(name)

    # validate data
    data = request.get_json()

    if not isinstance(data, dict):
        return ErrorResponse.invalid_request_body()

    invalid = DataValidator.is_valid(data, DataValidator.SCHEMA_GROUP_MEMBERS)
    if invalid:
        return invalid

    userids = data['userids']

    # remove unwanted users
    for user in reversed(group.users):
        if user.userid in userids:
            userids.remove(user.userid)
        else:
            group.users.remove(user)

    # add wanted users
    for userid in userids:
        user = User.get_user(userid)

        # user MUST exist
        if not user:
            return ErrorResponse.user_not_found(userid, 400)

        group.users.append(user)

    # persist group to db
    db.session.commit()

    # fetch members
    members = Group.get_members(name)

    return jsonify(members), 200


'''
    CREATE USER:
    Creates a new user record. The body of the request should be a valid
    user record. POSTs to an existing user are treated as errors and flagged
    with the appropriate HTTP status code (409).
'''
@app.route('/users', methods=['POST'])
def create_user():
    # validate data
    data = request.get_json()

    if not isinstance(data, dict):
        return ErrorResponse.invalid_request_body()

    invalid = DataValidator.is_valid(data, DataValidator.SCHEMA_USER)
    if invalid:
        return invalid

    first_name = data['first_name']
    last_name = data['last_name']
    userid = data['userid']
    groups = data['groups']

    # user MUST NOT exist
    if User.get_user(userid):
        return ErrorResponse.user_exists(userid)

    # build user object
    user = User(
        first_name=first_name,
        last_name=last_name,
        userid=userid
    )

    # add groups
    for name in groups:
        group = Group.get_group(name)

        # group MUST exist
        if not group:
            return ErrorResponse.group_not_found(name, 400)

        user.groups.append(group)

    # persist user to db
    db.session.add(user)
    db.session.commit()

    return jsonify(user.serialize()), 201


'''
    DELETE USER:
    Deletes a user record. Returns 404 if the user doesn't exist.
'''
@app.route('/users/<userid>', methods=['DELETE'])
def delete_user(userid):
    user = User.get_user(userid)

    # user MUST exist
    if not user:
        return ErrorResponse.user_not_found(userid)

    # remove user from db
    db.session.delete(user)
    db.session.commit()

    return '', 204


'''
    FETCH USER:
    Returns the matching user record or 404 if none exist.
'''
@app.route('/users/<userid>', methods=['GET'])
def fetch_user(userid):
    user = User.get_user(userid)

    # user MUST exist
    if not user:
        return ErrorResponse.user_not_found(userid)

    return jsonify(user.serialize()), 200


'''
    UPDATE USER:
    Updates an existing user record. The body of the request should
    be a valid user record. PUTs to a non-existant user return a 404.
'''
@app.route('/users/<userid>', methods=['PUT'])
def update_user(userid):
    user = User.get_user(userid)

    # user MUST exist
    if not user:
        return ErrorResponse.user_not_found(userid)

    # validate data
    data = request.get_json()

    if not isinstance(data, dict):
        return ErrorResponse.invalid_request_body()

    invalid = DataValidator.is_valid(data, DataValidator.SCHEMA_USER)
    if invalid:
        return invalid

    first_name = data['first_name']
    last_name = data['last_name']
    new_userid = data['userid']
    groups = data['groups']

    # user MUST NOT exist (for new userid)
    if new_userid != userid and User.get_user(new_userid):
        return ErrorResponse.user_exists(new_userid)

    # update user
    user.first_name = first_name
    user.last_name = last_name
    user.userid = new_userid

    # remove unwanted groups
    for group in reversed(user.groups):
        if group.name in groups:
            groups.remove(group.name)
        else:
            user.groups.remove(group)

    # add wanted groups
    for name in groups:
        group = Group.get_group(name)

        # group MUST exist
        if not group:
            return ErrorResponse.group_not_found(name, 400)

        user.groups.append(group)

    # persist user to db
    db.session.commit()

    return jsonify(user.serialize()), 200


'''
    DATA VALIDATORS
'''
class DataValidator(Validator):
    SCHEMA_GROUP =  {
        "name": {"required": True, "type": "string", "is_name": True}
    }
    SCHEMA_GROUP_MEMBERS = {
        "userids": {"required": True, "type": "list", "is_members": True}
    }
    SCHEMA_USER = {
        "first_name": {"required": True, "type": "string", "is_name": True},
        "last_name": {"required": True, "type": "string", "is_name": True},
        "userid": {"required": True, "type": "string", "is_userid": True},
        "groups": {"required": True, "type": "list", "is_groups": True}
    }

    def is_valid(data, schema, status=400):
        v = DataValidator()
        if not v.validate(data, schema):
            return jsonify(errors = v.errors), status

    def _validate_is_name(self, is_name, field, value):
        '''
            {"type": "boolean"}
        '''
        if is_name and not re.match("^[a-zA-Z]{1,20}$", str(value)):
            self._error(field, "must contain only letters, "
                "and be 1 to 20 characters long")

    def _validate_is_userid(self, is_userid, field, value):
        '''
            {"type": "boolean"}
        '''
        if is_userid and not re.match("^[a-zA-Z0-9]{5,12}$", str(value)):
            self._error(field, "must contain only letters and numbers, "
                "and be 5 to 12 characters long")

    def _validate_is_groups(self, is_groups, field, value):
        '''
            {"type": "boolean"}
        '''
        def validate_group_names(names):
            if not isinstance(names, list):
                return False

            for name in names:
                if not re.match("^[a-zA-Z]{1,20}$", str(name)):
                    return False
            return True

        if is_groups and not validate_group_names(value):
            self._error(field, "must be a list of group names "
                "containing only letters "
                "(each 1 to 20 characters long)")

    def _validate_is_members(self, is_members, field, value):
        '''
            {"type": "boolean"}
        '''
        def validate_userids(userids):
            if not isinstance(userids, list):
                return False

            for userid in userids:
                if not re.match("^[a-zA-Z0-9]{5,12}$", str(userid)):
                    return False
            return True

        if is_members and not validate_userids(value):
            self._error(field, "must be a list of userids "
                "containing only letters and numbers "
                "(each 5 to 12 characters long)")


'''
    ERROR RESPONSES
'''
class ErrorResponse():
    def invalid_request_body(status=400):
        return jsonify({"errors":
            {"request": ["invalid request body"]}}), status

    def group_exists(name, status=409):
        return jsonify({"errors":
            {"name": ["group '" + name + "' already exists"]}}), status

    def group_not_found(name, status=404):
        return jsonify({"errors":
            {"name": ["group '" + name + "' not found"]}}), status

    def user_exists(userid, status=409):
        return jsonify({"errors":
            {"userid": ["user '" + userid + "' already exists"]}}), status

    def user_not_found(userid, status=404):
        return jsonify({"errors":
            {"userid": ["user '" + userid + "' not found"]}}), status
