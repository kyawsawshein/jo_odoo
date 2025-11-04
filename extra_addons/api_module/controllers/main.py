import jwt
import logging
from odoo import _, http  # type: ignore
from odoo.exceptions import ValidationError
from odoo.http import request  # type: ignore

from .auth_route import AuthRoute


_logger = logging.getLogger(__name__)


class JwtAuthController(http.Controller):

    @http.route(AuthRoute.jwt_login, type="json", auth="none", csrf=False)
    # pylint: disable=no-self-use
    def jwt_login(self, **params):
        _logger.info(f"#====== params {params}")
        # In Odoo 19, authenticate takes only login and password
        # The database is already available in the request context
        uid = request.session.authenticate(params.get("login"), params.get("password"))
        config = (
            request.env["api.config"]
            .sudo()
            .search([("active", "=", True), ("enable_jwt_auth", "=", True)], limit=1)
        )
        _logger.info(f"#===== uid , {uid}, {config}")
        return [{"token": config.generate_token(uid=uid)}]

    # pylint: disable=too-many-arguments,no-self-use
    @http.route(
        AuthRoute.jwt_call,
        type="json",
        auth="none",
        csrf=False,
    )
    def jwt_call(self, model=None, function=None, token=None, args=None, kwargs=None):
        if not token:
            raise ValidationError(_("Missing token"))
        try:
            config = request.env["api.config"]
            payload = config.decode_token(token=token)
            env = request.env(user=payload.get("uid"))
            model_obj = env[model]
            func = getattr(model_obj, function, None)  # type: ignore
            return func(*(args or []), **(kwargs or {}))
        except jwt.ExpiredSignatureError as sig_err:
            raise jwt.ExpiredSignatureError("Token has expired") from sig_err
        except jwt.InvalidTokenError as token_err:
            raise jwt.InvalidTokenError("Invalid token") from token_err
