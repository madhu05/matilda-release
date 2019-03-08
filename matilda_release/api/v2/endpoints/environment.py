import logging

from flask import request, jsonify
from flask_restplus import Resource

from matilda_release.api.v2.restplus import api
from matilda_release.api.v2.model.model import environment, environment_with_workflow, env_type_cd
from matilda_release.api.v2.handler import environment_handler

log = logging.getLogger(__name__)

ns = api.namespace('rls', description='Operations related to Release')

@ns.route('/release/<int:release_id>/envs')
class EnvironmentCollection(Resource):

    @api.marshal_list_with(environment_with_workflow, skip_none=True)
    def get(self, release_id):
        """
        Returns list of releases.
        """
        resp = environment_handler.get_environments(release_id)
        return resp

    @api.response(201, 'Env successfully created.', environment, skip_none=True)
    @api.expect(environment)
    @api.expect(environment_with_workflow)
    def post(self, release_id):
        data = request.json
        print ('Incomig request {}'.format(data))
        resp = environment_handler.create_environment(release_id, data)
        resp['workflows'] = []
        print ('Response {}'.format(resp))
        return resp


@ns.route('/release/<int:release_id>/env/<int:env_id>')
@api.response(404, 'Release not found.')
class EnvironmentItem(Resource):

    @api.marshal_with(environment_with_workflow, skip_none=True)
    def get(self, release_id, env_id):
        """
        Returns release details.
        """
        resp = environment_handler.get_environment_details(release_id, env_id)
        return resp


    @api.expect(environment_with_workflow)
    @api.response(204, 'Release successfully updated.')
    def put(self, id):

        data = request.json
        #update_category(id, data)
        return None, 204

    @api.response(204, 'Release successfully deleted.')
    def delete(self, id):
        #delete_category(id)
        return None, 204


@ns.route('/release/<int:release_id>/source_env_id/<int:source_env_id>/target_env_name/<string:target_env_name>/target_env_type_cd/<int:target_env_type_cd>/clone')
@api.response(404, 'Environment not found.')
class CloneEnvironment(Resource):
    # @api.expect(environment_with_workflow)
    @api.marshal_with(environment_with_workflow)
    def post(self, release_id, source_env_id, target_env_name, target_env_type_cd):
        resp = environment_handler.clone_environment(release_id=release_id, source_env_id=source_env_id, target_env_name=target_env_name, target_env_type_cd=target_env_type_cd)
        return resp


@ns.route('/release/<int:rls_id>/env/<int:env_id>/action/<string:action>')
@api.response(404, 'Release not found.')
class EnvironmentItemActions(Resource):

    @api.marshal_with(environment)
    def get(self, rls_id, env_id, action):
        pass

    def post(self, rls_id, env_id, action):
        print ('action {}'.format(action))
        if action == 'start':
            environment_handler.start_environment(env_id,rls_id)
            return True


@ns.route('/release/env/env_types')
class ReleaseTypeCollection(Resource):

    @api.marshal_list_with(env_type_cd)
    def get(self):
        resp = environment_handler.get_env_type_cd()
        return resp

# print(environment_handler.clone_environment(release_id=9, source_env_id=10, target_env_name='test_env_clone_abcdefg', target_env_type_cd=1))