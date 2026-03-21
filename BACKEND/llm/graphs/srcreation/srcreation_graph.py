from typing import TypedDict
from langgraph.graph import StateGraph,END
from schemas.system.system_schema import MessageSchema
from llm.chains.srcreation.srcreation_chain import SRCreationChain
from langchain_core.runnables import RunnableConfig
from schemas.srcreation.classification_result_schema import ClassificationState
from db.services.prompt_key_dependency_service import PromptKeyDependencyService
from core.enums import PromptkeyDependency
from llm.utils.InMemoryMessasageUtil import InMemoryCache




def service_and_request_classification_node(state: ClassificationState, config: RunnableConfig):
    thread_id = config["configurable"].get("thread_id")

    # Create an instance of the SRCreationChain
    sr_chain = SRCreationChain(max_retries=state.max_retries)
    # Call the method
    state.llm_response_dets = None

    result = sr_chain.run(
        thread_id=thread_id,
        request=state.request,
        services="",
        typesofrequests=state.typesofrequests,
        state = state
        
    )

    # Update state with classification
    state.classification = result

    # Update workflow flags
    if result.clarification_question:
        state.needs_clarification = True
        state.clarification_question = result.clarification_question
        state.is_request_complete = False
        state.retry_count += 1
    else:
        state.needs_clarification = False
        state.is_request_complete = True
    state.classification = result
    state.service = result.service
    state.request_type = result.request_type
    state.confidence = result.confidence
    state.needs_clarification = result.clarification_question is not None
    state.clarification_question = result.clarification_question
    state.is_request_complete =  (
    state.service is not None and
    state.request_type is not None
)
    state.llm_response_dets = result.llm_response_dets

        # ✅ 8. Load final messages
    if state.llm_response_dets :
        if state.llm_response_dets.content:
            InMemoryCache.save_message(
            thread_id=thread_id,
            role="assistant",
            content=state.llm_response_dets.content,
            tokens=state.llm_response_dets.usage.total_tokens,
            state= state
        )
        conversation = InMemoryCache.load_messages(thread_id)
        state.llm_response_dets. messages = [MessageSchema(**msg) for msg in conversation]


    return state

def extract_necessary_details_node(state: ClassificationState, config: RunnableConfig):
    thread_id = config["configurable"].get("thread_id")

    sr_chain = SRCreationChain(max_retries=state.max_retries)
        # Call the method
    
    result = sr_chain.run_mandatory_fields(
           
            state = state, thread_id = thread_id

        )
    state.needs_clarification = result.clarification_question is not None
    state.clarification_question = result.clarification_question
    state.is_mandatory_fields_complete = not state.needs_clarification
    state.llm_response_dets = result.llm_response_dets
    if state.llm_response_dets :
        if state.llm_response_dets.content:
            InMemoryCache.save_message(
            thread_id=thread_id,
            role="assistant",
            content=state.llm_response_dets.content,
            tokens=state.llm_response_dets.usage.total_tokens,
            state= state
        )
        conversation = InMemoryCache.load_messages(thread_id)
        state.llm_response_dets. messages = [MessageSchema(**msg) for msg in conversation]
    return state
def route_after_classification(state: ClassificationState):
    if state.is_request_complete:
        return "extract_necessary_details_node"  # Go to Node 2 immediately
    return "end"  # Otherwise, return to client

def build_graph():
    graph = StateGraph(ClassificationState)

    # Node 1: Classification
    graph.add_node(
        "service_and_request_classification_node",
        service_and_request_classification_node
    )

    # Node 2: Extract details
    graph.add_node(
        "extract_necessary_details_node",
        extract_necessary_details_node
    )

    # Entry
    graph.set_entry_point("service_and_request_classification_node")

    # Conditional routing
    graph.add_conditional_edges(
        "service_and_request_classification_node",
        route_after_classification,
        {
            "extract_necessary_details_node": "extract_necessary_details_node",
            "end": END  # Stop and return to client
        }
    )

    # Node 2 always ends after execution
    graph.add_edge("extract_necessary_details_node", END)

    return graph.compile()