from fastapi import FastAPI
import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware


from src.routes.validacion import validacion
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(validacion)
# scheduler = BackgroundScheduler()


def descargar_crl(url, crl_name):
    res = requests.get(url)
    print(res)
    f = open(f"{crl_name}.crl", "wb")
    f.write(res.content)
    f.close()
    log = open(f"{crl_name}.txt", "a+", encoding="utf-8")
    today = datetime.now()
    log.write(f"Sé descargó crl -> {today} ")
    log.write(str("\n"))
    log.close()


def trigger_descargar_crl():
    crl_url_prod = "http://crl1.uanataca.com/public/pki/crl/CCGT.crl"
    crl_url_sandbox = "http://crl1.sandbox.uanataca.com/public/pki/crl/CCGT.crl"
    descargar_crl(crl_url_prod, "CCGCRL")
    descargar_crl(crl_url_sandbox, "CCGCRL_Sandbox")


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.on_event("startup")
async def startup_event():
    trigger_descargar_crl()
    scheduler = BackgroundScheduler()
    scheduler.add_job(trigger_descargar_crl, 'interval',
                      seconds=30, max_instances=1)
    scheduler.start()
