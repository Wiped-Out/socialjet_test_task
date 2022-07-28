from pydantic import BaseModel


class Profile(BaseModel):
    subscribers_count: int
    posts_count: int
    average_likes_count: float
