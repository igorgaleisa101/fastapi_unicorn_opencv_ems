from functools import wraps
from fastapi import FastAPI
from starlette.requests import Request
from access import WHITELIST
# from mangum import Mangum
from utils import resolve_ip_list

from EMS.ems_tracking_service import EMSTrackingService
from GlobalTrack.global_track_service import GlobalTrackingService
from USPS.usps_track_service import USPSTrackingService

app = FastAPI()


# handler = Mangum(app)


@app.get("/")
def root():
    return {"message": "EMS API v2.0"}


def check_whitelist(func):
    def wrapper(request: Request, *args, **kwargs):
        if request.client.host not in WHITELIST:
            return {'success': False, 'msg': 'Access Denied!', 'your_ip': request.client.host}
        return func(request, *args, **kwargs)
    return wrapper

# Custom decorator to check whitelist
def protected(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        if request.client.host not in resolve_ip_list(WHITELIST):
            return {'success': False, 'msg': 'Access Denied!', 'your_ip': request.client.host}
        return await func(*args, **kwargs)

    return wrapper

@app.get("/ems/track")
def track_ems(request: Request, tracking_number: str, proxy: int = 0, lang: str = 'en'):
    # Check access
    if not request.client.host in WHITELIST:
        return {'success': False, 'msg': 'Access Denied!', 'your_ip': request.client.host}

    # Create an instance of tracking service
    ems_service = EMSTrackingService(proxy=proxy, lang=lang)

    # Get the results
    result = ems_service.get_tracking_result(tracking_number)
    return result


@app.get("/globaltracktrace/track")
def global_track_trace(request: Request, tracking_number: str, proxy: int = 0, session: int = 0):
    # Check access
    if not request.client.host in WHITELIST:
        return {'success': False, 'msg': 'Access Denied!', 'your_ip': request.client.host}

    # Create an instance of tracking service
    service = GlobalTrackingService(proxy=proxy, session_id=session)

    # Get the results
    result = service.get_tracking_result(tracking_number)
    return result


@app.get("/usps/track")
def usps(request: Request, tracking_number: str, proxy: int = 0):
    # Check access
    if not request.client.host in WHITELIST:
        return {'success': False, 'msg': 'Access Denied!', 'your_ip': request.client.host}

    # Create an instance of tracking service
    service = USPSTrackingService(proxy=proxy)

    # Get the results
    result = service.get_tracking_result(tracking_number)
    return result


@app.get("/whitelist")
@protected
def whitelist(request: Request):
    # Check access
    if not request.client.host in resolve_ip_list(WHITELIST):
        return {'success': False, 'msg': 'Access Denied!', 'your_ip': request.client.host}
    return WHITELIST

@app.get("/test")
@protected
def test(request: Request, proxy: int = 0, session: int = 0):
    ems_service = EMSTrackingService(proxy=proxy, session_id=session)
    result = ems_service.test_request()
    result['your_ip'] = request.client.host
    return result


