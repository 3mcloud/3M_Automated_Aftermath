import os
import logging

from dotenv import load_dotenv
import sqlalchemy
from sqlalchemy import engine

from helpers.mdb_to_pandas import mdb_to_pandas
from files import files as FILES

load_dotenv()

log = logging.getLogger(__name__)

DB_ENDPOINT = os.getenv('DB_ENDPOINT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('SQLALCHEMY_DATABASE_USER')
DB_PASS = os.getenv('SQLALCHEMY_DATABASE_PASS')
DB_PORT = 5432


def get_uri(db_username: str, db_password: str) -> str:
    """
    Return database URI
    """
    return f"postgresql://{db_username}:{db_password}@{DB_ENDPOINT}:{DB_PORT}/{DB_NAME}"


def create_engine(db_username: str, db_password: str):
    return sqlalchemy.create_engine(get_uri(db_username, db_password))


def load_db_file(file_path: os.PathLike, year: int, tables_of_interest: list[bytes]):
    tables = mdb_to_pandas(file_path, tables_of_interest=tables_of_interest)
    type(tables)

    with engine.connect() as conn:
        for table in tables:
            print(table)
            tables[table].to_sql(
                name=f'{year}_staging_{table}'.lower(),
                con=conn,
                if_exists='replace')


if __name__ == "__main__":
    log.info("testing connection to postgres")
    engine = create_engine(DB_USER, DB_PASS)

    for file in FILES:
        load_db_file(
            file_path=os.path.join(os.path.dirname(
                __file__), "data/", file['file_name']),
            year=file['year'],
            tables_of_interest=file['tables_of_interest']
        )
