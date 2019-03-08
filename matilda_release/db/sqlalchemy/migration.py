import logging
import os

from migrate import exceptions as versioning_exceptions
from migrate.versioning import api as versioning_api
from migrate.versioning.repository import Repository
import sqlalchemy

from matilda_release.db.sqlalchemy import api as db_session
#from css.i18n import _

INIT_VERSION = {}
INIT_VERSION['matilda_release'] = 0
_REPOSITORY = {}

LOG = logging.getLogger(__name__)


def get_engine(database='matilda_release', context=None):
    if database == 'matilda_release':
        return db_session.get_engine()


def db_sync(version=None, database='matilda_release', context=None):
    if version is not None:
        try:
            version = int(version)
        except ValueError:
            raise Exception("version should be an integer")

    current_version = db_version(database, context=context)
    repository = _find_migrate_repo(database)
    if version is None or version > current_version:
        return versioning_api.upgrade(get_engine(database, context=context),
                                      repository, version)
    else:
        return versioning_api.downgrade(get_engine(database, context=context),
                                        repository, version)


def db_version(database='matilda_release', context=None):
    repository = _find_migrate_repo(database)
    try:
        return versioning_api.db_version(get_engine(database, context=context),
                                         repository)
    except versioning_exceptions.DatabaseNotControlledError as exc:
        meta = sqlalchemy.MetaData()
        engine = get_engine(database, context=context)
        meta.reflect(bind=engine)
        tables = meta.tables
        if len(tables) == 0:
            db_version_control(INIT_VERSION[database],
                               database,
                               context=context)
            return versioning_api.db_version(
                        get_engine(database, context=context), repository)
        else:
            LOG.exception(exc)
            # Some pre-Essex DB's may not be version controlled.
            # Require them to upgrade using Essex first.
            raise Exception("Upgrade DB using Essex release first.")


def db_initial_version(database='matilda_release'):
    return INIT_VERSION[database]


def db_version_control(version=None, database='matilda_mgmt', context=None):
    repository = _find_migrate_repo(database)
    versioning_api.version_control(get_engine(database, context=context),
                                   repository,
                                   version)
    return version


def _find_migrate_repo(database='matilda_release'):
    """Get the path for the migrate repository."""
    global _REPOSITORY
    rel_path = 'migrate_repo'
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                        rel_path)
    assert os.path.exists(path)
    if _REPOSITORY.get(database) is None:
        _REPOSITORY[database] = Repository(path)
    return _REPOSITORY[database]