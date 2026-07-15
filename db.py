from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = (
    "mysql+pymysql://root:ANCAhsuYI13Vtk43@gateway01.ap-northeast-1.prod.aws.tidbcloud.com:4000/test?ssl_verify_cert=true&ssl_verify_identity=true"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base() 