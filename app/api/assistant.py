from fastapi import APIRouter, Depends, Request

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.dependencies.authentication import get_current_user
from app.schemas.assistant.AssistantChat import AssistantChatRequest, AssistantChatResponse
from app.services.AssistantService import chat
from app.core.rate_limiter import limiter


assistant_router = APIRouter(
    prefix="/assistant",
    tags=["Assistant"],
)

@assistant_router.post(
    "/chat",
    response_model=AssistantChatResponse,
)
@limiter.limit("20/minute")
async def assistant_chat(
    request: Request,
    query: AssistantChatRequest,
    current_user=Depends(
        get_current_user
    ),
    session: AsyncSession = Depends(
        get_db
    ),
):

    return await chat(
        question=query.question,
        current_user=current_user,
        session=session,
        session_id=query.session_id,
    )
