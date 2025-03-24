from envparse import Env

env = Env()

SYNC_REAL_DATABASE_URL = env.str(
    "SYNC_DATABASE_URL",
    default="postgresql+psycopg2://postgres:postgres@localhost:5431/postgres"
)

ASYNC_REAL_DATABASE_URL = env.str(
    "ASYNC_DATABASE_URL",
    default="postgresql+asyncpg://postgres:postgres@localhost:5431/postgres"
)

# TEST_DATABASE_URL = env.str(
#     "TEST_DATABASE_URL",
#     default="postgresql+asyncpg://postgres_test:postgres_test@host.docker.internal:5429/postgres_test",
# )

TEST_DATABASE_URL = env.str(
    "TEST_DATABASE_URL",
    default="postgresql+asyncpg://postgres_test:postgres_test@localhost:5429/postgres_test",
)
SECRET_KEY_FOR_ACCESS: str = env.str(
    "SECRET_KEY_FOR_ACCESS", default="your-strong-access-secret-key"
)

ALGORITHM: str = env.str("ALGORITHM", default="HS256")

APP_PORT = env.int("APP_PORT", default=8000)