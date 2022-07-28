from functools import lru_cache
from typing import Optional

from fastapi import Depends

from db.cache_db import get_cache_db
from models.profile import Profile
from services.base_cache import BaseCacheStorage, AsyncCacheStorage
from utils.instagram_api import instagram_parser


class ProfileService(BaseCacheStorage):
    async def get_profile(
            self,
            username: str,
            cache_key: str
    ) -> Optional[Profile]:

        profile = await self.get_one_item_from_cache(cache_key=cache_key, model=Profile)

        if not profile:
            user = instagram_parser.get_profile(username=username)
            posts = instagram_parser.get_profile_posts(profile=user)

            profile = Profile(
                subscribers_count=instagram_parser.get_profile_subscribers_count(user),
                posts_count=instagram_parser.get_profile_posts_count(posts),
                average_likes_count=instagram_parser.get_average_likes_count(posts),
            )

            if profile:
                await self.put_one_item_to_cache(cache_key=cache_key, item=profile)

        return profile


@lru_cache()
def get_profile_service(
        cache: AsyncCacheStorage = Depends(get_cache_db),
) -> ProfileService:
    return ProfileService(cache=cache)
