from fastapi import Depends, FastAPI, Security
from fastapi.security import APIKeyCookie
from pydantic import BaseModel
from starlette.testclient import TestClient

app = FastAPI()

api_key = APIKeyCookie(name="key")


class User(BaseModel):
    username: str


def get_current_user(oauth_header: str = Security(api_key)):
    user = User(username=oauth_header)
    return user


@app.get("/users/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "Fast API", "version": "0.1.0"},
    "paths": {
        "/users/me": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
                "summary": "Read Current User Get",
                "operationId": "read_current_user_users_me_get",
                "security": [{"APIKeyCookie": []}],
            }
        }
    },
    "components": {
        "securitySchemes": {
            "APIKeyCookie": {"type": "apiKey", "name": "key", "in": "cookie"}
        }
    },
}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == openapi_schema


def test_security_api_key():
    response = client.get("/users/me", cookies={"key": "secret"})
    assert response.status_code == 200
    assert response.json() == {"username": "secret"}


def test_security_api_key_no_key():
    response = client.get("/users/me")
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}
