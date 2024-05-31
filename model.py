# Copyright 2024 Julien Peloton
# Author: Julien Peloton
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tables definition"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class"""

    pass


db = SQLAlchemy(model_class=Base)


class User(db.Model):
    """Base class for User information"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    affiliation = db.Column(db.String)
    node_id = db.Column(db.Integer)

    def __repr__(self):
        """Redefine string representation for the class User"""
        return f"<User id={self.id}, name={self.name}, email={self.email}>"


class Identity(db.Model):
    """Base class for User identity"""

    __tablename__ = "identities"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    provider = db.Column(db.String)
    identifier = db.Column(db.String)
    multipass_data = db.Column(db.Text)
    password = db.Column(db.String)
    user = db.relationship(User, backref="identities")

    @property
    def provider_impl(self):
        """Define who is the identity provider"""
        from app import multipass

        return multipass.identity_providers[self.provider]
