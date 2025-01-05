from fastapi import APIRouter, Path, status, Response, HTTPException
from .model import User, UserDTO
from ...Utils.models import ResponseSchema
from .Services import UserService

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@router.get(path="", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_all():
    try:
        data = await UserService.get_all()

        if data is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error retreiving data"
            )
        elif data == []:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No users registered"
            )

    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        return Response(ResponseSchema(detail="Error retreiving data").model_dump_json(), status_code=status.HTTP_400_BAD_REQUEST, media_type="application/json")
    else:
        return Response(ResponseSchema(detail="Successfully retreived", result=data).model_dump_json(), status_code=status.HTTP_200_OK, media_type="application/json")

@router.get(path="/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_user(id: str = Path(..., alias="id")):
    try:
        data = await UserService.get_user(int(id, 10))

        if data is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error retreiving data"
            )
        elif data == []:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No users registered"
            )

    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        return Response(ResponseSchema(detail="Error retreiving data").model_dump_json(), status_code=status.HTTP_400_BAD_REQUEST, media_type="application/json")
    else:
        return Response(ResponseSchema(detail="Successfully retreived", result=data).model_dump_json(), status_code=status.HTTP_200_OK, media_type="application/json")

@router.post(path="", response_model=ResponseSchema, response_model_exclude_none=True)
async def create_user(data: UserDTO):
    try:
        user_created = await UserService.create(data)

        # API_EMAIL = getenv("API_EMAIL")

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
        # else:
            # email_data = {'email': user_created.email, 'message': f'{
                # user_created.username}, le damos la bienvenida al sistema de gestión de imágenes'}
            # call email service
            # email_response = post(f'{API_EMAIL}/email', json=email_data)
            # if email_response.status_code != 200:
            #     raise HTTPException(
            #         status_code=status.HTTP_409_CONFLICT,
            #         detail="The user was created but the email was unable to sent"
            #     )

    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        return Response(ResponseSchema(detail="An unexpected error occurred").model_dump_json(), status_code=status.HTTP_400_BAD_REQUEST, media_type="application/json")
    else:
        return Response(ResponseSchema(detail="Successfully created, check your email", result=user_created).model_dump_json(), status_code=status.HTTP_201_CREATED, media_type="application/json")

@router.put(path="/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def update_user(data: UserDTO, id: str = Path(..., alias="id")):
    try:
        user_updated = await UserService.update(data, int(id, 10))

        if user_updated is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An unexpected error occurred"
            )
        elif user_updated == 1:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The user does not exist"
            )

    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        return Response(ResponseSchema(detail="An unexpected error occurred").model_dump_json(), status_code=status.HTTP_400_BAD_REQUEST, media_type="application/json")
    else:
        return Response(ResponseSchema(detail="Successfully created, check your email", result=user_updated).model_dump_json(), status_code=status.HTTP_200_OK, media_type="application/json")

@router.delete(path="/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def delete_user(id: str = Path(..., alias="id")):
    try:
        user_deleted = await UserService.delete(int(id, 10))

        if user_deleted is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An unexpected error occurred"
            )
        elif user_deleted == 1:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The user does not exist"
            )
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        return Response(ResponseSchema(detail="An unexpected error occurred").model_dump_json(), status_code=status.HTTP_400_BAD_REQUEST, media_type="application/json")
    else:
        return Response(ResponseSchema(detail="Successfully deleted", result=True).model_dump_json(), status_code=status.HTTP_200_OK, media_type="application/json")