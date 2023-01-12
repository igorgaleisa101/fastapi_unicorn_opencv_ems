from fastapi import FastAPI
from ems_tracking_service import EMSTrackingService

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/ems/track")
async def track_ems(tracking_number: str):
    # Create an instance of EMSTrackingService
    ems_service = EMSTrackingService()

    # Get the captcha challenge and capcode
    result = ems_service.get_tracking_result(tracking_number)

    return result
