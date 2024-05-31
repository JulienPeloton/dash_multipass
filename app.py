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
# limitations under the License.c
"""Dash application"""

import dash

import logging
import sys
from os.path import exists

from model import db
from flask_multipass import Multipass

_LOG = logging.getLogger(__name__)

app = dash.Dash(__name__)

if not exists("configuration.cfg"):
    _LOG.error("You need to create the configuration file: configuration.cfg")
    _LOG.error("Check https://github.com/JulienPeloton/dash_multipass")
    sys.exit()

app.server.config.from_pyfile("configuration.cfg")
app.server.secret_key = "my super secret key"
multipass = Multipass(app.server)

server = app.server

db.init_app(server)
with server.app_context():
    db.create_all()
