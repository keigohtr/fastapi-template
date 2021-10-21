"""
Test DB session.
"""
import os

from sqlalchemy import create_engine

DB_HOST = os.environ["TEST_DB_HOST"]
DB_USER = os.environ["TEST_DB_USER"]
DB_PASSWORD = os.environ["TEST_DB_PASSWORD"]


def build_uri(db_name: str):
    return f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{db_name}?charset=utf8"


def get_engine(db_name: str):
    return create_engine(build_uri(db_name), pool_pre_ping=True)
