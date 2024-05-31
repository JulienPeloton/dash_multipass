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
"""Application routes."""

from flask import url_for, Blueprint

from app import multipass

api_bp = Blueprint("/", __name__)


@api_bp.route("/login/", methods=("GET", "POST"))
@api_bp.route("/login/<provider>", methods=("GET", "POST"))
def login(provider=None):
    """Basic login redirect"""
    return multipass.process_login(provider)


@api_bp.route("/logout")
def logout():
    """Basic logout redirect"""
    return multipass.logout(url_for("/"), clear_session=True)
