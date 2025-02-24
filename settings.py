from envparse import Env

env = Env()

SYNC_REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default="postgresql+psycopg2://postgres:postgres@localhost:5431/postgres"
)

ASYNC_REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default="postgresql+asyncpg://postgres:postgres@localhost:5431/postgres"
)