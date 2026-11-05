from fastapi import Depends, FastAPI

def wire_board_dependencies(app: FastAPI) -> None:
    app.dependency_overrides.update(
        {
            
        }
    )