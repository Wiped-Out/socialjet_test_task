import aioredis
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import profiles
from core.config import settings
from db import cache_db
from services.base_cache import BaseRedisStorage

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    cache_db.cache = BaseRedisStorage(redis=await aioredis.create_redis_pool((
        settings.REDIS_HOST, settings.REDIS_PORT
    ), minsize=10, maxsize=20))


@app.on_event('shutdown')
async def shutdown():
    await cache_db.cache.close()


app.include_router(profiles.router, prefix='/api/v1/profiles', tags=['profiles'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8001,
    )
