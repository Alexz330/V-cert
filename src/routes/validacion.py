from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.services.crl.validacion import ValidacionCrl
from src.services.ocsp.validacion import Validacion_ocsp

from src.schemas.Credenciales import Credenciales

validacion = APIRouter()

validacion_services = ValidacionCrl()
validacion_services_ocsp = Validacion_ocsp()
@validacion.post("/ocsp")
async def validacion_ocsp(credenciales: Credenciales):
    validacion = await validacion_services_ocsp.validar_certificado(
        username=credenciales.username,
        password=credenciales.password
    )

    return JSONResponse(status_code=200, content=validacion)

@validacion.post("/crl")
async def validacion_crl(credenciales: Credenciales):
    validacion = await validacion_services.validar_certificado(
        username=credenciales.username,
        password=credenciales.password
    )

    return JSONResponse(status_code=200, content=validacion)
