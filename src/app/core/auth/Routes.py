from fastapi import APIRouter, Path, status, Response, HTTPException
from .model import User
from ...Utils.models import ResponseSchema
from ...Utils.auth import signJWT
from .Controller import LoginController
from requests import post
from os import getenv

router = APIRouter(
    prefix="/login",
    tags=["login"]
)
@router.post(path="", response_model=ResponseSchema, response_model_exclude_none=True)
async def register_user(data: User):
    try:
        user_created = await LoginController.register(data)

        # generate token
        # token = signJWT(user_created.username)
        # sign_out = SignToken(token=token, user=dict(user_created))

        if user_created is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An unexpected error occurred"
            )
        elif user_created == 1:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="The user already exist"
            )

    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        return Response(ResponseSchema(detail="An unexpected error occurred").model_dump_json(), status_code=status.HTTP_400_BAD_REQUEST, media_type="application/json")
    else:
        return Response(ResponseSchema(detail="Successfully created, check your email", result=data).model_dump_json(), status_code=status.HTTP_201_CREATED, media_type="application/json")