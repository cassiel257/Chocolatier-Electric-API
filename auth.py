import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen

# TODO:Update and export these variables
AUTH0_DOMAIN = "sparkle-coffee.us.auth0.com"
ALGORITHMS = ["RS256"]
API_AUDIENCE = "chocolate"

# Define Auth Error


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Get Authorization Header
def get_token_auth_header():
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError(
            {
                "code": "authorization_header_missing",
                "description": "Authorization header is missing.",
            },
            401,
        )

    header_parts = auth.split()
    if header_parts[0].lower() != "bearer":
        raise AuthError(
            {
                "code": "invalid_header",
                "description": 'Authorization header should begin with "Bearer".',  # noqa
            },
            401,
        )

    elif len(header_parts) == 1:
        raise AuthError(
            {"code": "invalid_header", "description": "No token found."}, 401
        )

    elif len(header_parts) > 2:
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Malformed authorization header.",
            },
            401,
        )

    token = header_parts[1]
    return token


# Check Permissions
def check_permissions(permission, payload):
    if payload.get("permissions"):
        token_info = payload.get("permissions")
        if permission not in token_info:

            raise AuthError(
                {
                    "code": "invalid_claims",
                    "description": "Permissions not included in JWT.",
                },
                401,
            )
        else:
            return True

    else:
        raise AuthError(
            {"code": "unauthorized",
                "description": "Permission not found."}, 403
        )


# Decode JWT
def verify_decode_jwt(token):
    myurl = "https://%s/.well-known/jwks.json" % (AUTH0_DOMAIN)
    jsonurl = urlopen(myurl)
    content = jsonurl.read().decode(jsonurl.headers.get_content_charset())
    jwks = json.loads(content)
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if "kid" not in unverified_header:
        raise AuthError(
            {"code": "invalid_header",
                "description": "Authorization malformed."}, 401
        )

    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer="https://" + AUTH0_DOMAIN + "/",
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError(
                {"code": "token_expired", "description": "Token expired."}, 401
            )

        except jwt.JWTClaimsError:
            raise AuthError(
                {
                    "code": "invalid_claims",
                    "description": "Incorrect claims. Please, check the audience and issuer.",  # noqa
                },
                401,
            )
        except Exception:
            raise AuthError(
                {
                    "code": "invalid_header",
                    "description": "Unable to parse authentication token.",
                },
                400,
            )
    raise AuthError(
        {
            "code": "invalid_header",
            "description": "Unable to find the appropriate key.",
        },
        400,
    )


# Requires Auth Method
def requires_auth(permission=""):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
                check_permissions(permission, payload)
            except:  # noqa
                abort(401)
            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
