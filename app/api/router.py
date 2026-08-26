from fastapi import APIRouter

from app.api.authentication import auth_router
from app.api.books import book_router
from app.api.members import member_router
from app.api.authors import author_router
from app.api.book_authors import book_author_router
from app.api.courses import course_router
from app.api.enrollments import enrollment_router
from app.api.loans import loan_router
from app.api.assistant import assistant_router
from app.api.book_document import book_document_router
from app.api.reservations import reservation_router

api_router = APIRouter(
    prefix="/api",
)

api_router.include_router(auth_router)
api_router.include_router(book_router)
api_router.include_router(member_router)
api_router.include_router(author_router)
api_router.include_router(book_author_router)
api_router.include_router(course_router)
api_router.include_router(enrollment_router)
api_router.include_router(loan_router)
api_router.include_router(assistant_router)
api_router.include_router(book_document_router)
api_router.include_router(reservation_router)