from fastapi import FastAPI
from wiring.auth import wire_auth_dependencies
from wiring.user import wire_user_dependencies

# FastAPI Dependency Overrides 와이어링
def wire_dependencies(app: FastAPI) -> None:
    wire_user_dependencies(app)
    wire_auth_dependencies(app)