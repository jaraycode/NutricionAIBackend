from fastapi import APIRouter, Path, status, Response, HTTPException, Depends
from .model import LogInDTO
from ..users.model import UserDTO
from ...Utils.models import ResponseSchema
from .Services import LoginService

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post(path="/register", response_model=ResponseSchema, response_model_exclude_none=True)
async def register_user(data: UserDTO):
    try:
        user_registed = await LoginService.register(data)

        # generate token
        # token = signJWT(user_logged.username)
        # sign_out = SignToken(token=token, user=dict(user_logged))

        if user_registed is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An unexpected error occurred"
            )
        elif user_registed == 1:
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
        return Response(ResponseSchema(detail="Successfully created", result=user_registed).model_dump_json(), status_code=status.HTTP_201_CREATED, media_type="application/json")


@router.post(path="/login", response_model=ResponseSchema, response_model_exclude_none=True)
async def login(data: LogInDTO):
    try:
        user_logged = await LoginService.logIn(data)

        # generate token
        # token = signJWT(user_logged.username)
        # sign_out = SignToken(token=token, user=dict(user_logged))

        if user_logged is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An unexpected error occurred"
            )
        elif user_logged == 1:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The user email could not be found"
            )
        elif user_logged == 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid password"
            )

    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        return Response(ResponseSchema(detail="An unexpected error occurred").model_dump_json(), status_code=status.HTTP_400_BAD_REQUEST, media_type="application/json")
    else:
        return Response(ResponseSchema(detail="Successfully logged in", result=user_logged).model_dump_json(), status_code=status.HTTP_201_CREATED, media_type="application/json")