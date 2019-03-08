from matilda_release.db.sqlalchemy import migration as IMPL


def db_sync(version=None, database='matilda_mgmt'):
    return IMPL.db_sync(version=version, database=database)


def db_version(database='matilda_mgmt'):
    return IMPL.db_version(database=database)


def db_initial_version(database='matilda_mgmt'):
    return IMPL.db_initial_version(database=database)
