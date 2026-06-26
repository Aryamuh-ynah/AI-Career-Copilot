from sqlalcemy import create_engine
from sqlalcemy.orm import declarative_base, sessionmaker

DATABASE_URL="ADD your Database link from TuDB"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={
        "ssl":{
            "ssl": True
        }
    }
)
SassionLocal = sessionmaker(bind=endine)
Base = declarative_base()