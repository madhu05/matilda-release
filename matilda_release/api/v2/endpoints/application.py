import logging

from flask import request
from flask_restplus import Resource

from matilda_release.api.v2.restplus import api
from matilda_release.api.v2.model.model import application
from matilda_release.api.v2.handler import application_handler

log = logging.getLogger(__name__)

ns = api.namespace('rls', description='Operations related to Release')


@ns.route('/applications')
class ApplicationCollection(Resource):

    @api.marshal_list_with(application)
    def get(self):
        """
        Returns list of releases.
        """
        resp = application_handler.get_applications()
        print(resp)
        return resp

    @api.response(201, 'Release successfully created.')
    @api.expect(application)
    def post(self):
        data = request.json
        application_handler.create_application(data)
        return None, 201
