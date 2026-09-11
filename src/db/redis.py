import redis.asyncio as aioredis
from src.config import getsetting

set = getsetting()

# token_blocklist = aioredis.Redis(
#     host=set.REDIS_HOST,
#     port=set.REDIS_PORT,
#     db=0
# )

token_blocklist = aioredis.from_url(set.REDIS_URL)

JTI_EXPIRY = 3600

async def add_jti_to_token_blocklist(jti: str) -> None:
    await token_blocklist.set(name=jti, value="", ex=JTI_EXPIRY)

async def jti_in_token_blocklist(jti: str) -> bool:
    jti = await token_blocklist.get(jti)
    return jti is not None

