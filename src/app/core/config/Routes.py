from fastapi import APIRouter, Path, status, Response, HTTPException
from .model import ConfigDTO
from ...Utils.models import ResponseSchema
from .Services import ConfigService

router = APIRouter(
    prefix="/config",
    tags=["config"]
)

@router.get(path="", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_all():
    try:
        data = await ConfigService.get_all()

        if data is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error retreiving data"
            )
        elif data == []:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No config registered"
            )

    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        return Response(ResponseSchema(detail="Error retreiving data").model_dump_json(), status_code=status.HTTP_400_BAD_REQUEST, media_type="application/json")
    else:
        return Response(ResponseSchema(detail="Successfully retreived", result=data).model_dump_json(), status_code=status.HTTP_200_OK, media_type="application/json")

@router.get(path="/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_config(id: str = Path(..., alias="id")):
    try:
        data = await ConfigService.get_config(int(id, 10))

        if data is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error retreiving data"
            )
        elif data == []:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No config registered"
            )

    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        return Response(ResponseSchema(detail="Error retreiving data").model_dump_json(), status_code=status.HTTP_400_BAD_REQUEST, media_type="application/json")
    else:
        return Response(ResponseSchema(detail="Successfully retreived", result=data).model_dump_json(), status_code=status.HTTP_200_OK, media_type="application/json")

@router.post(path="", response_model=ResponseSchema, response_model_exclude_none=True)
async def create_food(data: ConfigDTO):
    try:
        config_created = await ConfigService.create(data)

        if config_created is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An unexpected error occurred"
            )
        elif config_created == 1:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="The config already exist"
            )

    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        return Response(ResponseSchema(detail="An unexpected error occurred").model_dump_json(), status_code=status.HTTP_400_BAD_REQUEST, media_type="application/json")
    else:
        return Response(ResponseSchema(detail="Successfully created, check your email", result=config_created).model_dump_json(), status_code=status.HTTP_201_CREATED, media_type="application/json")

@router.put(path="/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def update_food(data: ConfigDTO, id: str = Path(..., alias="id")):
    try:
        config_updated = await ConfigService.update(data, int(id, 10))

        if config_updated is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An unexpected error occurred"
            )
        elif config_updated == 1:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The role does not exist"
            )

    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        return Response(ResponseSchema(detail="An unexpected error occurred").model_dump_json(), status_code=status.HTTP_400_BAD_REQUEST, media_type="application/json")
    else:
        return Response(ResponseSchema(detail="Successfully created, check your email", result=config_updated).model_dump_json(), status_code=status.HTTP_200_OK, media_type="application/json")

@router.delete(path="/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def delete_food(id: str = Path(..., alias="id")):
    try:
        config_deleted = await ConfigService.delete(int(id, 10))

        if config_deleted is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An unexpected error occurred"
            )
        elif config_deleted == 1:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The role does not exist"
            )
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        return Response(ResponseSchema(detail="An unexpected error occurred").model_dump_json(), status_code=status.HTTP_400_BAD_REQUEST, media_type="application/json")
    else:
        return Response(ResponseSchema(detail="Successfully deleted", result=True).model_dump_json(), status_code=status.HTTP_200_OK, media_type="application/json")