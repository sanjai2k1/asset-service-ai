from core.rest_helper import RestHelper
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi import APIRouter
from services.AnalyzeExcel.analyzeexcel_service import AnalyzeExcelService
router = APIRouter(
    prefix="/analyze-excel",
    tags=["Excel Analyzer"]
)

analyze_excel_service = AnalyzeExcelService()


@router.post("/ask")
async def upload_excel(
    request: str = Form(""),
    file: UploadFile = File(None),   # ✅ FIXED
    thread_id: str = Form("")      # also simplify this
):
    return await RestHelper.execute(analyze_excel_service.ask,request,file,thread_id)