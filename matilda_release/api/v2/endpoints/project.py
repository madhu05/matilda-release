import logging

from flask import request
from flask_restplus import Resource

from matilda_release.api.v2.restplus import api
from matilda_release.api.v2.model.model import project, project_with_apps
from matilda_release.api.v2.handler import project_handler

log = logging.getLogger(__name__)

ns = api.namespace('rls', description='Operations related to Release')


@ns.route('/projects')
class ProjectCollection(Resource):

    @api.marshal_list_with(project_with_apps)
    def get(self):
        """
        Returns list of releases.
        """
        resp = project_handler.get_projects()
        print(resp)
        return resp

    @api.response(201, 'Release successfully created.')
    @api.expect(project)
    def post(self):
        data = request.json
        project_handler.create_project(data)
        return None, 201