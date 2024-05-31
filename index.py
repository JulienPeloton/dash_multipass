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
"""Application launcher & callbacks"""

from dash import Input, Output, html, dcc
from dash.exceptions import PreventUpdate

from flask import session

import dash_mantine_components as dmc
from dash_iconify import DashIconify

from app import app, server
from model import User

import identity  # noqa: F401

from routes import api_bp


def log_button(title, icon, color, href):
    """Template button for login/logout"""
    out = dmc.Anchor(
        dmc.Button(
            title,
            id="log-icon",
            leftIcon=DashIconify(icon=icon, width=20),
            color=color,
            radius="sm",
        ),
        href=href,
        variant="text",
        style={
            "textTransform": "capitalize",
            "textDecoration": "none",
        },
        id="log",
    )
    return out


@app.callback(
    Output("button", "children"),
    [
        Input("url", "pathname"),
    ],
    prevent_initial_call=True,
)
def is_logged(nclick):
    """Dynamically change the login button properties"""
    if session.get("user_id", None) is not None:
        # user is logged in, and can log out
        return log_button(
            "Log out",
            "ion:log-out-outline",
            "red",
            "http://{}:{}/logout".format(
                server.config["PROJECT_URL"], server.config["PROJECT_PORT"]
            ),
        )
    else:
        # user is logged out, and can log in
        return log_button(
            "Log in",
            "ion:log-in-outline",
            "green",
            "http://{}:{}/login".format(
                server.config["PROJECT_URL"], server.config["PROJECT_PORT"]
            ),
        )


@app.callback(
    Output("notifications-container", "children"),
    Input("obj1", "n_clicks"),
    prevent_initial_call=True,
)
def show_status(click):
    """Notify logging status"""
    if click is not None and click > 0:
        if session.get("user_id", None) is None:
            return dmc.Notification(
                title="You need to log in",
                id="simple-notify-login",
                action="show",
                color="red",
                message="Click on the button login to log in.",
                icon=DashIconify(icon="lucid:x"),
            )
        user = User.query.filter_by(id=session["user_id"]).first()
        return dmc.Notification(
            title="Welcome {}".format(user),
            id="simple-notify-logout",
            action="show",
            color="green",
            message="You are logged in. Click on logout to log out.",
            icon=DashIconify(icon="lucid:check"),
        )
    PreventUpdate  # noqa: B018


app.layout = dmc.MantineProvider(
    dmc.NotificationsProvider(
        [
            dcc.Location(id="url", refresh=True),
            dmc.Paper(
                dmc.Center(
                    [
                        html.Div(
                            log_button(
                                "Log in",
                                "ion:log-in-outline",
                                "green",
                                "javascript:void(0);",
                            ),
                            id="button",
                        ),
                        dmc.Space(w="xl"),
                        dmc.Button(
                            "Test connection status",
                            variant="gradient",
                            gradient={"from": "grape", "to": "pink", "deg": 35},
                            radius="xl",
                            id="obj1",
                            n_clicks=0,
                        ),
                    ],
                    style={"height": 200, "width": "100%"},
                ),
                shadow="xs",
            ),
            html.Div(id="notifications-container"),
            html.Div(id="result"),
        ]
    )
)

server.register_blueprint(api_bp, url_prefix="/")


if __name__ == "__main__":
    app.run_server(
        server.config["PROJECT_URL"], port=server.config["PROJECT_PORT"], debug=True
    )
