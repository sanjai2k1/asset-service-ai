from db.session import SessionLocal
from datetime import datetime
from typing import Optional, Dict
from db.models.ServiceRequest import ServiceRequest


class ServiceRequestRepository:

    def create(
        self,
        service: Optional[str] = None,
        request_type: Optional[str] = None,
        data: Optional[Dict[str, Optional[str]]] = None,
        final_summary: Optional[str] = None,
    ):
        with SessionLocal() as db:
            record = ServiceRequest(
                service=service,
                request_type=request_type,
                data=data,
                final_summary=final_summary,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            db.add(record)
            db.commit()
            db.refresh(record)

            return record
    def update(
        self,
        request_id: str,
        service: Optional[str] = None,
        request_type: Optional[str] = None,
        data: Optional[Dict] = None,
        final_summary: Optional[str] = None
    ):
        with SessionLocal() as db:
            record = db.query(ServiceRequest).filter(ServiceRequest.id == request_id).first()

            if not record:
                return None  # or raise exception

            # Update only provided fields
            if service is not None:
                record.service = service

            if request_type is not None:
                record.request_type = request_type

            if data is not None:
                record.data = data

            if final_summary is not None:
                record.final_summary = final_summary

            db.commit()
            db.refresh(record)

            return record
    def get_records(
        self,
        limit: int = 10,
        offset: int = 0,
        service: Optional[str] = None,
        request_type: Optional[str] = None
    ) -> Tuple[List[ServiceRequest], int]:
        """
        Fetch paginated ServiceRequest records with optional filtering.

        Args:
            limit (int): number of records to fetch (default 10)
            offset (int): starting point (default 0)
            service (str, optional): filter by service
            request_type (str, optional): filter by request_type

        Returns:
            Tuple[List[ServiceRequest], int]: list of records and total count
        """
        with SessionLocal() as db:
            query = db.query(ServiceRequest)

            # Optional filtering
            if service:
                query = query.filter(ServiceRequest.service == service)
            if request_type:
                query = query.filter(ServiceRequest.request_type == request_type)

            total_count = query.count()  # total records before pagination

            records = query.order_by(ServiceRequest.created_at.desc()) \
                           .offset(offset) \
                           .limit(limit) \
                           .all()

            return records, total_count