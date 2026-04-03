from db.repository.service_request_repository import ServiceRequestRepository

class ServiceRequestService:
    def __init__(self):
        self.repository = ServiceRequestRepository()

    def create_service_request(self,service,request_type,data,final_summary):
        return self.repository.create(
    service=service,
    request_type=request_type,
    data=data,
    final_summary=final_summary
)
    def update_service_request(self,request_id,service,request_type,data,final_summary):
        return self.repository.update(

            request_id=request_id,
            service=service,
    request_type=request_type,
    data=data,
    final_summary=final_summary
        )
    def get_records(self,limit,offset,service,request_type):
        return self.repository.get_records(limit,offset,service,request_type)
        
service_request_service = ServiceRequestService()