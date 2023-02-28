from src.services.certificado.Certificado import Certificado
from cryptography.x509 import Certificate, load_der_x509_crl
from datetime import datetime


class ValidacionCrl():
    def __init__(self) -> None:

        self.certificado = Certificado()

    async def validar_certificado(self, username: str, password: str,env:str):
        try:
            certificado = await self.certificado.obtener_cerficado_crl(username, password,env)

            if type(certificado) is dict:

                return certificado
            else:
                validacion_vencimiento = self.validacion_vencimiento(certificado)

                
                if(validacion_vencimiento is not None):
                    return validacion_vencimiento
                
                validacion_revocacion = self.validacion_revocacion(certificado,env)
                
                if (validacion_revocacion is not None):
                    return validacion_revocacion 
                return {
                    "codigo": 3,
                    "estado": "Certificado Vigente"
                }
        except:
            return{
                "codigo":8,
                "estado":"Error al obtener certificado, Verifique la conexión a internet"
            }

    def validacion_vencimiento(self, certificado: Certificate) -> dict:
        fecha_actual = datetime.now()
        fecha_vencimiento = certificado.not_valid_after
        if (fecha_actual > fecha_vencimiento):
            return {
                "codigo": 1,
                "estado": "Certificado Vencido",
                "fecha_de_vencimiento": certificado.not_valid_after.strftime("%d/%m/%Y"),
                

            }
        return None

    def validacion_revocacion(self, certificado: Certificate,env:str) -> dict:
        no_serial_certificado = certificado.serial_number
        if env == "prod":
            crl_data = open("CCGCRL.crl", "rb").read()
        elif env == "sandbox":
            crl_data = open("CCGCRL_Sandbox.crl", "rb").read()
            

        crl = load_der_x509_crl(crl_data)
        for r in crl:
            if no_serial_certificado == r.serial_number:
                return {
                    "codigo": 2,
                    "estado": "Certificado Revocado",
                    "fecha_de_revocacion": r.revocation_date.strftime("%d/%m/%Y"),
                    
                }
        return None
