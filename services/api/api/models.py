from api import app, db


groups_users = db.Table(
    'groups_users',
    db.Column('group_id', db.ForeignKey('groups.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True),
    db.Column('user_id', db.ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
)


class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    users = db.relationship(
        'User',
        secondary=groups_users,
        back_populates='groups'
    )

    def serialize(self):
        return {
            "name": self.name
        }

    def get_group(name):
        return db.session.query(Group).filter(Group.name == name).first()

    def get_members(name):
        userids = []

        for member in db.session.query(User.userid).order_by(
            User.userid).filter(User.groups.any(name=name)).all():
            userids.append(member.userid)

        return {"userids": userids}


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    userid = db.Column(db.String(12), unique=True, nullable=False)
    groups = db.relationship(
        'Group',
        secondary=groups_users,
        back_populates='users'
    )

    def serialize(self):
        groups = [];
        for group in self.groups:
            groups.append(group.name)

        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "userid": self.userid,
            "groups": sorted(groups)
        }

    def get_user(userid):
        return db.session.query(User).filter(User.userid == userid).first()
