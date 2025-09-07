from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import DB_URL

# Base model cho ORM
Base = declarative_base()

# Tạo engine (pool_pre_ping để check connection khỏe)
# Chỉ tạo engine khi DB_URL có sẵn
engine = None
SessionLocal = None

def get_engine():
    global engine
    if engine is None:
        if not DB_URL:
            raise RuntimeError("DATABASE_URL is not set. Please configure it in Railway Variables.")
        engine = create_engine(
            DB_URL,
            pool_pre_ping=True,  # giúp tránh lỗi connection drop
            connect_args={"check_same_thread": False} if DB_URL.startswith("sqlite") else {}
        )
    return engine

def get_session_local():
    global SessionLocal
    if SessionLocal is None:
        engine = get_engine()
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal

# Dependency để inject DB session vào route
def get_db():
    session_local = get_session_local()
    db = session_local()
    try:
        yield db
    finally:
        db.close()