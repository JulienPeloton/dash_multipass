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
"""Identity resolution through callback."""

import json

from flask import session, flash

from model import User, db, Identity
from app import multipass


@multipass.identity_handler
def identity_handler(identity_info):
    """Handle identity"""
    identity = Identity.query.filter_by(
        provider=identity_info.provider.name, identifier=identity_info.identifier
    ).first()
    if not identity:
        user = User.query.filter_by(email=identity_info.data["email"]).first()
        if not user:
            user = User(**identity_info.data.to_dict())
            db.session.add(user)
        identity = Identity(
            provider=identity_info.provider.name, identifier=identity_info.identifier
        )
        user.identities.append(identity)
    else:
        user = identity.user
    identity.multipass_data = json.dumps(identity_info.multipass_data)
    db.session.commit()

    # Add this information to the global session
    session["user_id"] = user.id

    flash(f"Received IdentityInfo: {identity_info}", "success")
