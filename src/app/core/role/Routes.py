from fastapi import APIRouter, Path, status, Response, HTTPException
from .model import Role, RoleDTO
from ...Utils.models import ResponseSchema
from .Services import RoleService

router = APIRouter(
    prefix="/role",
    tags=["role"]
)

@router.get(path="", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_all():
    try:
        data = await RoleService.get_all()

        if data is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error retreiving data"
            )
        elif data == []:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No roles registered"
            )

    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        return Response(ResponseSchema(detail="Error retreiving data").model_dump_json(), status_code=status.HTTP_400_BAD_REQUEST, media_type="application/json")
    else:
        return Response(ResponseSchema(detail="Successfully retreived", result=data).model_dump_json(), status_code=status.HTTP_200_OK, media_type="application/json")

@router.get(path="/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_role(id: str = Path(..., alias="id")):
    try:
        data = await RoleService.get_role(int(id, 10))

        if data is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error retreiving data"
            )
        elif data == []:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No roles registered"
            )

    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        return Response(ResponseSchema(detail="Error retreiving data").model_dump_json(), status_code=status.HTTP_400_BAD_REQUEST, media_type="application/json")
    else:
        return Response(ResponseSchema(detail="Successfully retreived", result=data).model_dump_json(), status_code=status.HTTP_200_OK, media_type="application/json")

@router.post(path="", response_model=ResponseSchema, response_model_exclude_none=True)
async def create_role(data: RoleDTO):
    try:
        role_created = await RoleService.create(data)

        if role_created is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An unexpected error occurred"
            )
        elif role_created == 1:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="The role already exist"
            )

    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        return Response(ResponseSchema(detail="An unexpected error occurred").model_dump_json(), status_code=status.HTTP_400_BAD_REQUEST, media_type="application/json")
    else:
        return Response(ResponseSchema(detail="Successfully created, check your email", result=role_created).model_dump_json(), status_code=status.HTTP_201_CREATED, media_type="application/json")

@router.put(path="/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def update_role(data: RoleDTO, id: str = Path(..., alias="id")):
    try:
        role_updated = await RoleService.update(data, int(id, 10))

        if role_updated is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An unexpected error occurred"
            )
        elif role_updated == 1:
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
        return Response(ResponseSchema(detail="Successfully created, check your email", result=role_updated).model_dump_json(), status_code=status.HTTP_200_OK, media_type="application/json")

@router.delete(path="/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def delete_role(id: str = Path(..., alias="id")):
    try:
        role_deleted = await RoleService.delete(int(id, 10))

        if role_deleted is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An unexpected error occurred"
            )
        elif role_deleted == 1:
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