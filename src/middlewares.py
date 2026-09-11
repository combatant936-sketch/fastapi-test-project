from fastapi import status
from fastapi.responses import JSONResponse
from time import time
from fastapi import Request
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import logging

logger=logging.getLogger("uvicorn.access")
logging.disable=True

def register_middlewares(app: FastAPI):
    @app.middleware("http")
    async def custom_logging(request: Request, call_next):
        start_time = time()
        print(f"before request {start_time}")

        response = await call_next(request)
        processed_time=time() - start_time
        print(f"{request.client.host}:{request.client.port} - {request.method} - {request.url.path} - {response.status_code} - processed time {processed_time}")

        return response
    
    


    # @app.middleware("http")
    # async def authorization(request: Request, call_next):
    #     if not "Authorization" in request.headers:
    #         return JSONResponse(content={"error":"Asds"},status_code=status.HTTP_401_UNAUTHORIZED)

    #     response = await call_next(request)

    #     return response

    app.add_middleware(CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials = False,
    
    )

    app.add_middleware(TrustedHostMiddleware,
            allowed_hosts= ["localhost","127.0.0.1","fastapi-book-api-vimc.onrender.com"],
    
    )
        