"""
Initializing API server
"""
import http
from typing import Any, Callable, Optional

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app import entities
from app.apis import health
from app.apis.api_v1.router import v1_router
from app.entities.message import MessageCodeEnum
from app.exceptions import ApiError
from app.logger import logger
from app.services.book_service import BookService


def configure_app(book_service: BookService) -> FastAPI:
    api = FastAPI(title="FastAPI template")
    api.include_router(health.router, tags=["health"])
    api.include_router(v1_router(book_service), prefix="/v1")

    @api.middleware("http")
    async def log_request(request: Request, call_next: Callable) -> Any:
        """Middleware for logging http request.
        Args:
            request:
            call_next:
        Returns:
            response:
        """
        payload = {
            "path": request.url.path,
            "method": request.method,
            "headers": request.headers,
            "queries": request.query_params,
            "client": request.client.host,
        }
        requester: Optional[str] = None
        if "x_requester" in request.headers.keys():
            requester = request.headers.get("x_requester")

        try:
            response = await call_next(request)
        except Exception as e:
            payload["status_code"] = http.HTTPStatus.INTERNAL_SERVER_ERROR
            logger.info(
                {
                    "message": "API request payload",
                    "requester": requester,
                    "payload": payload,
                }
            )
            raise e

        payload["status_code"] = response.status_code
        logger.info(
            {
                "message": "API request payload",
                "requester": requester,
                "payload": payload,
            }
        )
        return response

    @api.exception_handler(ApiError)
    async def api_error_handler(_: Request, exc: ApiError) -> JSONResponse:
        """ApiError"""
        message = entities.Message(code=exc.code, message=str(exc))
        return JSONResponse(status_code=exc.status_code, content=jsonable_encoder(message.dict()))

    @api.exception_handler(StarletteHTTPException)
    async def custom_http_exception_handler(_: Request, exc: StarletteHTTPException) -> JSONResponse:
        """HTTPException"""
        message = entities.Message(code=MessageCodeEnum.UNPROCESSABLE_ENTITY, message="", detail=exc.detail)
        headers = getattr(exc, "headers", None)
        if headers:
            return JSONResponse(status_code=exc.status_code, content=jsonable_encoder(message.dict()), headers=headers)
        return JSONResponse(status_code=exc.status_code, content=jsonable_encoder(message.dict()))

    @api.exception_handler(RequestValidationError)
    async def custom_request_validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
        """RequestValidationError"""
        message = entities.Message(code=MessageCodeEnum.UNPROCESSABLE_ENTITY, message="", detail=exc.errors())
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=jsonable_encoder(message.dict()))

    @api.exception_handler(Exception)
    async def default_exception_handler(_: Request, exc: Exception) -> JSONResponse:
        """Default exception handler"""
        message = entities.Message(code=MessageCodeEnum.INTERNAL_SERVER_ERROR, message=str(exc))
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(message.dict()))

    return api
