from functools import wraps
from fastapi import FastAPI
from starlette.requests import Request
from access import WHITELIST
# from mangum import Mangum
from utils import resolve_ip_list

from EMS.ems_tracking_service import EMSTrackingService

app = FastAPI()


# Custom decorator to check whitelist
def protected(func):
    @wraps(func)
    def wrapper(request: Request, *args, **kwargs):
        if request.client.host not in resolve_ip_list(WHITELIST):
            return {'success': False, 'msg': 'Access Denied!', 'your_ip': request.client.host}
        return func(request, *args, **kwargs)

    return wrapper


@app.get("/")
def root():
    return {"message": "EMS API v2.0"}


@app.get("/ems/track")
@protected
def track_ems(request: Request, tracking_number: str, proxy: int = 0, lang: str = 'en'):
    # Create an instance of tracking service
    ems_service = EMSTrackingService(proxy=proxy, lang=lang)

    # Get the results
    result = ems_service.get_tracking_result(tracking_number)
    return result

@app.get("/whitelist")
def whitelist(request: Request):
    return resolve_ip_list(WHITELIST)


@app.get("/test")
@protected
def test(request: Request, proxy: int = 0, session: int = 0):
    ems_service = EMSTrackingService(proxy=proxy, session_id=session)
    result = ems_service.test_request()
    result['your_ip'] = request.client.host
    return result


