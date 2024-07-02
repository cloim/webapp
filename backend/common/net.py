import socket

from fastapi.responses import JSONResponse
from starlette.requests import Request

from common.util import is_json


async def get_json_body(request: Request):
	method = str(request.method)
	content_type = request.headers.get("Content-Type")

	if method == 'POST' or method == 'PUT' or method == 'PATCH':
		if content_type == "application/json":
			body = await request.body()
			body_str = body.decode("utf-8")
			if is_json(body_str):
				data = await request.json()
			else:
				data = dict((itm.split('=')[0],itm.split('=')[1]) for itm in body_str.split('&'))
			return data
	return None


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('192.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def create_response(status_code: int, message: str = "", data: dict = None):
    return JSONResponse(
		{
			"result": "OK" if status_code == 200 else "FAIL",
			"message": message,
   			"data": data
		},
		status_code=status_code
	)
