from fastapi import FastAPI
from olt_config import olt_router
from ont_config import ont_router
from traffic_status import traffic_router
from debug_mode import debug_router

app = FastAPI()

# Include OLT & ONT routers
app.include_router(olt_router, prefix="/olt", tags=["OLT"])
app.include_router(ont_router, prefix="/ont", tags=["ONT"])
app.include_router(traffic_router, prefix="/traffic", tags=["TRAFFIC"])
app.include_router(debug_router, prefix="/debug", tags=["DEBUG"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
