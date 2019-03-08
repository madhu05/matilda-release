import logging

from flask import jsonify
from flask_restplus import Resource
from werkzeug.exceptions import BadRequest
from matilda_release.api.v2.restplus import api
from matilda_release.api.v2.handler import metrics_handler
from matilda_release.util.status_helper import ReleaseTypeCdDefinition as rls_type_cd

log = logging.getLogger(__name__)

ns = api.namespace('rls', description='Operations related to Release')


@ns.route('/metrics/release_type_cd/<int:release_type_cd>/component/<int:component_id>/start_date/<string:start_date>/end_date/<string:end_date>')
@api.response(404, 'Infra Metrics not found')
class ChartCollection(Resource):

    #@api.marshal_list_with(infra_release_impacted_systems,skip_none=True)
    def get(self, release_type_cd,component_id,start_date,end_date):

        try:
            if(release_type_cd==rls_type_cd.infrastructure.release_type_cd):
                resp = metrics_handler.get_infra_metrics_data(component_id,start_date,end_date)
            elif (release_type_cd == rls_type_cd.application.release_type_cd):
                resp = metrics_handler.get_app_metrics_data(component_id,start_date,end_date)
        except:
            raise BadRequest('Get Chart data failed for component_id {}',component_id)
        return resp

@ns.route('/metrics/release_type_cd/<int:release_type_cd>/component/<string:component_name>')
@api.response(404, 'Metrics component not found.')
class InfraComponent(Resource):

    #@api.marshal_with(release_with_artifacts, skip_none=True)
    def get(self,release_type_cd, component_name):

        try:
            if (release_type_cd == rls_type_cd.infrastructure.release_type_cd):
                resp = metrics_handler.get_infra_component_id(component_name=component_name)
            elif (release_type_cd == rls_type_cd.application.release_type_cd):
                resp = metrics_handler.get_app_component_id()
        except:
            raise BadRequest('Get component_name failed - component_name {} '.format(component_name))

        return resp[0]

@ns.route('/metrics/release_type_cd/<int:release_type_cd>/components')
@api.response(404, 'Metrics list component not found.')
class listComponent(Resource):

    #@api.marshal_with(release_with_artifacts, skip_none=True)
    def get(self,release_type_cd):

        try:
            if (release_type_cd == rls_type_cd.infrastructure.release_type_cd):
                resp = metrics_handler.get_infra_component_id()
            elif (release_type_cd == rls_type_cd.application.release_type_cd):
                resp = metrics_handler.get_app_component_id()
        except:
            raise BadRequest('Get components failed')

        return resp
