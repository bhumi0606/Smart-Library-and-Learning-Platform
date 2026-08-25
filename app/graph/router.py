import json

from app.core.config import settings
from app.core.openai_client import client

from app.graph.state import AssistantState

INTENT_PROMPT = """
You are the intent and task planner for a Smart Library assistant.

Analyze the user's request and identify:

1. Which library domains are involved.
2. Which concrete tasks need to be performed.
3. Whether the request requires multiple steps.

Available domains:

- book
  Book information, book content, authors, ISBN, book discovery,
  book recommendations, digital book questions, and book availability.

- loan
  Borrowing, returning, renewing, reserving books, overdue loans,
  borrowing history, and loan-related operations.

- course
  Course information, course discovery, course enrollment,
  and course-related questions.

- general
  Greetings, thanks, casual conversation, help requests,
  or anything unrelated to the library domains.

Available tasks:

- answer_general
  Use for greetings, thanks, casual conversation, or general help.

- search_book_content
  Use when the user asks about the actual CONTENT of a book or document.

  Examples:
  - "What is this book about?"
  - "Who are the main characters?"
  - "What does the book say about testing?"
  - "Explain chapter 5."
  - "Who is Joseph Lind?"
  - "What happened in the first chapter?"
  - "What are the main concepts discussed in this book?"

  IMPORTANT:
  Questions about characters, chapters, concepts, explanations,
  events, topics, summaries, or information contained inside the
  uploaded document MUST use search_book_content.

- search_books
  Use when the user wants to search/list books from the library catalog.

  Examples:
  - "Show me all Python books."
  - "Which books are available?"
  - "Find books by Robert Martin."

- get_book
  Use ONLY when the user explicitly asks for library metadata
  about a specific book and the book ID is known.

  Examples:
  - "Get book with ID 3."
  - "Show the details of book 3."

  Do NOT use get_book for questions about the content of a book.

- recommend_book
  Use when the user asks for a book recommendation.

- get_member_history
  Use when the user asks about their borrowing/loan history.

- check_book_availability
  Use when the user asks whether a specific book can currently
  be borrowed/accessed.

- borrow_book
  Use when the user explicitly wants to borrow a book.

- return_book
  Use when the user wants to return a borrowed book.

- renew_loan
  Use when the user wants to renew/extend a loan.

- reserve_book
  Use when the user wants to reserve a book.

- search_courses
  Use when the user asks to find/search/list courses.

- get_course
  Use when the user asks for details about a specific course.

- enroll_course
  Use when the user wants to enroll in a course.

Rules:

- Return only valid JSON.
- "intents" must contain one or more domains.
- "tasks" must contain the operations required to answer the request.
- Preserve the logical order of tasks.
- "is_multi_step" must be true if more than one operation is required.
- A simple question such as "Hi" should be:
  intents = ["general"]
  tasks = ["answer_general"]
  is_multi_step = false

Examples:

User:
"Hi"

Response:
{
    "intents": ["general"],
    "tasks": ["answer_general"],
    "is_multi_step": false
}


User:
"Which books cover machine learning basics?"

Response:
{
    "intents": ["book"],
    "tasks": ["search_book_content"],
    "is_multi_step": false
}


User:
"Is Clean Code available?"

Response:
{
    "intents": ["book"],
    "tasks": ["check_book_availability"],
    "is_multi_step": false
}


User:
"What books have I borrowed?"

Response:
{
    "intents": ["loan"],
    "tasks": ["get_member_history"],
    "is_multi_step": false
}

User:
"Recommend me a book."

Response:
{
    "intents": ["book", "loan"],
    "tasks": [
        "get_member_history",
        "search_books",
        "recommend_book"
    ],
    "is_multi_step": true
}


User:
"Recommend a book based on my borrowing history and reserve it
if it is available."

Response:
{
    "intents": ["loan", "book"],
    "tasks": [
        "get_member_history",
        "recommend_book",
        "check_book_availability",
        "reserve_book"
    ],
    "is_multi_step": true
}


User:
"Tell me what Clean Code says about testing and whether it is available."

Response:
{
    "intents": ["book"],
    "tasks": [
        "search_book_content",
        "check_book_availability"
    ],
    "is_multi_step": true
}


User:
"What courses are available and enroll me in Python if possible?"

Response:
{
    "intents": ["course"],
    "tasks": [
        "search_courses",
        "enroll_course"
    ],
    "is_multi_step": true
}


User:
"Thanks!"

Response:
{
    "intents": ["general"],
    "tasks": ["answer_general"],
    "is_multi_step": false
}


User request:
"""


ALLOWED_INTENTS = {
    "book",
    "loan",
    "course",
    "general",
}


ALLOWED_TASKS = {
    "answer_general",
    "search_book_content",
    "search_books",
    "get_book",
    "recommend_book",
    "get_member_history",
    "check_book_availability",
    "borrow_book",
    "return_book",
    "renew_loan",
    "reserve_book",
    "search_courses",
    "get_course",
    "enroll_course",
}


def detect_intent(
    question: str,
):
    if not question or not question.strip():
        return {
            "intents": ["general"],
            "tasks": ["answer_general"],
            "is_multi_step": False,
        }

    normalized_question = question.lower().strip()

    recommendation_keywords = [
        "recommend a book",
        "recommend me a book",
        "recommend books",
        "book recommendation",
        "recommendation",
        "suggest a book",
        "suggest me a book",
        "which book should i read",
        "what book should i read",
        "what should i read",
    ]

    if any(
        keyword in normalized_question
        for keyword in recommendation_keywords
    ):
        return {
            "intents": ["book"],
            "tasks": ["recommend_book"],
            "is_multi_step": False,
        }

    response = client.chat.completions.create(
        model=settings.OPENAI_CHAT_MODEL,
        messages=[
            {
                "role": "system",
                "content": INTENT_PROMPT,
            },
            {
                "role": "user",
                "content": question,
            },
        ],
    )

    content = (
        response.choices[0]
        .message
        .content
        .strip()
    )

    try:
        result = json.loads(content)

    except json.JSONDecodeError:
        return {
            "intents": ["general"],
            "tasks": ["answer_general"],
            "is_multi_step": False,
        }

    intents = result.get(
        "intents",
        [],
    )

    tasks = result.get(
        "tasks",
        [],
    )

    intents = [
        intent
        for intent in intents
        if intent in ALLOWED_INTENTS
    ]

    tasks = [
        task
        for task in tasks
        if task in ALLOWED_TASKS
    ]

    if not intents:
        intents = ["general"]

    if not tasks:
        tasks = ["answer_general"]

    return {
        "intents": intents,
        "tasks": tasks,
        "is_multi_step": len(tasks) > 1,
    }

def router_node(
    state: AssistantState,
):
    question = state.get("question", "").strip().lower()

    if any( 
        phrase in question 
        for phrase in [
            "return my book", 
            "return the book", 
            "i want to return", 
            "return a book", 
            "give back my book", 
            "give back the book", 
        ] 
    ): 
        return { 
            **state, 
            "intents": ["loan", "book"], 
            "tasks": [ "get_member_history", "return_book", ], 
            "is_multi_step": True,
        }

    if any(
        phrase in question
        for phrase in [
            "renew my book",
            "renew the book",
            "renew a book",
            "renew book",
            "renew my loan",
            "renew the loan",
            "extend my loan",
            "extend the loan",
        ]
    ):
        return {
            **state,
            "intents": ["loan"],
            "tasks": [
                "get_member_history",
                "renew_loan",
            ],
            "is_multi_step": True,
        }
    
    if any(
        phrase in question
        for phrase in [
            "return my book",
            "return the book",
            "i want to return",
            "return a book",
            "give back my book",
            "give back the book",
        ]
    ):
        return {
            **state,
            "intents": ["loan", "book"],
            "tasks": [
                "get_member_history",
                "return_book",
            ],
            "is_multi_step": True,
        }

    if any(
        phrase in question
        for phrase in [
            "recommend me a book",
            "recommend a book",
            "book recommendation",
            "recommend book",
            "suggest a book",
            "suggest me a book",
        ]
    ):
        return {
            **state,
            "intents": ["book", "loan"],
            "tasks": [
                "get_member_history",
                "search_books",
                "recommend_book",
            ],
            "is_multi_step": True,
        }

    result = detect_intent(
        question=question,
    )

    return {
        **state,
        "intents": result["intents"],
        "tasks": result["tasks"],
        "is_multi_step": result["is_multi_step"],
    }