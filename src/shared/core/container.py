from fastapi import FastAPI, Depends
from database import get_db

def wire_dependencies(app: FastAPI) -> None:
    # app.dependency_overrides
    pass
