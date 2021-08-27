import os

# https://dev.to/nestedsoftware/flask-and-sqlalchemy-without-the-flask-sqlalchemy-extension-3cf8

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from alembic.config import Config
from alembic import command

# We need to import all the models in order for them to be add to the Base.
# pylint: disable=unused-import
from .models import TABLE_NAME_MAP
from .base import Base


ALEMBIC_CFG = Config(os.path.abspath(
    os.path.dirname(__file__)) + "/alembic.ini")


def generate_models(database_uri, echo=False):
    """
    Generate database tables for the given database URI.

    In all cases, this should only be ran on a newly created database!
    The assumption is that all the available models will be created in
    their current state in this module, and that state corresponds to HEAD
    as in `alembic/versions`
    """
    engine = create_engine(database_uri, echo=echo)

    # add extensions
    engine.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    engine.execute('CREATE EXTENSION IF NOT EXISTS "citext";')

    session = sessionmaker(bind=engine)
    db_session = scoped_session(session)

    # Adds Query Property to Models - enables `User.query.query_method()`
    Base.query = db_session.query_property()

    # Create Tables
    Base.metadata.create_all(engine)
    # for table_name, table in Base.metadata.tables.items():

    # Stamp newly initialized schema as current head
    with engine.begin() as connection:
        ALEMBIC_CFG.set_main_option('sqlalchemy.url', database_uri)
        ALEMBIC_CFG.attributes['connection'] = connection  # pylint: disable=E1137
        ALEMBIC_CFG.set_main_option('script_location', os.path.abspath(
            os.path.dirname(__file__)) + "/alembic")
        command.stamp(ALEMBIC_CFG, "head")
