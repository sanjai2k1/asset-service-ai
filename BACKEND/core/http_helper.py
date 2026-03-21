import requests
from core.logging import logger
from core.exceptions import AppException

class HttpHelper:

    @staticmethod
    def post(url: str, payload: dict, headers: dict):

        try:

            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=120
            )

            response.raise_for_status()

            return response.json()
        except AppException as ex:
            logger.warning(f"Handled AppException: {ex.message}")

            raise HTTPException(
                status_code=ex.status_code,
                detail=ex.message
            )

        except Exception as ex:

            logger.error(str(ex), exc_info=True)
            raise