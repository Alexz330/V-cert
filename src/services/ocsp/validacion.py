import subprocess
from dateutil.parser import parse
from cryptography.x509 import Certificate, load_der_x509_crl

from src.services.certificado.Certificado import Certificado
from datetime import datetime
from src.utilities.normalize_pem import normalize_pem
from src.utilities.write_ceritficate import write_ceritficate

class Validacion_ocsp:
    def __init__(self) -> None:

        self.certificado = Certificado()
    async def validar_certificado(self, username: str, password: str):
        certificado,certificado_base64 = await self.certificado.obtener_cerficado_ocsp(username, password)
        print(certificado)
        if type(certificado) is dict:

            return certificado
        else:
            validacion_vencimiento = self.validacion_vencimiento(certificado)

            
            if(validacion_vencimiento is not None):
                return validacion_vencimiento
            
            validacion_revocacion = self.validacion_revocacion(certificado_base64)
            
            if (validacion_revocacion is not None):
                return validacion_revocacion 
            return {
                "codigo": 3,
                "estado": "Certificado Vigente"
            }

    
    def validacion_vencimiento(self, certificado: Certificate) -> dict:
        fecha_actual = datetime.now()
        print(certificado)
        fecha_vencimiento = certificado.not_valid_after
        if (fecha_actual > fecha_vencimiento):
            return {
                "codigo": 1,
                "estado": "Certificado Vencido",
                
                "fecha_de_vencimiento": certificado.not_valid_after.strftime("%d/%m/%Y"),
                
                
            }   
        return None
    
    def validacion_revocacion(self, certificado_base64):
        issuer = 'i.pem'
        cert = normalize_pem(certificado_base64)
        name_certificate = "test"
        write_ceritficate(name_certificate,cert)
        ocsp_url = 'http://ocsp1.uanataca.com/public/pki/ocsp'
        args = ['openssl', 'ocsp', '-issuer', issuer, '-cert', f"src/certificates/{name_certificate}.pem", '-text', '-url', ocsp_url]

        # Ejecutar el comando de OpenSSL
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = p.communicate()

        # Buscar la línea que contiene "Revocation Time"
        revocation_time_line = [line for line in output.decode('utf-8').split('\n') if 'Revocation Time' in line]

        # Obtener el valor de la revocación
        if len(revocation_time_line) > 0:
            revocation_time = revocation_time_line[0].split(': ')[1].strip()
            date_revoked = parse(revocation_time)
            print(revocation_time)
            return {
                    "codigo": 2,
                    "estado": "Certificado Revocado",
                    "fecha de revocacion": date_revoked.strftime("%d/%m/%Y"),
                    
                }
   
        return None
        
        