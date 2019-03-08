import logging

from flask import request
from flask_restplus import Resource
from matilda_release.api.v2.restplus import api
from matilda_release.api.v2.model.model import release_plan
from matilda_release.api.v2.handler import release_plan_handler
from matilda_release.util.status_helper import ReleaseTypeCdDefinition as rls_type_cd
from werkzeug.exceptions import BadRequest


log = logging.getLogger(__name__)

ns = api.namespace('rls', description='Operations related to Release')

@ns.route('/release_plans')
class ReleasePlanCollection(Resource):

    @api.marshal_list_with(release_plan, skip_none=True)
    def get(self):

        release_type_cd = request.args.get('release_type_cd', None)
        if release_type_cd is not None:
            try:
                release_type_cd = int(release_type_cd)
            except:
                raise BadRequest('release type code not int {}'.format(release_type_cd))

        resp = release_plan_handler.get_release_plan(release_type_cd=release_type_cd)


        return resp

    @api.response(201, 'Release Plan Successfully Created', release_plan)
    @api.marshal_list_with(release_plan)
    @api.expect(release_plan)
    def post(self):
        data = request.json
        return release_plan_handler.create_release_plan(data)

@ns.route('/release_plans/<int:release_plan_id>')
@api.response(404, 'Release Plan not found.')
class ReleasePlan(Resource):

    @api.marshal_with(release_plan)
    def get(self, release_plan_id):
        resp = release_plan_handler.get_release_plan(release_plan_id=release_plan_id)
        if isinstance(resp, list) and len(resp) > 0:
            return resp[0]
        return resp

    @api.expect(release_plan)
    @api.marshal_with(release_plan)
    @api.response(204, 'Release Plan successfully updated.')
    def put(self, release_plan_id):
        data = request.json
        resp = release_plan_handler.update_release_plan(release_plan_id=release_plan_id, args=data)
        return resp

    @api.response(204, 'Release Plan successfully deleted.')
    def delete(self, release_plan_id):
        release_plan_handler.delete_release_plan(release_plan_id=release_plan_id)
        return None, 204


