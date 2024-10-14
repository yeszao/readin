from typing import Any

from flask import jsonify
from pydantic import BaseModel


class Json(BaseModel):
    data: Any = None
    message: str = "OK"

    @staticmethod
    def error(message: str, status_code: int = 400):
        return jsonify(Json(data=None, message=message).model_dump()), status_code

    @staticmethod
    def ok(data: Any = None, message: str = "OK"):
        return jsonify(Json(data=data, message=message).model_dump()), 200
