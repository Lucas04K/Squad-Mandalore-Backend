from fastapi import APIRouter, Depends, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from starlette.responses import Response

from src.database.database_utils import get_db
from src.models.models import Certificate, User
from src.schemas.certificate_schema import CertificateResponseSchema, CertificatePatchSchema
from src.services import certificate_service
from src.services.auth_service import get_current_user

router = APIRouter(
    # routing prefix
    prefix="/certificates",
    # documentation tag
    tags=["certificates"],
    # default response
    # responses={404: {"route": "Not found"}},
)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_certificates(id: str, db: Session = Depends(get_db)) -> Response:
    certificate = certificate_service.get_certificates_by_id(id, db)
    return Response(content=certificate.blob, media_type="application/octet-stream")


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_certificate(id: str, db: Session = Depends(get_db)) -> None:
    return certificate_service.delete_certificate(id, db)


@router.post("/", response_model=CertificateResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_certificate(blob: UploadFile = File(...), athlete_id: str = Form(...), title: str = Form(...), user: User = Depends(get_current_user),
                             db: Session = Depends(get_db)) -> Certificate:
    return certificate_service.create_certificate(athlete_id, title, blob, user.id, db)


@router.patch("/{id}", response_model=CertificateResponseSchema, status_code=status.HTTP_202_ACCEPTED)
async def update_certificate(id: str, certificate_patch_schema: CertificatePatchSchema, user: User = Depends(get_current_user),
                             db: Session = Depends(get_db)) -> Certificate:
    return certificate_service.update_certificate(id, certificate_patch_schema, db)