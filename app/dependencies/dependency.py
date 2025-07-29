from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.database import get_session
from app.dependencies.service_container import ServiceContainer

def get_service_container(session: Session = Depends(get_session)) -> ServiceContainer:
    return ServiceContainer(session=session)