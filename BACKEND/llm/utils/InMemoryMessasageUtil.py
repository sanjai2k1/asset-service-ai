import uuid
from typing import Dict, List, Any, Optional
from langchain_core.messages import HumanMessage, AIMessage


class InMemoryCache:
    _store: Dict[str, Dict[str, Any]] = {}

    @staticmethod
    def create_thread_id() -> str:
        return str(uuid.uuid4())

    @classmethod
    def _get_thread(cls, thread_id: str) -> Dict[str, Any]:
        if thread_id not in cls._store:
            cls._store[thread_id] = {
                "messages": [],
                "user_req": [],
                "state": None
            }
        return cls._store[thread_id]

    # -------------------------------
    # SAVE MESSAGE
    # -------------------------------
    @classmethod
    def save_message(
        cls,
        thread_id: str,
        role: str,
        content: str,
        tokens: int = 0,
        user_req: Optional[str] = None,
        state: Optional[Any] = None,
    ):
        thread = cls._get_thread(thread_id)

        msg = HumanMessage(content=content) if role == "user" else AIMessage(content=content)
        msg.additional_kwargs["tokens"] = tokens

        thread["messages"].append(msg)

        if user_req:
            thread["user_req"].append(user_req)

        if state is not None:
            thread["state"] = state

        return {
            "role": role,
            "content": content,
            "tokens": tokens
        }

    # -------------------------------
    # LOAD MESSAGES (DICT FORMAT)
    # -------------------------------
    @classmethod
    def load_messages(cls, thread_id: str) -> List[Dict]:
        thread = cls._get_thread(thread_id)

        result = []
        for msg in thread["messages"]:
            role = "user" if isinstance(msg, HumanMessage) else "assistant"
            result.append({
                "role": role,
                "content": msg.content,
                "tokens": msg.additional_kwargs.get("tokens", 0)
            })
        return result

    # -------------------------------
    # LOAD LC MESSAGES (RAW)
    # -------------------------------
    @classmethod
    def load_lc_messages(cls, thread_id: str):
        thread = cls._get_thread(thread_id)
        return thread["messages"]

    # -------------------------------
    # GET STATE
    # -------------------------------
    @classmethod
    def get_state(
        cls,
        thread_id: str,
        state_cls=None,
        **kwargs
    ):
        thread = cls._get_thread(thread_id)
        state = thread.get("state")
    
        # 🔹 No state exists → create new
        if state is None:
            if state_cls is None:
                return None
            state = state_cls(**kwargs)
            thread["state"] = state
            return state
    
        # 🔹 If stored as dict → rebuild object
        if isinstance(state, dict) and state_cls:
            state = state_cls(**state)
            thread["state"] = state
    
        # 🔹 Override runtime values
        for key, value in kwargs.items():
            setattr(state, key, value)
    
        return state
    @classmethod
    def get_config(cls,thread_id: str):
        return {
            "configurable": {
                "thread_id": thread_id
            }
        }
    # -------------------------------
    # SET STATE
    # -------------------------------
    @classmethod
    def set_state(cls, thread_id: str, state: Any):
        thread = cls._get_thread(thread_id)
        thread["state"] = state

    # -------------------------------
    # USER REQS
    # -------------------------------
    @classmethod
    def get_user_reqs(cls, thread_id: str) -> List[str]:
        thread = cls._get_thread(thread_id)
        return thread.get("user_req", [])

    # -------------------------------
    # DEBUG
    # -------------------------------
    @classmethod
    def debug(cls, thread_id: str):
        thread = cls._get_thread(thread_id)
        print("Messages:", len(thread["messages"]))
        print("User reqs:", thread["user_req"])
        print("State:", thread["state"])