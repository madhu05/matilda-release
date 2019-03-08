import logging

from flask import request
from flask_restplus import Resource
from werkzeug.exceptions import BadRequest
from matilda_release.api.v2.restplus import api
from matilda_release.api.v2.model.model import service, action, service_fields, services_with_actions_fields, services_by_category, output_fields
from matilda_release.api.v2.handler import service_handler

log = logging.getLogger(__name__)

ns = api.namespace('plugin', description='Operations related to Release')


@ns.route('/services')
class ServiceCollection(Resource):

    @api.marshal_list_with(services_by_category)
    def get(self):
        """
        Returns list of releases.
        """
        try:
            resp = service_handler.get_services()

        except:
            raise BadRequest('Get services ')
        return resp

    @api.response(201, 'Release successfully created.')
    @api.expect(service)
    def post(self):
        try:
            data = request.json
            service_handler.create_service(data)
        except:
            raise BadRequest('Create service  failed{} '.format(data))
        return None, 201

@ns.route('/service/<string:service_id>/actions')
class ActionCollection(Resource):

    @api.marshal_list_with(action)
    def get(self, service_id):
        """
        Returns list of releases.
        """
        resp = service_handler.get_actions(service_id)
        return resp

    @api.response(201, 'Release successfully created.')
    @api.expect(action)
    @api.expect([action])
    def post(self, service_id):
        data = request.json
        service_handler.create_action(service_id,data)
        return None, 201


@ns.route('/service/<string:service_id>')
@api.response(404, 'Release not found.')
class ServiceItem(Resource):

    @api.marshal_with(service)
    def get(self, service_id):
        """
        Returns release details.
        """
        resp = service_handler.get_services(service_id=service_id, by_category=False)
        return resp[0]

    @api.expect(service)
    @api.response(204, 'Release successfully updated.')
    def put(self, id):
        data = request.json
        # update_category(id, data)
        return None, 204

    @api.response(204, 'Release successfully deleted.')
    def delete(self, id):
        # delete_category(id)
        return None, 204

@ns.route('/service/new')
@api.response(404, 'Service Not found')
class ServiceStack(Resource):

    @api.expect([services_with_actions_fields])
    @api.expect(services_with_actions_fields)
    def post(self):
        data = request.json
        service_handler.create_service_stack(data)
        return None, 201

@ns.route('/service/<string:service_id>/action/<string:action_id>/fields')
class ServiceActionFields(Resource):

    @api.marshal_list_with(service_fields)
    def get(self, service_id, action_id):
        return service_handler.get_service_fields(service_id, action_id)

@ns.route('/service/<string:service_id>/action/<string:action_id>/outputfields')
class ServiceOutputFields(Resource):

    @api.marshal_list_with(output_fields)
    def get(self, service_id, action_id):
        return service_handler.get_output_fields(service_id, action_id)
