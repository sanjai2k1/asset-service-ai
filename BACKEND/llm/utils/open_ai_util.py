import tiktoken
from openai import OpenAI
from config.settings import settings
class OpenAI_LLMUtil:

    def __init__(self, llm_url: str, llm_key: str, llm_model: str, encoding_name="cl100k_base"):
        self.model = llm_model
        self.client = OpenAI(base_url=llm_url, api_key=llm_key)
        self.encoding = tiktoken.get_encoding(encoding_name)

    def count_tokens(self, text: str) -> int:
        """Count tokens using tiktoken"""

        return len(self.encoding.encode(text))
    def validate_token_limit(self,messages: List[Dict[str, Any]], max_limit: int = 128000):
        """
        Calculates the total tokens in a message list and raises an error if over limit.
        """
        total_tokens = sum(m.get("tokens", 0) for m in messages)
        
        if total_tokens > max_limit:
            raise ValueError(
                f"Token limit exceeded! Total: {total_tokens}, Limit: {max_limit}. "
                f"Please reduce the conversation length."
            )
        
        return total_tokens
    # def generate(self, prompt: str, thread_id: str = None):
    #     """
    #     Interacts with OpenAI and persists state using LangGraph's MemorySaver 
    #     via CheckpointUtil.
    #     """
    #     # 1. Ensure thread_id exists
    #     if not thread_id:
    #         thread_id = CheckpointUtil.create_thread_id()
    #         #print(f"[LLM] No thread_id provided. Created new session: {thread_id}")
    
    #     # --- EVERYTHING BELOW MUST BE OUTSIDE THE IF BLOCK ---
    
    #     # 2. Save the new user message
    #     user_tokens = self.count_tokens(prompt)
    #     CheckpointUtil.save_message(
    #         thread_id=thread_id, 
    #         role="user", 
    #         content=prompt, 
    #         tokens=user_tokens
    #     )
    #     #print("chk writed")
    #     # 3. Load the full conversation
    #     print("before generate")
    #     # 1. Load the conversation (which has 'role', 'content', and 'tokens')
    #     conversation = CheckpointUtil.load_thread(thread_id)
    #     print("Loaded history count:", len(conversation))
    #     print(conversation)
    #     print("lllllllllllllllllllllllllllllllllllllll")
    #     self.validate_token_limit(conversation, settings.max_tokens)
    #     # 2. Format for OpenAI API (STRIP the 'tokens' key)
    #     chat_messages = [
    #         {
    #             "role": m["role"], 
    #             "content": m["content"]
    #         } 
    #         for m in conversation 
    #         if m["content"].strip() # Also good to skip empty messages here!
    #     ]

    #     # 3. Final Safety Check
    #     if not chat_messages:
    #         chat_messages = [{"role": "user", "content": prompt}]
    #     # 5. Call OpenAI
    #     response = self.client.chat.completions.create(
    #         model=self.model,
    #         messages=chat_messages,
    #         temperature=0
    #     )
    #     #print(response)
    #     choice = response.choices[0].message
        
    #     assistant_content = choice.content
        
    #     if not assistant_content:
    #         if hasattr(choice, "tool_calls") and choice.tool_calls:
    #             assistant_content = str(choice.tool_calls)
    #     completion_tokens = getattr(response.usage, "completion_tokens", 0)
    #     prompt_tokens = getattr(response.usage, "prompt_tokens", 0)
    #     total_tokens = getattr(response.usage, "total_tokens", 0)

    #     CheckpointUtil.save_message(
    #         thread_id=thread_id, 
    #         role="assistant", 
    #         content=assistant_content, 
    #         tokens=completion_tokens
    #     )

    #     final_messages = CheckpointUtil.load_thread(thread_id)
    #     #print(final_messages)
    #     #print("final--------")
    #     return {
    #         "thread_id": thread_id,
    #         "content": assistant_content,
    #         "messages": final_messages,
    #         "usage": {
    #             "prompt_tokens": prompt_tokens,
    #             "completion_tokens": completion_tokens,
    #             "total_tokens": total_tokens
    #         }
    #     }
    # def generate(self, prompt: str, thread_id: str = None,state : dict = None,user_req : str = None):
    #     """
    #     Manual memory + OpenAI call (NO LangGraph state dependency)
    #     """

    #     # ✅ 1. Ensure thread_id
    #     if not thread_id:
    #         thread_id = CheckpointUtil.create_thread_id()

    #     # ✅ 2. Save user message
    #     user_tokens = self.count_tokens(prompt)

    #     CheckpointUtil.save_message(
    #         thread_id=thread_id,
    #         role="user",
    #         content=prompt,
    #         tokens=user_tokens,
    #         state= None,
    #         user_req = user_req
    #     )

    #     print("before generate")

    #     # ✅ 3. Load conversation (clean format)
    #     conversation = CheckpointUtil.load_messages(thread_id)

    #     print("Loaded history count:", len(conversation))
    #     print(conversation)

    #     # ✅ 4. Token validation
    #     self.validate_token_limit(conversation, settings.max_tokens)

    #     # ✅ 5. Format for OpenAI
    #     chat_messages = [
    #         {
    #             "role": m["role"],
    #             "content": m["content"]
    #         }
    #         for m in conversation
    #         if m["content"].strip()
    #     ]

    #     # ✅ Safety fallback
    #     if not chat_messages:
    #         chat_messages = [{"role": "user", "content": prompt}]

    #     # ✅ 6. Call OpenAI
    #     response = self.client.chat.completions.create(
    #         model=self.model,
    #         messages=chat_messages,
    #         temperature=0
    #     )

    #     choice = response.choices[0].message
    #     assistant_content = choice.content

    #     # ✅ Handle tool calls fallback
    #     if not assistant_content:
    #         if hasattr(choice, "tool_calls") and choice.tool_calls:
    #             assistant_content = str(choice.tool_calls)

    #     # ✅ Token usage
    #     completion_tokens = getattr(response.usage, "completion_tokens", 0)
    #     prompt_tokens = getattr(response.usage, "prompt_tokens", 0)
    #     total_tokens = getattr(response.usage, "total_tokens", 0)





    #     return {
    #         "thread_id": thread_id,
    #         "content": assistant_content,
    #         "messages": None,
    #         "usage": {
    #             "prompt_tokens": prompt_tokens,
    #             "completion_tokens": completion_tokens,
    #             "total_tokens": total_tokens
    #         }
    #     }
    def cleaned_generate(self, chat_messages: list[dict],thread_id : str) -> dict:
        """
        Minimal OpenAI call for chat completion.
        Returns the assistant content and token usage.
        """

        # Prepare messages (only current prompt, no memory)

        # Call OpenAI
        response = self.client.chat.completions.create(
            model=self.model,
            messages=chat_messages,
            temperature=0
        )

        # Get assistant content
        choice = response.choices[0].message
        assistant_content = getattr(choice, "content", "")

        # Fallback if content missing (tool calls etc.)
        if not assistant_content:
            if hasattr(choice, "tool_calls") and choice.tool_calls:
                assistant_content = str(choice.tool_calls)

        # Token usage
        usage = {
            "prompt_tokens": getattr(response.usage, "prompt_tokens", 0),
            "completion_tokens": getattr(response.usage, "completion_tokens", 0),
            "total_tokens": getattr(response.usage, "total_tokens", 0)
        }

        return {
            "thread_id": thread_id,
            "content": assistant_content,
            "messages": None,

            "usage": usage
        }