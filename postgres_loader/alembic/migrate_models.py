import os
import logging

# https://dev.to/nestedsoftware/flask-and-sqlalchemy-without-the-flask-sqlalchemy-extension-3cf8

from sqlalchemy import create_engine

from alembic.config import Config
from alembic import command

# We need to import all the models in order for them to be add to the Base.
# pylint: disable=unused-import
from .models import TABLE_NAME_MAP
from .base import Base


ALEMBIC_CFG = Config(os.path.abspath(
    os.path.dirname(__file__)) + "/alembic.ini")

logging.getLogger('alembic').setLevel(logging.DEBUG)


def migrate_models(database_uri, echo=False):
    """
    Migrate database tables for the given database URI to HEAD.
    Related: https://github.com/pallets/flask-sqlalchemy/pull/250#issuecomment-377080229
    """
    engine = create_engine(database_uri, echo=echo)

    with engine.begin() as connection:
        ALEMBIC_CFG.set_main_option('sqlalchemy.url', database_uri)
        ALEMBIC_CFG.attributes['connection'] = connection  # pylint: disable=E1137
        ALEMBIC_CFG.set_main_option('script_location', os.path.abspath(
            os.path.dirname(__file__)) + "/alembic")
        command.current(ALEMBIC_CFG, verbose=True)
        command.branches(ALEMBIC_CFG, verbose=True)
        command.upgrade(ALEMBIC_CFG, "head")


def downgrade_models_to_revision(database_uri, revision: str, echo=False):
    """
    Downgrade database tables for the given database URI to a specific revision.
    Related: https://github.com/pallets/flask-sqlalchemy/pull/250#issuecomment-377080229

    Args:
        database_uri [str]: PostgreSQL connection string to target database
        revision [str]: Target migration revision ID to downgrade database to

    Returns:
        None
    """
    engine = create_engine(database_uri, echo=echo)

    with engine.begin() as connection:
        ALEMBIC_CFG.set_main_option('sqlalchemy.url', database_uri)
        ALEMBIC_CFG.attributes['connection'] = connection  # pylint: disable=E1137
        ALEMBIC_CFG.set_main_option('script_location', os.path.abspath(
            os.path.dirname(__file__)) + "/alembic")
        command.current(ALEMBIC_CFG, verbose=True)
        command.branches(ALEMBIC_CFG, verbose=True)
        command.downgrade(ALEMBIC_CFG, revision)