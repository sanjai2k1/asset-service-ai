from .prompts  import SERVICE_CLASSIFICATION_PROMPT,EXTRACT_MANDATORY_FIELDS_PROMPT,FINAL_SUMMARY_PROMPT
from core.enums import PromptkeyDependency,Promptkey
from db.cache.prompt_cache import prompt_cache
import json
def build_table_for_services(cache_key: str, selected_ids: List[int]) -> str:
    cache_data = prompt_cache[cache_key]
    result = []

    for sid in selected_ids:
        data = cache_data.get(sid)
        if not data:
            continue

        service_name = None
        request_type_parent_id = None
        request_types = []

        # Step 1: Identify service and request_type parent
        for item in data:
            if item["parent_id"] == PromptkeyDependency.Service:
                service_name = item["description"]
            if item["keyword"] == "request_type":
                request_type_parent_id = item["dep_id"]

        # Step 2: Gather all request types under the parent
        for item in data:
            if item["parent_id"] == request_type_parent_id:
                rt_entry = {
                    "name": item["description"],
                    "description": item.get("uasge_description_dep", "")
                }
                request_types.append(rt_entry)

        # Step 3: Append structured service entry
        if service_name:
            result.append({
                "service": service_name,
                "request_types": request_types
            })

    # Convert full structure to JSON string
    return json.dumps(result, indent=2)


def build_service_classification_prompt(state) -> str:


    # safe access (dict-style for TypedDict)
    request = state.get("request")
    service = state.get("service_type")
    request_type = state.get("request_type")
    user_reqs = state.get("user_reqs") + [request]
    services_reqstable = build_table_for_services(Promptkey.SR_CREATION, [PromptkeyDependency.FEMS, PromptkeyDependency.BEMS, PromptkeyDependency.CLS, PromptkeyDependency.LLS, PromptkeyDependency.HWMS])            

    prompt = SERVICE_CLASSIFICATION_PROMPT.format(
        request="\n".join(user_reqs),
        services_and_reqtypes=services_reqstable 
    )

    return prompt



def get_required_fields_for_request_type(
    cache_key: str,
    selected_ids: list[int],
    service_keyword: str,
    request_type_keyword: str
) -> dict:
    cache_data = prompt_cache[cache_key]
    required_fields = dict()
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
                required_fields[item["keyword"]]={}
                required_fields[item["keyword"]][item["description"]] = item["uasge_description_dep"] if item["uasge_description_dep"] else ""
    return required_fields

def build_dict_for_mandator_fields(found_service : str , found_request_type : str)-> dict:
    ans = get_required_fields_for_request_type(cache_key= Promptkey.SR_CREATION,selected_ids= [PromptkeyDependency.FEMS, PromptkeyDependency.BEMS, PromptkeyDependency.CLS, PromptkeyDependency.LLS, PromptkeyDependency.HWMS]
     ,service_keyword=found_service,
    request_type_keyword=found_request_type)
    return ans

def build_prompt_extarct_mandatory(state)-> str:
    mandatory_fields = build_dict_for_mandator_fields (
         found_service=state["service"],
    found_request_type=state["request_type"]
        )
    if not mandatory_fields:
        return ""
    user_reqs = state["user_reqs"]+[state["request"]]
    prompt = EXTRACT_MANDATORY_FIELDS_PROMPT.format(mandatory_fields = json.dumps(mandatory_fields, indent=2) ,user_reqs = "\n".join(user_reqs))
    return prompt


def build_prompt_final_summary(state)-> str:
    service = state["service"]
    request_type = state["request_type"]
    data = state["data"]
    user_reqs = state["user_reqs"]
    prompt = FINAL_SUMMARY_PROMPT.format(
        service = service,
        request_type = request_type,
        data = json.dumps(data,indent=2),
        user_reqs = "\n".join(user_reqs)
        
        )
    return prompt