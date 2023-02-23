import base64
import json

import aiohttp
from cryptography import x509


class Certificado:

    async def descargar_certificado(self, username: str, password: str):
        headers = {"content-type": "application/json"}
        url_uanataca_signcloud = "https://cryptoapi.uanataca.com/api/get_objects"
        credenciales = {
            "username": username,
            "password": password,
            "type": None,
            "identifier": "DS0"
        }
        credenciales_json = json.dumps(credenciales)
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(url=url_uanataca_signcloud, data=credenciales_json) as response:
                return [response.status, await response.text()]

    async def obtener_cerficado_crl(self, username: str, password: str):
        status, res = await self.descargar_certificado(username, password)
        if status == 200:

            certificado_base64 = json.loads(res)["result"][1]["data"]
            certificado_decodificado = base64.b64decode(certificado_base64)
            try:
                certificado = x509.load_der_x509_certificate(
                    certificado_decodificado)

                return certificado

            except ValueError:
                certificado_base64 = json.loads(res)["result"][0]["data"]
                certificado_decodificado = base64.b64decode(certificado_base64)

                certificado = x509.load_der_x509_certificate(
                    certificado_decodificado)
                return certificado

        # validacion de certificado no existente
        elif status == 403:
            return {
                "codigo": 5,
                "estado": "Usuario Inválido"
            }
        # validacion de certificado password incorrecto
        elif status == 401:
            return {
                "codigo": 6,
                "estado": "Contraseña Incorrecta"
            }
        elif status == 420:
            return {
                "codigo": 7,
                "estado": "La última autenticación falló, intenteló en un momento."
            }

    async def obtener_cerficado_ocsp(self, username: str, password: str):
        status, res = await self.descargar_certificado(username, password)
        
        
        if status == 200:
           
            certificado_base64 = json.loads(res)["result"][1]["data"]
            certificado_decodificado = base64.b64decode(
                certificado_base64)
            try:
                certificado = x509.load_der_x509_certificate(
                    certificado_decodificado)

                return [certificado, certificado_base64]

            except ValueError:
                certificado_base64 = json.loads(
                    res)["result"][0]["data"]
                certificado_decodificado = base64.b64decode(
                    certificado_base64)
                certificado = x509.load_der_x509_certificate(
                    certificado_decodificado)
                return [certificado, certificado_base64]

        # validacion de certificado no existente
        elif status == 403:
            return [{
                "codigo": 5,
                "estado": "Usuario Inválido"
            }, None]
        # validacion de certificado password incorrecto
        elif status == 401:
            return [{
                "codigo": 6,
                "estado": "Contraseña Incorrecta"
            }, None]
        elif status == 420:
            return [{
                "codigo": 7,
                "estado": "La última autenticación falló, intenteló en un momento."
            }, None]
