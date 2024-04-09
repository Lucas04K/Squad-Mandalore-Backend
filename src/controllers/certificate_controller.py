from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database.database_utils import get_db
from src.models.models import Certificate
from src.schemas.certificate_schema import CertificateResponseSchema, CertificatePostSchema, CertificatePatchSchema
from src.services import certificate_service

router = APIRouter(
    # routing prefix
    prefix="/certificates",
    # documentation tag
    tags=["certificates"],
    # default response
    # responses={404: {"route": "Not found"}},
)


@router.get("/all", response_model=list[CertificateResponseSchema], status_code=status.HTTP_200_OK)
async def get_all_certificates(db: Session = Depends(get_db)) -> list[Certificate]:
    return certificate_service.get_all_certificates(db)


@router.get("/{id}", response_model=CertificateResponseSchema, status_code=status.HTTP_200_OK)
async def get_certificates(id: str, db: Session = Depends(get_db)) -> Certificate:
    return certificate_service.get_certificates_by_id(id, db)


@router.delete("/{id}", response_model=CertificateResponseSchema, status_code=status.HTTP_200_OK)
async def delete_certificate(id: str, db: Session = Depends(get_db)) -> None:
    return certificate_service.delete_certificate(id, db)


@router.post("/", response_model=CertificateResponseSchema, status_code=status.HTTP_200_OK)
async def create_certificate(certificate_post_schema: CertificatePostSchema,
                             db: Session = Depends(get_db)) -> Certificate:
    return certificate_service.create_certificate(certificate_post_schema, db)


@router.patch("/{id}", response_model=CertificateResponseSchema, status_code=status.HTTP_202_ACCEPTED)
async def update_certificate(id: str, certificate_patch_schema: CertificatePatchSchema,
                             db: Session = Depends(get_db)) -> Certificate:
    return certificate_service.update_certificate(id, certificate_patch_schema, db)
