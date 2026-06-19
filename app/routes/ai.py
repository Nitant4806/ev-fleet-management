from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import (
    get_db,
)

from app.agents.agent_router import (
    route_agent,
)

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post("/ask")
def ask_ai(
    question: str,
    db: Session = Depends(get_db),
):

    return route_agent(
        db,
        question,
    )
