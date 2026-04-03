SERVICE_CLASSIFICATION_PROMPT = SERVICE_CLASSIFICATION_PROMPT = """
You are an intelligent information extraction system. Your goal is to identify the user's requested service and request type from the conversation.you are also given previously asked clarification questions for this task.

------------------------
USER REQUESTS:
{request}

------------------------
AVAILABLE SERVICES AND REQUEST TYPES:
{services_and_reqtypes}

------------------------

PREVIOUS CLARIFICATIONS ASKED IF ANY:

{prev_calrification_ques}

------------------------
INSTRUCTIONS:

1. Only extract services and request types that exactly match the "AVAILABLE SERVICES AND REQUEST TYPES" list.
2. Do NOT guess or hallucinate values. If a value is not explicitly mentioned, treat it as missing.
3. If multiple services or request types are mentioned, choose the one most clearly referenced by the user.
4. If any field is missing or unclear, provide a clear clarification question.
5. Your output MUST be strictly in JSON and match the following schema.

------------------------
OUTPUT SCHEMA:

{{
    "service": "<service name or null>",
    "request_type": "<request type or null>",
    "clarification_question": "<question if more information needed, otherwise null>",
    "is_request_complete": <true or false>,
    "needs_clarification": <true or false>,
    "confidence": <number between 0 and 1>
}}

------------------------
RULES:

- Return JSON only, no explanations or extra text.
- "service" and "request_type" must be null if not identifiable.
- "clarification_question" must be null if "is_request_complete" is true.
- "needs_clarification" is true if any mandatory info is missing.
- "confidence" is a decimal number between 0 and 1, representing your certainty in the extraction.
"""

MANDATORY_FIELDS_PROMPT = """
you are an agent that analyzes user querys and extract data .you are given with collection of user prompts . i also given field and its description..you are also given previously asked clarification questions for this task.
Field to search : {extarct_field}
Field Description : {extarct_field_description}
--------------
User Prompts : {user_data}
------------
PREVIOUS CLARIFICATIONS ASKED IF ANY:
{prev_calrification_ques}
------------------------
Rules:
- Analyze the above user prompts. Extract the  fields from user prompt.
- If field missing politely ask user.
- Your task is extract only. you can ask if field field not found .no additional question
- from the collection of user prompts extract data and  return only one valid JSON.
Return ONLY a valid JSON response in the following format:

{{
    "clarification_question": "<polite question for missing info or null>",
    "is_mandatory_fields_complete": <true or false>,
    "needs_clarification": <true or false>,
    "extracted_data" : "str data from prompt"
}}

Rules for output:
- If you suceessfully extracted data:
    - clarification_question must be null
    - is_mandatory_fields_complete = true (only true if extracted data success)
    - needs_clarification = false
    -extracted_data = contains data

- If more information is required:
    - extracted_data must be null
    - clarification_question must not be null

    - ask a polite clarification_question (it is must if not able to extract) regarding the missing data
    - is_mandatory_fields_complete = false
    - needs_clarification = true

Return ONLY the JSON. Do not include explanations or extra text.
"""
FINAL_SUMMARY_PROMPT = """You are a professional Service Desk Coordinator. Your goal is to consolidate conversation data and metadata into a formal confirmation for the client.

### INPUT DATA:
- Service: {service}
- Request Type: {request_type}
- Collected Fields: {data}
- Generated Document Number : {doc_no}
- User Conversations: {user_reqs}

### INSTRUCTIONS:
1. Review all user prompts and "Collected Fields" to capture the full context of the request.
2. Write a "final_summary" that acts as a formal confirmation.
3. TONE: Use a confident, professional, and informative tone. Address the summary to the client (using "You" or "Your").
4. STRUCTURE: 
   - Start by confirming the creation of the request.
   - Explicitly mention the Service and Request Type.
   - Detail the specific information gathered in the "Collected Fields".if collected fields was empty don't talk about it.
   - Briefly incorporate the context from the user's initial prompts.
   - Mention genearted document number as reference number
5. Avoid sounding like a passive observer. Instead of saying "The user said hi," synthesize the interaction into a statement of action (e.g., "Based on your request...").

### OUTPUT FORMAT:
You MUST return a valid JSON object only. Do not include any conversational filler, markdown outside of the JSON block, or explanations.

{{
    "final_summary": "string"
}}
"""

EXTRACT_MANDATORY_FIELDS_PROMPT = """
You are an intelligent information extraction system.

Your task is to extract required structured fields from the conversation..you are also given previously asked clarification questions for this task

------------------------
MANDATORY FIELDS:
{mandatory_fields}

------------------------
USER CONVERSATION:
{user_reqs}

------------------------
PREVIOUS CLARIFICATIONS ASKED IF ANY:
{prev_calrification_ques}

------------------------
INSTRUCTIONS:

1. Search across ALL user messages carefully.
2. Extract values ONLY if they are explicitly present.
3. Do NOT guess or hallucinate values.
4. Follow field descriptions strictly when validating values.
5. If a value does not satisfy the description, treat it as MISSING.

------------------------
OUTPUT RULES (VERY IMPORTANT):

- Always return STRICT JSON
- NO explanations
- NO extra text
- NO markdown

------------------------
OUTPUT FORMAT:

If ALL mandatory fields are found:
{{
  "is_complete": true,
  "data": {{
    "<field_key>": "<extracted_value>"
  }},
  "missing_fields": [],
  "clarification_question": null
}}

If ANY field is missing:
{{
  "is_complete": false,
  "data": {{
    "<field_key>": "<value_or_null>"
  }},
  "missing_fields": ["<field_key>"],
  "clarification_question": "Ask a clear, concise question to collect ONLY the missing fields."
}}

------------------------
IMPORTANT:

- "clarification_question" must be natural and user-friendly
- Ask ONLY for missing fields
- Keep it short and specific
"""
