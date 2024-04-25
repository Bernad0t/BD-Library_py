from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine, String
from config import settings
from typing import Annotated

engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    #echo=True,
    # pool_size=5,
    # max_overflow=10,
)

session = sessionmaker(engine)

date_issue = 30

str_256 = Annotated[str, 256]
class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)
    }




# with engine.connect() as conn:
#     res = conn.execute(text("SELECT VERSION()"))
#     print(res)