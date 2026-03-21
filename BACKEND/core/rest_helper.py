import traceback
import inspect
from fastapi.responses import JSONResponse
from core.logging import logger
import asyncio
from fastapi import HTTPException
from core.exceptions import AppException

class RestHelper:
    @staticmethod
    async def execute(func, *args, **kwargs):
        """Execute function and propagate exceptions as standard FastAPI 500 errors"""
        logger.info(f"Executing API: {func.__name__}")
        try:

            # Check if function is async
            if asyncio.iscoroutinefunction(func):
                logger.info(f"Success API: {func.__name__}")

                return await func(*args, **kwargs)
            logger.info(f"Success API: {func.__name__}")

            # If sync, run in a thread
            return await asyncio.to_thread(lambda: func(*args, **kwargs))
        except AppException as ex:
            logger.warning(f"Handled AppException: {ex.message}")

            raise HTTPException(
                status_code=ex.status_code,
                detail=ex.message
            )
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
            # Let FastAPI handle it as 500
            raise HTTPException(status_code=500, detail="Internal Server Error")