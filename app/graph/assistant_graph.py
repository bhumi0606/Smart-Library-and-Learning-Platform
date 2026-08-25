from langgraph.graph import END, START, StateGraph

from app.graph.router import router_node
from app.graph.state import AssistantState
from app.graph.task_execute import execute_tasks

async def task_execute_node(
    state: AssistantState,
):
    result = await execute_tasks(
        state=state,
    )
    return result

async def final_response_node(
    state: AssistantState,
):
    
    if state.get("answer"):
        return state

    return {
        **state,
        "answer": (
            "I processed your request, "
            "but I could not generate a response."
        ),
    }

def build_assistant_graph():

    graph = StateGraph(
        AssistantState,
    )

    # Nodes
    graph.add_node(
        "router",
        router_node,
    )

    graph.add_node(
        "task_executor",
        task_execute_node,
    )

    graph.add_node(
        "final_response",
        final_response_node,
    )

    # START
    graph.add_edge(
        START,
        "router",
    )

    # Router → Task Executor
    graph.add_edge(
        "router",
        "task_executor",
    )

    # Task Executor → Final Response
    graph.add_edge(
        "task_executor",
        "final_response",
    )

    # Final → END
    graph.add_edge(
        "final_response",
        END,
    )

    return graph.compile()


assistant_graph = build_assistant_graph()
