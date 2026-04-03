from fastapi.responses import JSONResponse
from llm.utils.check_pointer_util import checkpoint_util
from config.settings import settings
import os
from core.utils import IDGenerator
import shutil
from domain.excel_analysis.graph import compile_graph

UPLOAD_FOLDER = settings.excel_uploaded_dir




def save_uploaded_file(file, thread_id: str, upload_folder: str) -> Tuple[str, str]:
    """
    Saves the uploaded file to a user-specific folder.

    Args:
        file: The uploaded file object (FastAPI UploadFile or similar)
        thread_id: Unique thread/session id
        upload_folder: Base upload folder path

    Returns:
        Tuple of (file_name, saved_file_path)
    """
    thread_path = os.path.join(upload_folder, thread_id)
    os.makedirs(thread_path, exist_ok=True)

    file_id = IDGenerator.generate_uuid()
    file_name = f"{file_id}_{file.filename}"
    file_path = os.path.join(thread_path, file_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_name, file_path
class AnalyzeExcelService:
    async def ask(self,request,file, thread_id):
        state = {"current_node_message":"Identifying Intent..." , "thread_id" : thread_id}
        if thread_id is None or not thread_id:
            thread_id = checkpoint_util.create_thread_id()
            state["thread_id"]= thread_id
        state["request"] = request

        if file :
            file_name, file_path = save_uploaded_file(file, thread_id, UPLOAD_FOLDER)
            state["excel_path"] = file_path

        else:
            file_name, file_path = None,None

        # Call your LangGraph flow
        compiled_graph = compile_graph()
        config = checkpoint_util.get_config(thread_id)
        result = await compiled_graph.ainvoke(
            state,
            config=config
        )
        return result

