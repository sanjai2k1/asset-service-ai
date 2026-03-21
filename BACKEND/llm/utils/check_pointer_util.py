import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage
import schemas.srcreation.classification_result_schema as sr_schemas
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer

allowed = [
    (sr_schemas.__name__, "ClassificationResult"),
    (sr_schemas.__name__, "LLMResponseDetails"),
    (sr_schemas.__name__, "ClassificationState"),

]

# class CheckpointUtil:
#     _checkpointer = MemorySaver(
# serde=JsonPlusSerializer(allowed_msgpack_modules=allowed)

#     )
#     _namespace = "default" 

#     @staticmethod
#     def create_thread_id() -> str:
#         return str(uuid.uuid4())

#     @staticmethod
#     def get_config(thread_id: str):
#         return {
#             "configurable": {
#                 "thread_id": thread_id,
#                 "checkpoint_ns": CheckpointUtil._namespace,
#             "checkpoint_id": thread_id   # ✅ ADD THIS (MANDATORY)

#             }
#         }
#     @classmethod
#     def save_message(cls, thread_id: str, role: str, content: str, tokens: int):
#         base_config = cls.get_config(thread_id)
#         checkpoint_id = str(uuid.uuid4())
    
#         # 1. Load existing history as dicts
#         full_history_dicts = cls.load_thread(thread_id)
    
#         # 2. Convert dicts back to Message Objects to preserve history in the NEW checkpoint
#         existing_messages = []
#         for m in full_history_dicts:
#             if m["role"] == "user":
#                 msg = HumanMessage(content=m["content"])
#             else:
#                 msg = AIMessage(content=m["content"])
#             msg.additional_kwargs["tokens"] = m.get("tokens", 0)
#             existing_messages.append(msg)
    
#         # 3. Initialize the checkpoint WITH the existing messages
#         initial_checkpoint = {
#             "v": 1,
#             "id": checkpoint_id,
#             "ts": datetime.now(timezone.utc).isoformat(),
#             "channel_values": {
#                 "messages": existing_messages  # <--- CRITICAL: Add history here
#             },
#             "channel_versions": {},
#             "versions_seen": {},
#             "pending_sends": []
#         }
    
#         # 4. Put the checkpoint
#         cls._checkpointer.put(
#             base_config, 
#             initial_checkpoint,
#             metadata={"source": "manual_init"},
#             new_versions={}
#         )
    
#         # 5. Prepare the specific new message object
#         if role == "user":
#             new_msg = HumanMessage(content=content)
#         else:
#             new_msg = AIMessage(content=content)
        
#         new_msg.additional_kwargs["tokens"] = tokens
    
#         # 6. Perform the write
#         write_config = {
#             "configurable": {
#                 **base_config["configurable"],
#                 "checkpoint_id": checkpoint_id
#             }
#         }
    
#         cls._checkpointer.put_writes(
#             write_config,
#             [("messages", [new_msg])],
#             task_id=str(uuid.uuid4()),
#         )
    
#         print(f"WRITE SUCCESS. Total messages now: {len(existing_messages) + 1}")
#         return {"role": role, "content": content, "tokens": tokens}
    
#     @classmethod
#     def load_thread(cls, thread_id: str) -> List[Dict[str, Any]]:
#         print(f"Loading thread: {thread_id}")

#         search_config = {"configurable": {"thread_id": thread_id}}
#         checkpoints = list(cls._checkpointer.list(search_config))

#         if not checkpoints:
#             print("No checkpoints found.")
#             return []

#         all_messages = []

#         # ✅ Iterate through ALL checkpoints (old → new)
#         for cp_tuple in reversed(checkpoints):   # reverse = correct order

#             checkpoint = cp_tuple.checkpoint

#             # 1. committed messages
#             if "channel_values" in checkpoint and "messages" in checkpoint["channel_values"]:
#                 msgs = checkpoint["channel_values"]["messages"]
#                 if isinstance(msgs, list):
#                     all_messages.extend(msgs)
#                 else:
#                     all_messages.append(msgs)

#             # 2. pending writes
#             for write in cp_tuple.pending_writes:
#                 try:
#                     if len(write) == 3:
#                         _, channel, value = write
#                     elif len(write) == 2:
#                         channel, value = write
#                     else:
#                         continue

#                     if channel == "messages":
#                         if isinstance(value, list):
#                             all_messages.extend(value)
#                         else:
#                             all_messages.append(value)

#                 except Exception as e:
#                     print("⚠️ Skipping bad write:", write, e)

#         # ✅ Remove duplicates (important)
#         seen = set()
#         unique_messages = []
#         for m in all_messages:
#             if id(m) not in seen:
#                 seen.add(id(m))
#                 unique_messages.append(m)

#         # ✅ Convert to dict format
#         result = []
#         for m in unique_messages:
#             if isinstance(m, HumanMessage):
#                 role = "user"
#                 content = m.content
#                 tokens = m.additional_kwargs.get("tokens", 0)

#             elif isinstance(m, AIMessage):
#                 role = "assistant"
#                 content = m.content
#                 tokens = m.additional_kwargs.get("tokens", 0)

#             elif isinstance(m, dict):
#                 role = m.get("role", "unknown")
#                 content = m.get("content", "")
#                 tokens = m.get("tokens", 0)

#             else:
#                 continue

#             result.append({
#                 "role": role,
#                 "content": content,
#                 "tokens": tokens
#             })

#         print(f"Successfully loaded {len(result)} messages.")
#         return result
 
#     @classmethod
#     def clear_thread(cls, thread_id: str):
#         """
#         Resets the conversation history for a specific thread 
#         by overwriting it with an empty state.
#         """
#         if not thread_id:
#             print("[DEBUG] Clear failed: No thread_id provided.")
#             return False

#         config = cls.get_config(thread_id)
        
#         # We create a 'blank' checkpoint structure
#         empty_checkpoint = {
#             "v": 1,
#             "ts": datetime.now(timezone.utc).isoformat(),
#             "id": str(uuid.uuid4()),
#             "step": 0,  # ✅ ADD THIS

#             "channel_values": {"messages": []}, # Empty the messages list
#             "channel_versions": {"messages":1},
#             "versions_seen": {},
#             "pending_sends": []
#         }

#         # Put the empty state into memory
#         cls._checkpointer.put(config, empty_checkpoint, {"source": "manual_reset"}, {})
        
#         print(f"[DEBUG] History CLEARED for Thread: {thread_id}")
#         return True


class CheckpointUtil:
    _checkpointer = MemorySaver(
serde=JsonPlusSerializer(allowed_msgpack_modules=allowed)

    )
    _namespace = "default" 

    @staticmethod
    def create_thread_id() -> str:
        return str(uuid.uuid4())

    @staticmethod
    def get_config(thread_id: str):
        return {
            "configurable": {
                "thread_id": thread_id,
                "checkpoint_ns": CheckpointUtil._namespace,
            }
        }
    @classmethod
    def load_checkpoint(cls, thread_id: str):
        config = cls.get_config(thread_id)
        checkpoint = cls._checkpointer.get(config)

        if not checkpoint:
            return None

        return checkpoint

    @classmethod
    def load_messages(cls, thread_id: str):
        checkpoint = cls.load_checkpoint(thread_id)

        if not checkpoint:
            return []

        messages = checkpoint.get("channel_values", {}).get("messages", [])

        result = []
        for msg in messages:
            role = "user" if isinstance(msg, HumanMessage) else "assistant"
            result.append({
                "role": role,
                "content": msg.content,
                "tokens": msg.additional_kwargs.get("tokens", 0)
            })

        return result
    @classmethod
    def load_lc_messages(cls, thread_id: str):
        checkpoint = cls.load_checkpoint(thread_id)

        if not checkpoint:
            return []

        messages = checkpoint.get("channel_values", {}).get("messages", [])

        fixed = []
        for msg in messages:
            if isinstance(msg, dict):
                # 🔥 fix polluted checkpoints
                if msg["role"] == "user":
                    m = HumanMessage(content=msg["content"])
                else:
                    m = AIMessage(content=msg["content"])

                if "tokens" in msg:
                    m.additional_kwargs["tokens"] = msg["tokens"]

                fixed.append(m)
            else:
                fixed.append(msg)

        return fixed
    @classmethod
    def debug_checkpoint(cls, thread_id: str):
        checkpoint = cls.load_checkpoint(thread_id)

        if not checkpoint:
            print("No checkpoint found")
            return

        print("Checkpoint ID:", checkpoint.get("id"))
        print("Versions:", checkpoint.get("channel_versions"))
        print("Messages count:", len(checkpoint.get("channel_values", {}).get("messages", [])))

    @classmethod
    def load_state_for_graph(cls, thread_id: str, state_cls, **kwargs):
        """
        Generic loader for any state class

        :param thread_id: conversation id
        :param state_cls: Pydantic model class (e.g., ClassificationState)
        :param kwargs: dynamic fields like request, user_input, etc.
        """
        checkpoints = list(cls._checkpointer.list(cls.get_config(thread_id)))
        latest = checkpoints[-1] if checkpoints else None
        
        checkpoint = (
            latest.checkpoint if hasattr(latest, "checkpoint") else latest
        ) if latest else None
        # ✅ No checkpoint → fresh state
        if not checkpoint:
            return state_cls(**kwargs)

        channel_values = checkpoint.get("channel_values", {})

        # 1️⃣ Get the saved state from checkpoint
        state_obj = channel_values.get("state")

        if isinstance(state_obj, dict) or state_obj is None:
            # safe: unpack dict into state_cls
            state = state_cls(**(state_obj or {}))
        elif isinstance(state_obj, state_cls):
            # already a Pydantic instance, use as-is
            state = state_obj
        else:
            raise TypeError(f"Unexpected state type: {type(state_obj)}")

        # 2️⃣ Override with latest runtime inputs (kwargs)
        for key, value in kwargs.items():
            setattr(state, key, value)

        return state

        # ✅ 2. Fallback: build from messages
        messages = channel_values.get("messages", [])

        history = []
        for msg in messages:
            role = "User" if isinstance(msg, HumanMessage) else "Assistant"
            history.append(f"{role}: {msg.content}")

        # ✅ Merge fallback + runtime values
        return state_cls(
            conversation_history=history,
            **kwargs
        )
#     def save_message(cls, thread_id: str, role: str, content: str, tokens: int, state: dict = None):
#         config = cls.get_config(thread_id)
#         checkpoint_id = str(uuid.uuid4())

#         # ✅ 1. Load existing checkpoint
#         checkpoint = cls._checkpointer.get(config) or {}

#         channel_values = checkpoint.get("channel_values", {})
#         channel_versions = checkpoint.get("channel_versions", {})
#         versions_seen = checkpoint.get("versions_seen", {})

#         messages = channel_values.get("messages", [])

#         # ✅ 2. Create message object
#         if role == "user":
#             msg = HumanMessage(content=content)
#         else:
#             msg = AIMessage(content=content)

#         # ✅ store tokens
#         msg.additional_kwargs["tokens"] = tokens

#         # ✅ 3. Append message (NO rebuilding)
#         messages.append(msg)
#         # ✅ 4. Save full state if provided
#         if state:
#             channel_values["state"] = state
#         # ✅ 4. Increment version (CRITICAL)
#         # ✅ messages version
#         current_msg_version = channel_versions.get("messages", 0)
#         new_msg_version = current_msg_version + 1
#         channel_versions["messages"] = new_msg_version

#         # ✅ state version (ADD THIS)
#         current_state_version = channel_versions.get("state", 0)
#         new_state_version = current_state_version + 1
#         channel_versions["state"] = new_state_version
#         # ✅ 5. Build checkpoint
#         new_checkpoint = {
#             "v": 1,
#             "id": checkpoint_id,
#             "ts": datetime.now(timezone.utc).isoformat(),
#             "channel_values": {
#                 "messages": messages,
# "state":   channel_values.get('state',{})
#          },
#             "channel_versions": channel_versions,
#             "versions_seen": versions_seen,
#             "pending_sends": []
#         }

#         # ✅ 6. Save checkpoint (ONLY put, no put_writes)
#         cls._checkpointer.put(
#             config,
#             new_checkpoint,
#             metadata={"source": "manual"},
#             new_versions={
#                 "messages": new_msg_version,
#                 "state": new_state_version   # ✅ CRITICAL
#             }
#         )

#         print(f"[CHECKPOINT] Saved {role} message. Total: {len(messages)}")

#         return {
#             "role": role,
#             "content": content,
#             "tokens": tokens
#         }
    @classmethod
    def save_message(cls, thread_id: str, role: str, content: str, tokens: int, state: dict = None, user_req: str = None):
        """ Save user or AI message to checkpoint safely, preserving all previous messages """
        config = cls.get_config(thread_id)
        checkpoint_id = str(uuid.uuid4())

        # Load existing checkpoint
        checkpoint = cls._checkpointer.get(config) or {}
        channel_values = checkpoint.get("channel_values", {})
        channel_versions = checkpoint.get("channel_versions", {})
        versions_seen =      checkpoint.get("versions_seen", {})

        # Make sure messages list exists
        messages = list(channel_values.get("messages", []))
        # Create message object
        msg = HumanMessage(content=content) if role == "user" else AIMessage(content=content)
        msg.additional_kwargs["tokens"] = tokens
        messages.append(msg)

        # Ensure user_req list exists
        user_reqs = list(channel_values.get("user_req", []))
        if user_req is not None:
            user_reqs.append(user_req)

        # Handle state
        existing_state = state if state is not None else channel_values.get("state")

        # Update versions based on lengths
        channel_versions = channel_versions.copy()
        
        channel_versions["messages"] = channel_versions.get("messages", 0) + 1
        channel_versions["user_req"] = channel_versions.get("user_req", 0) + (1 if user_req is not None else 0)
        
        if state is not None:
            channel_versions["state"] = channel_versions.get("state", 0) + 1
        versions_seen = versions_seen.copy()
        for key, value in channel_versions.items():
            versions_seen[key] = value
        # Build new channel values
        new_channel_values = {
            "messages": messages,
            "user_req": user_reqs
        }
        if existing_state is not None:
            new_channel_values["state"] = existing_state

        # Build new checkpoint by merging into old checkpoint
        new_checkpoint = {
            **checkpoint,  # preserve other keys
            "v": 1,
            "id": checkpoint_id,
            "ts": datetime.now(timezone.utc).isoformat(),
            "channel_values": new_channel_values,
            "channel_versions": channel_versions,
            "versions_seen": versions_seen,
            "pending_sends": []
        }

        # Save atomically
        cls._checkpointer.put(
            config,
            new_checkpoint,
            metadata={"source": "manual"},
            new_versions=channel_versions
        )

        # DEBUG: Verify immediately
        all_cps = list(cls._checkpointer.list(config))

        print("TOTAL CHECKPOINTS:", len(all_cps))

        latest_cp = all_cps[-1] if all_cps else None

        if latest_cp:
            cp = latest_cp.checkpoint if hasattr(latest_cp, "checkpoint") else latest_cp

            print("===== AFTER SAVE CHECKPOINT (LATEST) =====")
            print("Messages count:", len(cp.get("channel_values", {}).get("messages", [])))
            print("Full messages:", cp.get("channel_values", {}).get("messages", []))

        return {
            "role": role,
            "content": content,
            "tokens": tokens
        }
    @classmethod
    def get_user_reqs(cls, thread_id: str) -> list[str]:
        """
        Returns the list of all saved user requests (user_req) for a given thread_id.
        Returns an empty list if none are found.
        """
        checkpoint = cls.load_checkpoint(thread_id)
        if not checkpoint:
            return []

        channel_values = checkpoint.get("channel_values", {})
        user_reqs = channel_values.get("user_req", [])

        # ensure all items are strings
        return [str(ur) for ur in user_reqs]