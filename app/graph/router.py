import json

from app.core.config import settings
from app.core.openai_client import client
from app.graph.state import AssistantState


# TASK DEFINITIONS
TASK_DESCRIPTIONS = {

    "answer_general":
        "Answer greetings, thanks, casual conversation, "
        "or general library-related questions.",

    "search_book_content":
        "Search the actual uploaded/document content of books. "
        "Use this when the user asks about chapters, explanations, "
        "concepts, summaries, characters, or what a book says.",

    "search_books":
        "Search the library catalog for books using title, author, "
        "ISBN, availability/status, or a general catalog query.",

    "get_book":
        "Get detailed information about a specific book.",

    "recommend_book":
        "Recommend books based on the user's interests, request, "
        "or borrowing history.",

    "get_member_history":
        "Get the current member's borrowing history and active loans.",

    "check_book_availability":
        "Check whether a specific book is currently available.",

    "borrow_book":
        "Borrow, check out, or issue a book to the current member.",

    "return_book":
        "Return a book that the current member has borrowed.",

    "renew_loan":
        "Renew or extend an existing active loan.",

    "reserve_book":
        "Reserve or hold a book for the current member.",

    "search_courses":
        "Search the course catalog.",

    "get_course":
        "Get details about a specific course.",

    "enroll_course":
        "Enroll the current member in a course.",
}


ALLOWED_INTENTS = {
    "book",
    "loan",
    "course",
    "reservation",
    "general",
}


ALLOWED_TASKS = set(
    TASK_DESCRIPTIONS.keys()
)

# BUILD TASK DESCRIPTION
def _build_task_descriptions() -> str:

    return "\n".join(
        f"- {task}: {description}"
        for task, description
        in TASK_DESCRIPTIONS.items()
    )

# PLANNER PROMPT
def _build_intent_prompt() -> str:

    tasks = _build_task_descriptions()

    return f"""
You are the planning agent for a production Smart Library
and Learning Platform.

Your job is ONLY to understand the user's request and create
a structured execution plan.

You DO NOT execute database operations.

You DO NOT answer the user.

You ONLY decide:

1. What intent the user has.
2. Which tasks need to be executed.
3. The correct order of those tasks.
4. The arguments required by each task.

============================================================
AVAILABLE TASKS
============================================================

{tasks}


============================================================
IMPORTANT RULES
============================================================

1. Understand the COMPLETE meaning of the user's request.

2. DO NOT use keyword matching.

3. The user may express the same operation in many different ways.

4. Never require exact words such as:
   - borrow
   - return
   - renew
   - reserve
   - available

5. Infer the operation semantically.

6. Only select tasks from the available task list.

7. Never invent a task.

8. If multiple tasks are required, return them in the correct
   execution order.

9. Extract useful entities from the user's request.

10. Do not invent database IDs.

11. If the user gives a book title, put it into task arguments.

12. If the user gives a book ID, put it into task arguments.

13. If the user gives an author, put it into task arguments.

14. If the user asks for available books, use:
    status = "available"

15. If the user asks for borrowed/unavailable books, use:
    status = "borrowed"

16. Database state must always be determined by application
    code, not by the LLM.

17. Do not silently convert unsupported operations into supported
    operations.

18. Return ONLY valid JSON.

============================================================
TASK ARGUMENTS
============================================================

For search_books, supported arguments are:

{{
    "title": string | null,
    "author": string | null,
    "status": "available" | "borrowed" | "lost" | "damaged" | null,
    "query": string | null,
    "page": integer,
    "limit": integer
}}

For tasks such as:

check_book_availability
borrow_book
return_book
renew_loan
reserve_book
get_book

you may provide:

{{
    "book_id": integer | null,
    "book_title": string | null
}}

Do not invent book IDs.

============================================================
EXAMPLES
============================================================


USER:
"Which books are available?"

PLAN:
{{
    "intents": ["book"],
    "tasks": ["search_books"],
    "task_arguments": {{
        "search_books": {{
            "title": null,
            "author": null,
            "status": "available",
            "query": null,
            "page": 1,
            "limit": 100
        }}
    }},
    "is_multi_step": false
}}


USER:
"What books can I borrow right now?"

PLAN:
{{
    "intents": ["book", "loan"],
    "tasks": ["search_books"],
    "task_arguments": {{
        "search_books": {{
            "title": null,
            "author": null,
            "status": "available",
            "query": null,
            "page": 1,
            "limit": 100
        }}
    }},
    "is_multi_step": false
}}


USER:
"Do you have Clean Code?"

PLAN:
{{
    "intents": ["book"],
    "tasks": ["search_books"],
    "task_arguments": {{
        "search_books": {{
            "title": "Clean Code",
            "author": null,
            "status": null,
            "query": null,
            "page": 1,
            "limit": 100
        }}
    }},
    "is_multi_step": false
}}


USER:
"Can I borrow Clean Code?"

PLAN:
{{
    "intents": ["book", "loan"],
    "tasks": [
        "search_books",
        "check_book_availability",
        "borrow_book"
    ],
    "task_arguments": {{
        "search_books": {{
            "title": "Clean Code",
            "author": null,
            "status": null,
            "query": null,
            "page": 1,
            "limit": 100
        }},
        "check_book_availability": {{
            "book_title": "Clean Code",
            "book_id": null
        }},
        "borrow_book": {{
            "book_title": "Clean Code",
            "book_id": null
        }}
    }},
    "is_multi_step": true
}}


USER:
"I need to give Clean Code back."

PLAN:
{{
    "intents": ["loan", "book"],
    "tasks": [
        "get_member_history",
        "return_book"
    ],
    "task_arguments": {{
        "get_member_history": {{}},
        "return_book": {{
            "book_title": "Clean Code",
            "book_id": null
        }}
    }},
    "is_multi_step": true
}}


USER:
"Can I keep Clean Code for another two weeks?"

PLAN:
{{
    "intents": ["loan"],
    "tasks": [
        "get_member_history",
        "renew_loan"
    ],
    "task_arguments": {{
        "get_member_history": {{}},
        "renew_loan": {{
            "book_title": "Clean Code",
            "book_id": null
        }}
    }},
    "is_multi_step": true
}}


USER:
"Can you hold Clean Code for me?"

PLAN:
{{
    "intents": ["book", "reservation"],
    "tasks": [
        "search_books",
        "check_book_availability",
        "reserve_book"
    ],
    "task_arguments": {{
        "search_books": {{
            "title": "Clean Code",
            "author": null,
            "status": null,
            "query": null,
            "page": 1,
            "limit": 100
        }},
        "check_book_availability": {{
            "book_title": "Clean Code",
            "book_id": null
        }},
        "reserve_book": {{
            "book_title": "Clean Code",
            "book_id": null
        }}
    }},
    "is_multi_step": true
}}


USER:
"Recommend something based on what I have borrowed."

PLAN:
{{
    "intents": ["book", "loan"],
    "tasks": [
        "get_member_history",
        "search_books",
        "recommend_book"
    ],
    "task_arguments": {{
        "get_member_history": {{}},
        "search_books": {{
            "title": null,
            "author": null,
            "status": null,
            "query": null,
            "page": 1,
            "limit": 100
        }},
        "recommend_book": {{}}
    }},
    "is_multi_step": true
}}


USER:
"Find a Python course and sign me up."

PLAN:
{{
    "intents": ["course"],
    "tasks": [
        "search_courses",
        "enroll_course"
    ],
    "task_arguments": {{
        "search_courses": {{
            "query": "Python"
        }},
        "enroll_course": {{}}
    }},
    "is_multi_step": true
}}


USER:
"Hi"

PLAN:
{{
    "intents": ["general"],
    "tasks": ["answer_general"],
    "task_arguments": {{
        "answer_general": {{}}
    }},
    "is_multi_step": false
}}


USER:
"Which books cover machine learning basics?"

PLAN:
{{
    "intents": ["book"],
    "tasks": ["search_books"],
    "task_arguments": {{
        "search_books": {{
            "title": null,
            "author": null,
            "status": null,
            "query": "machine learning basics",
            "page": 1,
            "limit": 100
        }}
    }},
    "is_multi_step": false
}}


============================================================
FINAL REQUIREMENT
============================================================

Return ONLY JSON.

Format:

{{
    "intents": ["book"],
    "tasks": ["search_books"],
    "task_arguments": {{
        "search_books": {{
            "query": "machine learning"
        }}
    }},
    "is_multi_step": false
}}
"""

# FALLBACK
def _fallback_plan() -> dict:

    return {
        "intents": ["general"],
        "tasks": ["answer_general"],
        "task_arguments": {
            "answer_general": {}
        },
        "is_multi_step": False,
    }


# VALIDATION
def _validate_plan(result: dict) -> dict:

    if not isinstance(result, dict):
        return _fallback_plan()

    intents = result.get(
        "intents",
        [],
    )

    tasks = result.get(
        "tasks",
        [],
    )

    task_arguments = result.get(
        "task_arguments",
        {},
    )

    if not isinstance(intents, list):
        intents = []

    if not isinstance(tasks, list):
        tasks = []

    if not isinstance(task_arguments, dict):
        task_arguments = {}

    intents = [
        intent
        for intent in intents
        if isinstance(intent, str)
        and intent in ALLOWED_INTENTS
    ]

    tasks = [
        task
        for task in tasks
        if isinstance(task, str)
        and task in ALLOWED_TASKS
    ]

    if not intents:
        intents = ["general"]

    if not tasks:
        tasks = ["answer_general"]

    clean_arguments = {}

    for task in tasks:

        arguments = task_arguments.get(
            task,
            {},
        )

        if not isinstance(arguments, dict):
            arguments = {}

        clean_arguments[task] = arguments

    return {
        "intents": intents,
        "tasks": tasks,
        "task_arguments": clean_arguments,
        "is_multi_step": len(tasks) > 1,
    }


# DETECT PLAN
def detect_intent(
    question: str,
):

    response = client.chat.completions.create(
        model=settings.OPENAI_CHAT_MODEL,
        messages=[
            {
                "role": "system",
                "content": _build_intent_prompt(),
            },
            {
                "role": "user",
                "content": question,
            },
        ],
    )

    content = (
        response
        .choices[0]
        .message
        .content
        .strip()
    )

    # Remove markdown JSON fences
    if content.startswith("```"):

        content = content.replace(
            "```json",
            "",
        )

        content = content.replace(
            "```",
            "",
        )

        content = content.strip()

    # Parse JSON
    try:

        result = json.loads(
            content
        )

    except json.JSONDecodeError:

        return _fallback_plan()

    return _validate_plan(
        result
    )

# LANGGRAPH ROUTER NODE
def router_node(
    state: AssistantState,
):

    question = state.get(
        "question",
        "",
    ).strip()

    if not question:

        return {
            **state,
            "intents": ["general"],
            "tasks": ["answer_general"],
            "task_arguments": {
                "answer_general": {}
            },
            "is_multi_step": False,
        }

    plan = detect_intent(
        question=question,
    )

    return {
        **state,

        "intents": plan[
            "intents"
        ],

        "tasks": plan[
            "tasks"
        ],

        "task_arguments": plan[
            "task_arguments"
        ],

        "is_multi_step": plan[
            "is_multi_step"
        ],
    }