import uuid

class IDGenerator:

    @staticmethod
    def generate_uuid() -> str:
        return str(uuid.uuid4())