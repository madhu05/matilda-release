import logging
import sys

from flask import request
from flask_restplus import Resource

from matilda_release.api.v2.restplus import api
from matilda_release.api.v2.model.model import task, task_response
from matilda_release.api.v2.handler import task_handler

log = logging.getLogger(__name__)

ns = api.namespace('rls', description='Operations related to Release')


@ns.route('/release/<int:rls_id>/environment/<int:env_id>/workflow/<int:wf_id>/stage/<int:stage_id>/tasks')
class TaskCollection(Resource):

    @api.marshal_list_with(task)
    def get(self, rls_id, env_id, wf_id, stage_id):
        """
        Returns list of releases.
        """
        resp = task_handler.get_task(stage_id=stage_id)
        return resp

    @api.response(201, 'Release successfully created.')
    @api.expect([task])
    @api.expect(task)
    def post(self, rls_id, env_id, wf_id, stage_id):
        data = request.json
        task_handler.create_task(stage_id, data)
        return None, 201

@ns.route('/release/<int:rls_id>/environment/<int:env_id>/workflow/<int:wf_id>/stage/<int:stage_id>/task/<int:task_id>')
@api.response(404, 'Release not found.')
class TaskItem(Resource):

    @api.marshal_with(task)
    def get(self, rls_id, env_id, wf_id, stage_id, task_id):
        """
        Returns release details.
        """
        resp = task_handler.get_task(stage_id=stage_id)
        return resp[0]

    @api.expect(task)
    @api.response(204, 'Release successfully updated.')
    def put(self, id):
        data = request.json
        # update_category(id, data)
        return None, 204

    @api.response(204, 'Release successfully deleted.')
    def delete(self, id):
        # delete_category(id)
        return None, 204

@ns.route('/release/task/<int:task_id>/update')
@api.response(404, 'Release not found.')
class TaskResponse(Resource):

    @api.response(201, 'Task Response Updated')
    @api.expect()
    def post(self, task_id):
        data = request.json
        resp = task_handler.update_task_stats(task_id, data)
        return resp

