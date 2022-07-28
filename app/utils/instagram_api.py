from instagrapi import Client
from instagrapi.types import User, Media
from core.config import settings

# Коннектим клиент сразу, чтобы на каждом запросе не авторизоваться и не нагружать
client = Client()
client.login(settings.INSTAGRAM_LOGIN, settings.INSTAGRAM_PASSWORD)


class InstagramApi:
    @staticmethod
    def get_profile(username: str) -> User:
        return client.user_info_by_username_v1(username=username)

    @staticmethod
    def get_profile_posts(profile: User) -> list[Media]:
        user_id = client.user_id_from_username(username=profile.username)
        return client.user_medias(int(user_id))

    @staticmethod
    def get_profile_posts_count(posts: list[Media]) -> int:
        return len(posts)

    @staticmethod
    def get_average_likes_count(posts: list[Media]) -> float:
        likes_count = 0
        posts_count = 0
        for post in posts:
            likes_count += post.like_count
            posts_count += 1

        if posts_count == 0:
            return likes_count

        return likes_count / posts_count

    @staticmethod
    def get_profile_subscribers_count(profile: User) -> int:
        return profile.follower_count


instagram_parser = InstagramApi()
