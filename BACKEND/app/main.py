from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine

from app.routes.alert import router as alert_router
from app.routes.auth import router as auth_router
from app.routes.medicine import router as medicine_router
from app.routes.notification import router as notification_router
from app.routes.report import router as report_router
from app.routes.scan import router as scan_router


app = FastAPI(
    title="SwasthLink API",
    version="1.0.0",
    swagger_ui_parameters={
        "persistAuthorization": True,
    },
)

app.include_router(auth_router)
app.include_router(medicine_router)
app.include_router(scan_router)
app.include_router(report_router)
app.include_router(alert_router)
app.include_router(notification_router)


@app.get("/api/health")
def health_check():

    with engine.connect() as connection:
        database_name = connection.execute(
            text("SELECT current_database()")
        ).scalar()

    return {
        "status": "healthy",
        "database": database_name,
    }