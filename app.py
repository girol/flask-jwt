from flask import Flask
from auth import verify_password, generate_token, auth_needed
from config import JWT_TOKEN_EXPIRY_SECONDS

app = Flask(__name__)


@app.route("/")
def hello_world():
    return {"message": "Hello World!"}


@app.route("/token")
def get_token():
    credentials = verify_password()
    token = generate_token(credentials["username"])
    return {
        "token": token,
        "expires_in": JWT_TOKEN_EXPIRY_SECONDS,
        "token_type": "Bearer",
    }

@app.route("/secret")
@auth_needed
def secret_page():
    return "Swordfish"
