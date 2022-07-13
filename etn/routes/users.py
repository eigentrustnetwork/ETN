from etn.database import DatabaseManager
from etn.helpers import get_params
from flask import Response, request
from werkzeug.datastructures import Headers
import hashlib


def verify_credentials():
    """
    Used to verify ETN user credentials for website login, or other purposes.

    Message Structure:
    {
        "username": str
        "password": str
    }
    Returns:
    403: Username or Password is incorrect.
    200: Success.
    """

    # Set CORS headers.
    headers = Headers()
    headers.add("Access-Control-Allow-Origin", "http://www.eigentrust.net")
    headers.add("Access-Control-Allow-Headers", "Content-type")
    headers.add("Vary", "Origin")
    if(request.method == "OPTIONS"):
        return Response(status=200, headers=headers)

    username, password = get_params(["username", "password"])

    with DatabaseManager() as db:
        result = db.execute("SELECT * FROM users WHERE username=:username", {"username": username})
        user = result.fetchone()
        if not user:
            return Response("Username or Password is incorrect.", 403, headers)

        salt = user["salt"]
        sha512 = hashlib.new("sha512")
        sha512.update(f"{password}:{salt}".encode("utf8"))
        password_hash = sha512.hexdigest()
        if not password_hash == user["password"]:
            return Response("Username or Password is incorrect.", 403, headers)

        return Response("Success.", 200, headers)
