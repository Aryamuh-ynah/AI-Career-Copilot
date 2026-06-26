from sqlalcemy import create_engine
from sqlalcemy.orm import declarative_base, sessionmaker

DATABASE_URL="mysql+mysqldb://JErV3tVdcUsDnzj.root:<PASSWORD>@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/sys?ssl_mode=VERIFY_IDENTITY&ssl_ca=<CA_PATH>"

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