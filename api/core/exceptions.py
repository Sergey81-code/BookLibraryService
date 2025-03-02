
from fastapi import HTTPException


class AppExceptions:

    @staticmethod
    def bad_request_exception(message: str):
        """Raise HTTPException with status_code 400 and message"""
        raise HTTPException(status_code=400, detail=message)
    
    @staticmethod
    def not_found_exception(message: str):
        """Raise HTTPException with status_code 404 and message"""
        raise HTTPException(status_code=404, detail=message)
    
    @staticmethod
    def validation_exception(message: str):
        """Raise HTTPException with status_code 422 and message"""
        raise HTTPException(status_code=422, detail=message)
    
    @staticmethod
    def service_unavailable_exception(message: str):
        """Raise HTTPException with status_code 503 and message"""
        raise HTTPException(status_code=503, detail=message)