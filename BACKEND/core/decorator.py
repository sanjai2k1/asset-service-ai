# core/decorators.py
import functools
import sys
import io
import asyncio
from fastapi import HTTPException
from core.logging import logger
from core.exceptions import AppException

def handle_node_errors(func):
    """
    Pure Pass-Through Decorator:
    - Forwards ALL arguments (*args, **kwargs)
    - Propagates AppException with custom status codes
    - Converts unhandled Exceptions to 500
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        stderr = sys.stderr
        sys.stderr = io.StringIO()
        
        try:
            if asyncio.iscoroutinefunction(func):
                # Execute async node directly
                return await func(*args, **kwargs)
            else:
                # Execute sync node in a thread using a lambda to 
                # correctly unpack *args and **kwargs
                return await asyncio.to_thread(lambda: func(*args, **kwargs))
                
        except HTTPException:
            # Let existing FastAPI exceptions through
            raise
        except AppException as ex:
            # --- PROPAGATE CUSTOM APP ERRORS ---
            logger.warning(f"AppException in '{func.__name__}': {ex.message}")
            raise HTTPException(status_code=ex.status_code, detail=ex.message)
        except Exception as ex:
            # Log unexpected crashes and return 500
            logger.error(f"Unhandled crash in '{func.__name__}': {ex}", exc_info=True)
            raise HTTPException(status_code=500, detail="Internal Server Error")
        finally:
            sys.stderr = stderr
            
    return wrapper