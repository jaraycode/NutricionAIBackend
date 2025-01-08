from fastapi import APIRouter, Path, status, Response, HTTPException
from .model import FoodDTO
from ...Utils.models import ResponseSchema
from .Services import FoodService

router = APIRouter(
    prefix="/food",
    tags=["food"]
)

@router.get(path="", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_all():
    try:
        data = await FoodService.get_all()

        if data is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error retreiving data"
            )
        elif data == []:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No food registered"
            )

    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        return Response(ResponseSchema(detail="Error retreiving data").model_dump_json(), status_code=status.HTTP_400_BAD_REQUEST, media_type="application/json")
    else:
        return Response(ResponseSchema(detail="Successfully retreived", result=data).model_dump_json(), status_code=status.HTTP_200_OK, media_type="application/json")

@router.get(path="/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_food(id: str = Path(..., alias="id")):
    try:
        data = await FoodService.get_food(int(id, 10))

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

@router.post(path="/image", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_food_by_image(img):
    try:
        data = await FoodService.get_food_by_image(img=img)

        if data is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error retreiving data"
            )
        elif data == []:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No food found"
            )

    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        return Response(ResponseSchema(detail="Error retreiving data").model_dump_json(), status_code=status.HTTP_400_BAD_REQUEST, media_type="application/json")
    else:
        return Response(ResponseSchema(detail="Successfully retreived", result=data).model_dump_json(), status_code=status.HTTP_200_OK, media_type="application/json")

@router.post(path="", response_model=ResponseSchema, response_model_exclude_none=True)
async def create_food(data: FoodDTO):
    try:
        food_created = await FoodService.create(data)

        if food_created is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An unexpected error occurred"
            )
        elif food_created == 1:
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
        return Response(ResponseSchema(detail="Successfully created, check your email", result=food_created).model_dump_json(), status_code=status.HTTP_201_CREATED, media_type="application/json")

@router.put(path="/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def update_role(data: FoodDTO, id: str = Path(..., alias="id")):
    try:
        food_updated = await FoodService.update(data, int(id, 10))

        if food_updated is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An unexpected error occurred"
            )
        elif food_updated == 1:
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
        return Response(ResponseSchema(detail="Successfully created, check your email", result=food_updated).model_dump_json(), status_code=status.HTTP_200_OK, media_type="application/json")

@router.delete(path="/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def delete_role(id: str = Path(..., alias="id")):
    try:
        food_deleted = await FoodService.delete(int(id, 10))

        if food_deleted is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An unexpected error occurred"
            )
        elif food_deleted == 1:
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