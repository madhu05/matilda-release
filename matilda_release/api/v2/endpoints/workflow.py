import logging

from flask import request, jsonify
from flask_restplus import Resource

from matilda_release.api.v2.restplus import api
from matilda_release.api.v2.model.model import workflow, workflow_with_stages, environment_with_workflow, template, \
    templates_drop_down, frequency, jenkins
from matilda_release.api.v2.handler import workflow_handler

log = logging.getLogger(__name__)

ns = api.namespace('rls', description='Operations related to Release')


@ns.route('/release/<int:rls_id>/environment/<int:env_id>/workflows')
class WorkflowCollection(Resource):

    @api.marshal_list_with(workflow)
    def get(self, rls_id, env_id):
        """
        Returns list of releases.
        """
        resp = workflow_handler.get_workflow(env_id)
        return resp

    @api.response(201, 'Release successfully created.')
    @api.expect(workflow)
    @api.expect(workflow_with_stages)
    @api.expect(environment_with_workflow)
    @api.marshal_with(environment_with_workflow)
    def post(self, rls_id, env_id):
        data = request.json
        include_env = request.args.get('include_env', True, type=bool)
        resp = workflow_handler.create_workflow(env_id=env_id, wf_id=None, args=data, include_env=include_env)
        print ('WF resp {}'.format(resp))
        return resp


@ns.route('/release/<int:rls_id>/environment/<int:env_id>/workflow/<int:wf_id>')
@api.response(404, 'Release not found.')
class WorkflowItem(Resource):

    @api.marshal_with(workflow)
    def get(self, rls_id, env_id, wf_id, extended=None):
        """
        Returns release details.
        """
        resp = workflow_handler.get_workflow(wf_id=wf_id)
        if isinstance(resp, list) and len(resp) > 0:
            return resp[0]
        return resp

    @api.expect(workflow)
    @api.expect(workflow_with_stages)
    @api.expect(environment_with_workflow)
    @api.response(204, 'Release successfully updated.')
    @api.marshal_with(environment_with_workflow)
    def put(self, rls_id, env_id, wf_id):
        data = request.json
        include_env = request.args.get('include_env', True, type=bool)
        resp = workflow_handler.create_workflow(env_id=env_id, wf_id=wf_id, args=data, update_flag=True, include_env=include_env)
        return resp

    @api.response(204, 'Release successfully deleted.')
    def delete(self, id):
        # delete_category(id)
        return None, 204

@ns.route('/release/<int:rls_id>/environment/<int:env_id>/workflow/<int:wf_id>/extended')
@api.response(404, 'Release not found.')
class WorkflowItemDetailed(Resource):

    @api.marshal_with(workflow_with_stages)
    def get(self, rls_id, env_id, wf_id):
        """
        Returns release details.
        """
        resp = workflow_handler.get_workflow_with_stages(rls_id=rls_id, env_id=env_id, wf_id=wf_id)
        return resp[0]

@ns.route('/release/<int:rls_id>/environment/<int:env_id>/workflow/<int:wf_id>/action/<string:action>')
@api.response(404, 'Release not found.')
class WorkflowItemActions(Resource):

    @api.marshal_with(workflow)
    def get(self, rls_id, env_id, wf_id, action):
        """
        Returns release details.
        """
        resp = workflow_handler.get_workflow_with_stages(rls_id=rls_id, env_id=env_id, wf_id=wf_id)
        return resp[0]

    def post(self, rls_id, env_id, wf_id, action):
        print ('action {}'.format(action))
        if action == 'deploy':
            workflow_handler.deploy_workflow(wf_id,rls_id,env_id)
            resp = workflow_handler.get_workflow_with_stages(rls_id=rls_id, env_id=env_id,wf_id=wf_id, include_env=True)
            return jsonify(resp)


@ns.route('/templates')
class TemplateCollection(Resource):

    @api.marshal_list_with(template)
    def get(self):
         """
         Returns list of templates.
         """
         resp = workflow_handler.get_template()
         return resp

    @api.response(201, 'Template successfully created.',template)
    @api.expect(template)
    def post(self):
        data = request.json
        print('data{}'.format(data))
        resp = workflow_handler.create_template(data)
        print ('template resp {}'.format(resp))
        return resp

@ns.route('/templates/<int:template_id>')
@api.response(404, 'Release not found.')
class TemplateItem(Resource):

    @api.marshal_with(template)
    def get(self, template_id):
        """
        Returns release details.
        """
        resp = workflow_handler.get_template(template_id=template_id)
        print('resp {}'.format(resp))
        return resp


@ns.route('/templates/list')
@api.response(404, 'Release not found.')
class TemplateItem(Resource):

    @api.marshal_with(templates_drop_down)
    def get(self):
        """
        Returns release details.
        """
        template_name = request.args.get('template_name', None)
        resp = workflow_handler.get_templates_drop_down_values(template_name=template_name)
        print('resp {}'.format(resp))
        return resp



@ns.route('/frequency')
class FrequencyCollection(Resource):

    @api.marshal_list_with(frequency)
    def get(self):
        """
        Returns list of releases.
        """
        resp = workflow_handler.get_frequency()
        return resp

    @api.response(201, 'Frequency successfully created.')
    @api.expect(frequency)
    def post(self):
        data = request.json
        resp = workflow_handler.create_frequency(data)
        return resp

@ns.route('/jenkins')
class JobParametersCollection(Resource):

    @api.response(201, 'Retrieved parameter list successfully.')
    @api.expect(jenkins)
    def post(self):
        data = request.json
        resp = workflow_handler.get_jenkinsjob_parameters(data)
        return resp
