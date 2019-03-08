import logging

from flask import request
from flask_restplus import Resource

from matilda_release.api.v2.restplus import api
from matilda_release.api.v2.model.model import stage, stage_with_tasks
from matilda_release.api.v2.handler import stage_handler

log = logging.getLogger(__name__)

ns = api.namespace('rls', description='Operations related to Release')


@ns.route('/release/<int:rls_id>/environment/<int:env_id>/workflow/<int:wf_id>/stages')
class StageCollection(Resource):

    @api.marshal_list_with(stage)
    def get(self, rls_id, env_id, wf_id):
        """
        Returns list of releases.
        """
        resp = stage_handler.get_stage(wf_id)
        return resp

    @api.response(201, 'Release successfully created.')
    @api.expect([stage])
    @api.expect(stage)
    @api.expect([stage_with_tasks])
    def post(self, rls_id, env_id, wf_id):
        data = request.json
        stage_handler.create_stage(wf_id, data)
        return None, 201


@ns.route('/release/<int:rls_id>/environment/<int:env_id>/workflow/<int:wf_id>/stage/<int:stage_id>')
@api.response(404, 'Release not found.')
class StageItem(Resource):

    @api.marshal_with(stage)
    def get(self, rls_id, env_id, wf_id, stage_id):
        """
        Returns release details.
        """
        resp = stage_handler.get_stage(wf_id, stage_id)
        return resp[0]

    @api.expect(stage)
    @api.response(204, 'Release successfully updated.')
    def put(self, id):
        data = request.json
        # update_category(id, data)
        return None, 204

    @api.response(204, 'Release successfully deleted.')
    def delete(self, id):
        # delete_category(id)
        return None, 204
