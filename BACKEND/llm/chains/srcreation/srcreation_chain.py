from langchain_core.messages import HumanMessage
from llm.factory.llm_factory import LLMFactory
from llm.prompts.servicerequestcreation import servicerequestcreate_prompt 
from llm.utils.guardrails_utils import GuardrailsUtils
from schemas.srcreation.classification_result_schema import ClassificationResult,MandatoryFieldsResponse
from db.cache.prompt_cache import prompt_cache
from core.enums import PromptkeyDependency,Promptkey
from config.settings import settings
from llm.utils.InMemoryMessasageUtil import InMemoryCache
class SRCreationChain:
    def __init__(self, max_retries: int = 1):
        self.llm = LLMFactory.get_open_ai_llm()
        self.guard = GuardrailsUtils.create_guard(ClassificationResult)
        self.mandatory_field_guard = GuardrailsUtils.create_guard(MandatoryFieldsResponse)
        self.max_retries = max_retries
    def build_table_for_services(self,cache_key: str, selected_ids: list[int]) -> str:

        cache_data = prompt_cache[cache_key]

        table_lines = []
        table_lines.append("Service | Request Types")
        table_lines.append("-" * 70)

        for sid in selected_ids:
            data = cache_data.get(sid)

            if not data:
                continue

            service_name = ""
            request_type_parent_id = None
            request_types = []

            # 🔹 Step 1: Identify correct service + request_type node
            for item in data:
                # ✅ ONLY ROOT SERVICE
                if item["parent_id"] == PromptkeyDependency.Service:
                    service_name = item["description"]

                # request_type node
                if item["keyword"] == "request_type":
                    request_type_parent_id = item["dep_id"]

            # 🔹 Step 2: Get all request types
            for item in data:
                if item["parent_id"] == request_type_parent_id:
                    request_types.append(item["description"] + (f" ({item['uasge_description_dep']})" if item.get("uasge_description_dep") else ""))

            # 🔹 Step 3: Build row
            types_str = ", ".join(request_types)
            table_lines.append(f"{service_name:<50} | {types_str}")

        return "\n".join(table_lines)
    def generate_for_service_and_reqtypes(
        self,
        prompt: str,
        thread_id: str = None,
        state: dict = None,
        user_req: str = None
    ) -> dict:
        """
        Full generate method: saves user message, loads conversation, validates tokens,
        formats chat_messages, and calls OpenAI via cleaned_generate.
        """
        # 1️⃣ Ensure thread_id
        if not thread_id:
            thread_id = InMemoryCache.create_thread_id()

        # 2️⃣ Save user message to checkpoint
        user_tokens = self.llm.count_tokens(prompt)
        InMemoryCache.save_message(
            thread_id=thread_id,
            role="user",
            content=prompt,
            tokens=user_tokens,
            state=None,      # optionally pass state if needed
            user_req=user_req
        )

        # 3️⃣ Load full conversation
        conversation = InMemoryCache.load_messages(thread_id)

        # 4️⃣ Token validation
        self.llm.validate_token_limit(conversation, settings.max_tokens)

        # 5️⃣ Format messages for OpenAI
        chat_messages = [
            {"role": m["role"], "content": m["content"]}
            for m in conversation
            if m["content"].strip()
        ]

        # Safety fallback: at least the current prompt
        if not chat_messages:
            chat_messages = [{"role": "user", "content": prompt}]

        # 6️⃣ Call OpenAI using cleaned_generate
        response = self.llm.cleaned_generate(chat_messages=chat_messages, thread_id=thread_id)

        return response
    def generate_for_mandatory_fields(
        self,
        prompt: str,
        thread_id: str,
        state : dict = None,
        user_req: str = None
    ) -> dict:
        """
        Generate LLM response for mandatory fields prompt.
        Sends only the latest prompt to the LLM and optionally saves user input.

        Args:
            prompt (str): The formatted prompt to send to the LLM.
            thread_id (str): Thread ID for checkpoint tracking.
            user_req (str, optional): User input to save in checkpoint.

        Returns:
            dict: LLM response from cleaned_generate, including content and token usage.
        """

        # Save the user request if provided
        user_tokens = self.llm.count_tokens(user_req)
        InMemoryCache.save_message(
                thread_id=thread_id,
                role="user",
                content=prompt,
                tokens=user_tokens,
                state=None,
                user_req=user_req
            )

        # 1️⃣ Get only user requests
        user_reqs = InMemoryCache.get_user_reqs(thread_id)

        

        chat_messages = [{"role": "user", "content": prompt}]

        # Call LLM
        response = self.llm.cleaned_generate(chat_messages=chat_messages, thread_id=thread_id)

        return response

    def run(self, thread_id: str, request: str, services: Optional[str], typesofrequests: Optional[str],state : dict = None) -> ClassificationResult:

            services_reqstable = self.build_table_for_services(Promptkey.SR_CREATION, [PromptkeyDependency.FEMS, PromptkeyDependency.BEMS, PromptkeyDependency.CLS, PromptkeyDependency.LLS, PromptkeyDependency.HWMS])            
            print(services_reqstable)
            prompt = servicerequestcreate_prompt.SERVICE_CLASSIFICATION_PROMPT.format(
                request=request,
                services_and_reqtypes=services_reqstable or "",
                found_service = state.service or "<service name or null>",
                found_reqtype = state.request_type or "<request type or null>"
            )

            for attempt in range(self.max_retries):
                try:
                    
                    # 1. Call LLM
                    response = self.generate_for_service_and_reqtypes(prompt=prompt, thread_id=thread_id,state = state,user_req=request)
                    content_to_validate = response.get("content")
                    if not content_to_validate:
                        raise ValueError("LLM generated empty content.")

                    # 2. Validate via Guardrails
                    outcome = self.guard.parse(content_to_validate)
                    data = outcome.validated_output



                    # 3. If validation passed, return ClassificationResult
                    if outcome.validation_passed:
                                # ✅ 7. Save assistant response

                        return ClassificationResult(
    **(data if isinstance(data, dict) else data.model_dump()),
    llm_response_dets=response
)
                except Exception as e:

                    print(f"Guardrails validation failed on attempt {attempt + 1}: {e}")
                    print(str(e))

            # 4. If all retries fail, return empty ClassificationResult
            return ClassificationResult()
    def get_required_fields_for_request_type(
        self,
        cache_key: str,
        selected_ids: list[int],
        service_keyword: str,
        request_type_keyword: str
    ) -> list[str]:

        cache_data = prompt_cache[cache_key]

        required_fields = []

        for sid in selected_ids:
            data = cache_data.get(sid)
            if not data:
                continue

            service_id = None
            request_type_parent_id = None
            request_type_id = None
            required_fields_parent_id = None

            # 🔹 Step 1: Find service
            for item in data:
                if item["description"].lower() == service_keyword.lower() and item["parent_id"] == PromptkeyDependency.Service:
                    service_id = item["dep_id"]

            if not service_id:
                continue

            # 🔹 Step 2: Find request_type root
            for item in data:
                if item["keyword"] == "request_type" and item["parent_id"] == service_id:
                    request_type_parent_id = item["dep_id"]

            # 🔹 Step 3: Find specific request_type
            for item in data:
                if (
                    item["parent_id"] == request_type_parent_id and
                    item["description"].lower() == request_type_keyword.lower()
                ):
                    request_type_id = item["dep_id"]

            if not request_type_id:
                continue

            # 🔹 Step 4: Find required_fields node
            for item in data:
                if (
                    item["keyword"] == "required_fields" and
                    item["parent_id"] == request_type_id
                ):
                    required_fields_parent_id = item["dep_id"]

            if not required_fields_parent_id:
                continue

            # 🔹 Step 5: Get actual fields
            for item in data:
                if item["parent_id"] == required_fields_parent_id:
                    required_fields.append(item["description"])

        return required_fields

    def run_mandatory_fields(self,thread_id: str,state : dict = None):
        found_service = state.service
        found_request_type = state.request_type
        mandatory_fields = self.get_required_fields_for_request_type(cache_key= Promptkey.SR_CREATION,selected_ids= [PromptkeyDependency.FEMS, PromptkeyDependency.BEMS, PromptkeyDependency.CLS, PromptkeyDependency.LLS, PromptkeyDependency.HWMS]
         ,service_keyword=found_service,
    request_type_keyword=found_request_type
        )

        print(mandatory_fields)

        list_of_user_data = InMemoryCache.get_user_reqs(thread_id=thread_id)
        prompt = servicerequestcreate_prompt.MANDATORY_FIELDS_PROMPT.format(
              
                mandatory_fields = ",".join(mandatory_fields),
                user_data = "\n".join(list_of_user_data)
            )
        try:

            response = self.generate_for_mandatory_fields(prompt=prompt, thread_id=thread_id,state = state,user_req=state.request)

            content_to_validate = response.get("content")
            if not content_to_validate:
                raise ValueError("LLM generated empty content.")
            # 2. Validate via Guardrails
            outcome = self.mandatory_field_guard.parse(content_to_validate)
            data = outcome.validated_output
            if outcome.validation_passed:
                return MandatoryFieldsResponse(
    **(data if isinstance(data, dict) else data.model_dump()),    llm_response_dets=response

)
        except Exception as e:
            print(str(e))
        return state