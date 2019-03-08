import os
import pytest

from oslo_config import cfg

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from matilda_release.db import api as db_api
from matilda_release.test.it import test_data

conf_file = os.path.normpath(os.path.join(os.path.dirname(__file__), '../../../etc/matilda_release.conf'))
CONF = cfg.CONF
CONF(default_config_files=[conf_file])


def create_project():
    project = test_data.get_project()
    db_api.create_project(project)

def create_application():
    application = test_data.get_application()
    db_api.create_application(application)

create_project()
create_application()