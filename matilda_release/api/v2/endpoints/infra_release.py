import logging

from flask import request, jsonify
from flask_restplus import Resource
from matilda_release.api.v2.restplus import api
from matilda_release.api.v2.model.model import master_application, infra_release_impacted_application, opt_out_application
from matilda_release.api.v2.handler import infra_release_handler

log = logging.getLogger(__name__)

ns = api.namespace('rls', description='Operations related to Release')

@ns.route('/infra_release/master_applications')
class MasterApplicationCollection(Resource):

    @api.marshal_list_with(master_application, skip_none=True)
    def get(self):
        platform = request.args.get('platform', None)
        resp = infra_release_handler.get_master_application(platform=platform)
        return resp

    @api.response(201, '', master_application)
    @api.marshal_with(master_application)
    @api.expect(master_application)
    def post(self):
        data = request.json
        print ('Incoming request {}'.format(data))
        resp = infra_release_handler.create_master_application(args=data)
        return resp


@ns.route('/infra_release/<int:release_id>/impacted_applications')
class InfraReleaseImpactedApplicationCollection(Resource):

    # @api.marshal_list_with(infra_release_impacted_application, skip_none=True)
    def get(self, release_id):
        resp = infra_release_handler.get_infra_release_impacted_application(release_id=release_id,
                                                                            create_environment=True)
        print('response on api:{}'.format(resp))
        return jsonify(resp)

    @api.response(201, '', infra_release_impacted_application)
    @api.marshal_with(infra_release_impacted_application)
    @api.expect(infra_release_impacted_application)
    def post(self, release_id):
        data = request.json
        print ('Incoming request {}'.format(data))
        resp = infra_release_handler.create_infra_release_impacted_application(release_id=release_id,args=data)
        return resp


@ns.route('/infra_release/<int:release_id>/impacted_application/<int:impacted_application_id>')
@api.response(404, 'Release not found.')
class InfraReleaseImpactedApplication(Resource):

    @api.marshal_with(infra_release_impacted_application)
    def get(self, release_id, impacted_application_id):
        """
        Returns release details.
        """
        resp = infra_release_handler.get_infra_release_impacted_application(release_id=release_id, impacted_application_id=impacted_application_id)
        if isinstance(resp, list) and len(resp) > 0:
            return resp[0]
        return resp

    @api.marshal_with(infra_release_impacted_application)
    @api.expect(infra_release_impacted_application)
    @api.response(204, 'Release successfully updated.')
    def put(self, release_id, impacted_application_id):
        data = request.json
        resp = infra_release_handler.update_infra_release_impacted_application(release_id=release_id, impacted_application_id=impacted_application_id, args=data)
        return resp

@ns.route('/infra_release/<int:release_id>/impacted_application/application_name')
@api.response(404, 'Release not found.')
class UpdateInfraReleaseImpactedApplication(Resource):

    @api.expect(opt_out_application)
    @api.response(204, 'opt out for application successfully updated.')
    def put(self, release_id):
        data = request.json
        application_name = data.get('application_name')
        opt_out = data.get('opt_out')
        resp = infra_release_handler.update_opt_out_for_application(release_id=release_id, application_name=application_name, opt_out=opt_out)
        return resp

@ns.route('/infra_release/<int:release_id>/testSuites')
class InfraReleaseTestSuite(Resource):

    @api.response(201, 'Test Suites creation Triggered')
    def post(self, release_id):
        resp = infra_release_handler.create_test_suites(release_id)
        return resp