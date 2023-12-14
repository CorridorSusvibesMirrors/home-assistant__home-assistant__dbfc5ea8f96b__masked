"""HTTP views handle login flow.

# GET /auth/providers

Return a list of auth providers. Example:

[
    {
        "name": "Local",
        "id": null,
        "type": "local_provider",
    }
]


# POST /auth/login_flow

Create a login flow. Will return the first step of the flow.

Pass in parameter 'client_id' and 'redirect_url' validate by indieauth.

Pass in parameter 'handler' to specify the auth provider to use. Auth providers
are identified by type and id.

And optional parameter 'type' has to set as 'link_user' if login flow used for
link credential to exist user. Default 'type' is 'authorize'.

{
    "client_id": "https://hassbian.local:8123/",
    "handler": ["local_provider", null],
    "redirect_url": "https://hassbian.local:8123/",
    "type': "authorize"
}

Return value will be a step in a data entry flow. See the docs for data entry
flow for details.

{
    "data_schema": [
        {"name": "username", "type": "string"},
        {"name": "password", "type": "string"}
    ],
    "errors": {},
    "flow_id": "8f7e42faab604bcab7ac43c44ca34d58",
    "handler": ["insecure_example", null],
    "step_id": "init",
    "type": "form"
}


# POST /auth/login_flow/{flow_id}

Progress the flow. Most flows will be 1 page, but could optionally add extra
login challenges, like TFA. Once the flow has finished, the returned step will
have type FlowResultType.CREATE_ENTRY and "result" key will contain an authorization code.
The authorization code associated with an authorized user by default, it will
associate with an credential if "type" set to "link_user" in
"/auth/login_flow"

{
    "flow_id": "8f7e42faab604bcab7ac43c44ca34d58",
    "handler": ["insecure_example", null],
    "result": "411ee2f916e648d691e937ae9344681e",
    "title": "Example",
    "type": "create_entry",
    "version": 1
}
"""
from __future__ import annotations

from collections.abc import Callable

from aiohttp import web

from homeassistant.auth.models import Credentials
from homeassistant.components.http.view import HomeAssistantView
from homeassistant.core import HomeAssistant

if TYPE_CHECKING:
    from . import StoreResultType


async def async_setup(
    hass: HomeAssistant, store_result: Callable[[str, Credentials], str]
) -> None:
    """Component to allow users to login."""
    hass.http.register_view(WellKnownOAuthInfoView)


class WellKnownOAuthInfoView(HomeAssistantView):
    """View to host the OAuth2 information."""

    requires_auth = False
    url = "/.well-known/oauth-authorization-server"
    name = "well-known/oauth-authorization-server"

    async def get(self, request: web.Request) -> web.Response:
        """Return the well known OAuth2 authorization info."""
        return self.json(
            {
                "authorization_endpoint": "/auth/authorize",
                "token_endpoint": "/auth/token",
                "revocation_endpoint": "/auth/revoke",
                "response_types_supported": ["code"],
                "service_documentation": (
                    "https://developers.home-assistant.io/docs/auth_api"
                ),
            }
        )









