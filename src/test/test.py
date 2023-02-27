import aiohttp
import json
import asyncio
host = "192.168.1.240"
url = f"http://{host}:8000/crl"


async def send_request(session, credentials):
    headers = {"content-type": "application/json"}
    credenciales_json = json.dumps(credentials)
    async with session.post(url=url, data=credenciales_json, headers=headers) as response:
        print("Respuesta", await response.text(), "Credenciales", credentials)


async def main():
    credentials = [
        {
            "username": "4343983",
            "password": "n7dn37yB",
            "env":      "prod"
        },
        {
            "username": "4348167",
            "password": "T,_94VFK",
            "env": "prod"
        },
        {
            "username": "4344166",
            "password": "!b68P3J6",
            "env": "prod"
        },
        {
            "username": "4340584",
            "password": "n2F3Y!n4",
            "env": "prod"
        },

        {
            "username": "4343983",
            "password": "n7dn37yB",
            "env": "prod"
        },
        {
            "username": "4348167",
            "password": "T,_94VFK",
            "env": "prod"
        },
        {
            "username": "4344166",
            "password": "!b68P3J6",
            "env": "prod"
        },
        {"username": "4340584",
         "password": "n2F3Y!n4",
         "env": "prod"
         },

        {
            "username": "4343983",
            "password": "n7dn37yB",
            "env": "prod"
        },
        {
            "username": "4348167",
            "password": "T,_94VFK",
            "env": "prod"
        },
        {
            "username": "4344166",
            "password": "!b68P3J6",
            "env": "prod"
        },
        {
            "username": "4340584",
            "password": "n2F3Y!n4",
            "env": "prod"
         },

        {
            "username": "4343983",
            "password": "n7dn37yB",
            "env": "prod"
        },
        {
            "username": "4348167",
            "password": "T,_94VFK",
            "env": "prod"
        },
        {
            "username": "4344166",
            "password": "!b68P3J6",
            "env": "prod"
        },
        {
            "username": "4340584",
            "password": "n2F3Y!n4",
            "env": "prod"
        },
    ]
    print(len(credentials))

    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session, c) for c in credentials]

        await asyncio.gather(*tasks)


asyncio.run(main())