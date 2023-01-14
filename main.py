from fastapi import FastAPI
from EMS.ems_tracking_service import EMSTrackingService
# from mangum import Mangum


app = FastAPI()
# handler = Mangum(app)


@app.get("/")
async def root():
    return {"message": "EMS API v1.0"}


@app.get("/ems/track")
async def track_ems(tracking_number: str, proxy: int = 0, session: int = 0):
    # Create an instance of EMSTrackingService
    ems_service = EMSTrackingService(proxy=proxy, session_id=session)

    # Get the captcha challenge and capcode
    result = ems_service.get_tracking_result(tracking_number)
    return result

@app.get("/test")
async def test(proxy: int = 0, session: int = 0):
    ems_service = EMSTrackingService(proxy=proxy, session_id=session)
    result = ems_service.test_request()
    return result
