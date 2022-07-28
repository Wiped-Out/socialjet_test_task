from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request

from api.answers.v1 import answers
from schemas.v1_schemas import Profile
from services.profiles import get_profile_service, ProfileService

router = APIRouter()


@router.get(
    path="/{username}",
    response_model=Profile,
    description="Get info about profile"
)
async def get_genre(
        username: str, request: Request,
        profile_service: ProfileService = Depends(get_profile_service)
) -> Profile:
    cache_key = f"{request.url.path}_{username=}"

    try:
        profile = await profile_service.get_profile(username=username, cache_key=cache_key)
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=answers.CANT_GET_PROFILE,
        )

    if not profile:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=answers.PROFILE_NOT_FOUND,
        )

    return Profile(**profile.dict())
