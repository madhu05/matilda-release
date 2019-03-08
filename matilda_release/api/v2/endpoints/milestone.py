import logging

from flask import request
from flask_restplus import Resource
from matilda_release.api.v2.restplus import api
from matilda_release.api.v2.model.model import milestone_params, milestone_type, milestone_status_cd
from matilda_release.api.v2.handler import milestone_handler

log = logging.getLogger(__name__)

ns = api.namespace('rls', description='Operations related to Release')

@ns.route('/release/<int:release_id>/milestones')
class MilestoneCollection(Resource):

    @api.marshal_list_with(milestone_params, skip_none=True)
    def get(self, release_id):
        """
        Returns list of Milestones
        """
        resp = milestone_handler.get_milestone(release_id=release_id)
        return resp

    @api.response(201, '', milestone_params)
    @api.expect(milestone_params)
    def post(self, release_id):
        data = request.json
        print ('Incoming request {}'.format(data))
        resp = milestone_handler.create_milestone(release_id=release_id, args=data)
        return resp


@ns.route('/release/<int:release_id>/milestones/<int:milestone_id>')
@api.response(404, 'Milestone not found.')
class MilestoneItem(Resource):

    @api.marshal_with(milestone_params)
    def get(self, release_id, milestone_id):
        """
        Returns release details.
        """
        resp = milestone_handler.get_milestone(release_id=release_id, milestone_id=milestone_id)
        if isinstance(resp, list) and len(resp) > 0:
            return resp[0]
        return resp


    @api.expect(milestone_params)
    @api.marshal_with(milestone_params)
    @api.response(204, 'Milestone successfully updated.')
    def put(self, release_id, milestone_id):
        data = request.json
        resp = milestone_handler.update_milestone(release_id=release_id, milestone_id=milestone_id, args=data)
        return resp

    @api.response(204, 'Milestone successfully deleted.')
    def delete(self, release_id, milestone_id):
        milestone_handler.delete_milestone(release_id=release_id, milestone_id=milestone_id)
        return None, 204



@ns.route('/release/release_type/<int:release_type_cd>/milestone_types')
class MilestoneTypeCollection(Resource):

    @api.marshal_list_with(milestone_type, skip_none=True)
    def get(self, release_type_cd):
        """
        Returns list of Milestones
        """
        resp = milestone_handler.get_milestone_type(release_type_cd=release_type_cd)
        return resp

    @api.response(201, '', milestone_type)
    @api.expect(milestone_type)
    def post(self, release_type_cd):
        data = request.json
        print ('Incoming request {}'.format(data))
        resp = milestone_handler.create_milestone_type(release_type_cd=release_type_cd, args=data)
        return resp


@ns.route('/release/release_type/<int:release_type_cd>/milestone_types/<int:milestone_type_cd>')
@api.response(404, 'Milestone Type not found.')
class MilestoneTypeItem(Resource):

    @api.marshal_with(milestone_type)
    def get(self, release_type_cd, milestone_type_cd):
        """
        Returns release details.
        """
        resp = milestone_handler.get_milestone_type(release_type_cd=release_type_cd, milestone_type_cd=milestone_type_cd)
        if isinstance(resp, list) and len(resp) > 0:
            return resp[0]
        return resp


    @api.expect(milestone_type)
    @api.marshal_with(milestone_type)
    @api.response(204, 'Milestone successfully updated.')
    def put(self, release_type_cd, milestone_type_cd):
        data = request.json
        resp = milestone_handler.update_milestone_type(release_type_cd=release_type_cd, milestone_type_cd=milestone_type_cd, args=data)
        return resp

    @api.response(204, 'Milestone Type successfully deleted.')
    def delete(self, release_type_cd, milestone_type_cd):
        milestone_handler.delete_milestone_type(release_type_cd=release_type_cd, milestone_type_cd=milestone_type_cd)
        return None, 204

@ns.route('/release/milestones/milestone_status_cd')
class MilestoneCollection(Resource):

    @api.marshal_list_with(milestone_status_cd, skip_none=True)
    def get(self):
        resp = milestone_handler.get_milestone_status_cd()
        return resp