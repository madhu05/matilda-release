import logging.config

import os
from flask import Flask, Blueprint
from flask_cors import CORS

from oslo_config import cfg

from matilda_release.api.v2 import settings
from matilda_release.api.v2.endpoints.release import ns as release_namespace
from matilda_release.api.v2.endpoints.links import ns as links_namespace
from matilda_release.api.v2.endpoints.environment import ns as env_namespace
from matilda_release.api.v2.endpoints.workflow import ns as wf_namespace
from matilda_release.api.v2.endpoints.stages import ns as stage_namespace
from matilda_release.api.v2.endpoints.tasks import ns as task_namespace
from matilda_release.api.v2.endpoints.service import ns as service_namespace
from matilda_release.api.v2.endpoints.project import ns as project_namespace
from matilda_release.api.v2.endpoints.application import ns as application_namespace
from matilda_release.api.v2.endpoints.milestone import ns as milestone_namespace
from matilda_release.api.v2.endpoints.infra_release import ns as infra_release_namespace
from matilda_release.api.v2.endpoints.release_plan import ns as release_plan_namespace
from matilda_release.api.v2.endpoints.metrics import ns as metrics_namespace


from matilda_release.api.v2.restplus import api

app = Flask(__name__)
CORS(app)
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../../etc/logging.conf'))
conf_file = os.path.normpath(os.path.join(os.path.dirname(__file__), '../../etc/matilda_release.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)
CONF = cfg.CONF
CONF(default_config_files=[conf_file, logging_conf_path])

#blueprint = Blueprint('api', __name__, url_prefix='/api')
logging.info("initialized")


def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def initialize_app(flask_app):
    configure_app(flask_app)
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(release_namespace)
    api.add_namespace(links_namespace)
    api.add_namespace(env_namespace)
    api.add_namespace(project_namespace)
    api.add_namespace(application_namespace)
    api.add_namespace(wf_namespace)
    api.add_namespace(stage_namespace)
    api.add_namespace(task_namespace)
    api.add_namespace(service_namespace)
    api.add_namespace(milestone_namespace)
    api.add_namespace(release_plan_namespace)
    api.add_namespace(metrics_namespace)
    api.add_namespace(infra_release_namespace)
    flask_app.register_blueprint(blueprint)
    #db.init_app(flask_app)


def main():
    initialize_app(app)
    app.run(host='0.0.0.0', port=5000, debug=True)

#main()

if __name__ == "__main__":
    main()
