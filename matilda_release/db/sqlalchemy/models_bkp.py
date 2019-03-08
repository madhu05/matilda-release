import datetime

from oslo_config import cfg
from oslo_db.sqlalchemy import models
from sqlalchemy import (Column, String)
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import orm
from sqlalchemy import DateTime, Integer, Text, JSON

CONF = cfg.CONF
BASE = declarative_base()


def MediumText():
    return Text().with_variant(MEDIUMTEXT(), 'mysql')


class MatildaRlsBase(models.ModelBase):
    metadata = None

    def __copy__(self):
        session = orm.Session()

        copy = session.merge(self, load=False)
        session.expunge(copy)
        return copy

    def save(self, session=None):
        from matilda_release.db.sqlalchemy import api as db_api
        if session is None:
            session = db_api.get_session()

        super(MatildaRlsBase, self).save(session=session)

    def delete(self, session=None):
        from matilda_release.db.sqlalchemy import api as db_api
        if session is None:
            session = db_api.get_session()

        super(MatildaRlsBase, self).delete(session=session)

    def __repr__(self):
        items = ['%s=%r' % (col.name, getattr(self, col.name))
                 for col in self.__table__.columns]
        return "<%s.%s[object at %x] {%s}>" % (self.__class__.__module__,
                                               self.__class__.__name__,
                                               id(self), ','.join(items))

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class AppRelease(BASE, MatildaRlsBase):
    __tablename__ = 'app_release'

    app_release_id = Column(String(50), primary_key=True)
    release_id = Column(String(50))
    name = Column(String(50))
    project = Column(String(50))
    program = Column(String(50))
    application = Column(String(50))
    version = Column(String(20))
    status = Column(String(50))
    release_dt = Column(DateTime)
    comments = Column(Text)


class InfraRelease(BASE, MatildaRlsBase):
    __tablename__ = 'infra_release'

    infra_release_id = Column(String(50), primary_key=True)
    release_id = Column(String(50))
    name = Column(String(50))
    platform = Column(String(50))
    operating_system = Column(String(50))
    version = Column(String(50))
    source = Column(String(20))
    patch_version = Column(String(50))
    release_dt = Column(DateTime)
    comments = Column(Text)


class LinkType(BASE, MatildaRlsBase):
    __tablename__ = 'link_types'

    link_type_id = Column(Integer, primary_key=True)
    name = Column(String(50))
    type = Column(String(50))
    description = Column(String(50))
    fields = Column(JSON)


class Release(BASE, MatildaRlsBase):
    __tablename__ = 'release'

    release_id = Column(String(50), primary_key=True)
    release_type = Column(String(50))
    name = Column(String(50), nullable=False)
    description = Column(Text)
    status = Column(String(50))
    release_dt = Column(DateTime)

class ReleaseReqData(BASE, MatildaRlsBase):
    __tablename__ = 'release_req_data'

    id = Column(Integer, primary_key=True)
    req_id = Column(String(50))
    type = Column(String(50))
    req_data = Column(JSON)

class ReleaseCondition(BASE, MatildaRlsBase):
    __tablename__ = 'release_condition'

    condition_id = Column(Integer, primary_key=True)
    release_env_id = Column(String(50))
    type = Column(String(50))
    parameter = Column(String(50))
    environment = Column(String(50))
    value = Column(String(50))
    status = Column(DateTime)


class ReleaseEnv(BASE, MatildaRlsBase):
    __tablename__ = 'release_envs'

    release_env_id = Column(String(50), primary_key=True)
    release_id = Column(String(50))
    release_type = Column(String(50))
    release_type_id = Column(String(50))
    env_name = Column(String(50))
    env_type = Column(String(20))
    dependent_env = Column(String(50))
    status = Column(String(50))
    workflow_id = Column(String(50))
    stages = Column(Integer)
    create_dt = Column(DateTime)


class ReleaseExecution(BASE, MatildaRlsBase):
    __tablename__ = 'release_execution'

    id = Column(Integer, primary_key=True)
    release_env_id = Column(String(50))
    env_name = Column(String(50))
    start_dt = Column(DateTime)
    end_dt = Column(DateTime)
    status = Column(String(50))
    current_stage = Column(DateTime)


class ReleaseExecutionStat(BASE, MatildaRlsBase):
    __tablename__ = 'release_execution_stats'

    link_id = Column(String(50), primary_key=True)
    release_id = Column(String(50))
    release_type = Column(String(50))
    release_env_id = Column(String(50))
    total = Column(String(50))
    success = Column(String(50))
    fail = Column(String(50))
    in_progress = Column(String(50))
    pending = Column(String(50))
    last_updated = Column(DateTime)


class ReleaseLinkItem(BASE, MatildaRlsBase):
    __tablename__ = 'release_link_items'

    link_item_id = Column(Integer, primary_key=True)
    link_id = Column(String(50))
    value = Column(String(50))


class ReleaseLink(BASE, MatildaRlsBase):
    __tablename__ = 'release_links'

    link_id = Column(String(50), primary_key=True)
    release_id = Column(String(50))
    release_type = Column(String(50))
    type = Column(String(50))
    name = Column(String(50))
    source = Column(String(50))
    url = Column(String(50))
