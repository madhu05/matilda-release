import json
from flask_restplus import fields

import ast
from matilda_release.api.v2.restplus import api

class Options(fields.Raw):
    def format(self, value):
        print ('Value to be UPDATED {}'.format(value))
        if value is not None and (value != 'None' and value.strip() != ''):
            return ast.literal_eval(value)
        else:
            return None

application = api.model('Application', {
    'app_id': fields.String(readOnly=True, description='Application ID'),
    'owner': fields.String(required=True, description='Application Owner'),
    'create_dt': fields.DateTime(required=False, description='Creation Date'),
    'status': fields.String(required=True, description='status'),
    'name': fields.String(required=False, description='Name'),
    'project_id': fields.String(attribute='project_id')
})

project = api.model('Project', {
    'project_id': fields.String(readOnly=True, description='Project ID'),
    'name': fields.String(required=True, description='Project Name'),
    'owner': fields.String(required=True, description='Project Owner'),
    'create_dt': fields.DateTime(required=False, description='Creation Date'),
    'status': fields.String(required=True, description='status')
})

project_with_apps = api.inherit('project with apps', project, {
    'applications': fields.Nested(application)
})

platform = api.model('Platform', {
    'platform_id': fields.Integer(required=True, description='Platform Id'),
    'name': fields.String(required=True, description='Platform Name')
})

release_params = api.model('Release', {
    'release_id': fields.Integer(readOnly=True, description='The unique identifier of release'),
    'name': fields.String(required=True, description='Release name'),
    'create_dt': fields.DateTime(required=False, description='Release date', default=None),
    'release_dt': fields.DateTime(required=True, description='Release date', default=None),
    'project_id': fields.String(required=False, description='Project if app release', default=None),
    'project_name': fields.String(required=False, description='Project Name if App Release', default=None),
    'application_id': fields.String(required=False, description='Application Id if app release', default=None),
    'application_name': fields.String(required=False, description='Application Id if app release', default=None),
    # 'os_id': fields.Integer(required=False, description='Operating System ID if infra release', default=None),
    # 'os_name': fields.String(required=False, description='Operating System name if infra release', default=None),
    'platform': fields.List(fields.Nested(platform), required=False),
    'platform_name': fields.String(required=False, description='Platform names separated by comma', default=None),
    'vnf_site': fields.String(required=False, description='Operating System name if infra release', default=None),
    'vnf_node': fields.String(required=False, description='vnf node if Infra release', default=None),
    'release_type_cd': fields.Integer(readOnly=True, description='Release_type_cd'),
    'release_type_description': fields.String(required=False, description='Release type description'),
    'status_cd': fields.Integer(required=False, description='Status Code'),
    'status_description': fields.String(required=False, description='Status Description'),
    'duration': fields.String(required=False, description='Release duration'),
    'description': fields.String(required=False, description='Release duration'),
    'release_plan_id': fields.Integer(required=True, description = 'Release Plan Id'),
    'release_plan_name': fields.String(required=False, description='Release Plan Name')
})

release = api.inherit('Release with project and apps', release_params, {
    'project': fields.Nested(project),
    'application': fields.Nested(application)
})

release_count = api.model('Release_Count', {
    'release_type_cd': fields.Integer(required=True, description='Unique code for Release Type'),
    'count': fields.String(required=True, description='count for each Release type')
})

status = api.model('Status', {
    'status': fields.Raw(required=True, description='status: count')
})

release_type = api.model('Release_Type', {
    'release_type_cd': fields.Integer(required=True, description='Unique code for Release Type'),
    'release_type_description': fields.String(required=True, description='Release Type Description'),
    'color_pref': fields.String(required=False, description='Preferred color for release type')
})


milestone_params = api.model('Milestone', {
    'milestone_id': fields.Integer(readOnly=True, description='The unique identifier of milestone'),
    'start_dt': fields.DateTime(required=False, description='Milestone Start date'),
    'end_dt': fields.DateTime(required=False, description='Milestone End date'),
    'milestone_status_cd': fields.Integer(required=False, description='Milestone Status Code'),
    'milestone_description': fields.String(required=False, description='user description on milestone'),
    'percent_complete': fields.Float(required=False, description='percentage completion for milestone'),
    'release_id': fields.Integer(required=False, description='release id for which milestone is created')
})

milestone_type = api.model('Milestone_Type', {

    'milestone_type_cd': fields.Integer(required=True, description='Unique code for Milestone Type'),
    'milestone_type_description': fields.String(required=True, description='Milestone Type Description'),
    'release_type_cd': fields.Integer(readOnly=True, description='Release_type_cd')
})

milestone_status_cd = api.model('Milestone_Status_Cd', {
    'milestone_status_cd': fields.Integer(required=True, description='Unique code for Milestone Status'),
    'milestone_status_description': fields.String(required=True, description='Milestone Type Description')
})


environment = api.model('Environment', {
    'env_id': fields.Integer(readOnly=True, description='The unique identifier of environment'),
    'name': fields.String(required=True, description='Environment name'),
    'env_type_cd': fields.Integer(required=True, description='Environment version'),
    'env_type_description': fields.String(required=True, description='Environment version'),
    'create_dt': fields.DateTime(required=False, description='Environment Create date'),
    'start_dt': fields.DateTime(required=False, description='Environment Start date'),
    'end_dt': fields.DateTime(required=False, description='Environment End date'),
    'status_cd': fields.Integer(required=False, description='Status Code'),
    'status_description': fields.String(required=False, description='Status Description'),
    'release_id': fields.Integer(required=False, description='release id'),
    'release': fields.String(attribute='release.name')
})

artifact_type = api.model('ArtifactType', {
    'id': fields.Integer(readOnly=True, description='Artifact Type ID'),
    'name': fields.String(required=True, description='Artifact name'),
    'type': fields.String(required=True, description='Artifact type')
})

release_link_items = api.model('ReleaseLinkItem', {
    'release_link_item_id': fields.Integer(readOnly=True, description='Release artifact ID'),
    'data': fields.String(required=True, description='Release artifact link'),
    'release_link_id': fields.Integer(attribute='release_link_id')
})

release_link = api.model('ReleaseLink', {
    'release_link_id': fields.Integer(readOnly=True, description='Release artifact ID'),
    'name': fields.String(required=True, description='Release artifact name'),
    'url': fields.String(required=False, description='Release version'),
    'source': fields.String(required=False, description='Release version'),
    'description': fields.String(required=False, description='Release date'),
    'release_id': fields.Integer(attribute='release.release_id')
})

workflow = api.model('Workflow', {
    'wf_id': fields.Integer(readOnly=True, description='The unique identifier of environment'),
    'name': fields.String(required=True, description='Workflow name'),
    'template_id': fields.Integer(required=False, description='Template Used'),
    'description': fields.String(required=False, description='description'),
    'create_dt': fields.DateTime(required=False, description='Environment Create date'),
    # 'schedule_dt': fields.DateTime(required=False, description='Schedule date'),
    'status_cd': fields.Integer(required=False, description='Status Code'),
    'status_description': fields.String(required=False, description='Status Description'),
    'release_id': fields.Integer(required=False, description='Release Id'),
    'release': fields.String(attribute='release.name'),
    'frequency_cd': fields.Integer(required=False, description='Frequency Code'),
    'frequency_description': fields.String(required=False, description='Frequency description'),
    'env_id': fields.Integer(required=False, description='environment id'),
    'overall_progress': fields.Integer(required=False, description='Progress'),
    'environment_name': fields.String(required=False, description='Progress'),
    'dag_name': fields.String(required=False, description='dag name')
})

stage = api.model('Stage', {
    'stage_id': fields.Integer(readOnly=True, description='Stage ID'),
    'stage_ui_id': fields.String(required=True, description='Workflow name'),
    'name': fields.String(required=True, description='Workflow name'),
    'description': fields.String(required=False, description='stage description'),
    'create_dt': fields.DateTime(required=False, description='Environment Create date'),
    'planned_start_dt': fields.DateTime(required=False, description='Schedule date'),
    'planned_end_dt': fields.DateTime(required=False, description='Schedule date'),
    'actual_start_dt': fields.DateTime(required=False, description='Schedule date'),
    'actual_end_dt': fields.DateTime(required=False, description='Schedule date'),
    'status_cd': fields.Integer(required=False, description='Status Code'),
    'status_description': fields.String(required=False, description='Status Description'),
    'owner': fields.String(required=False, description='Owner'),
    'order': fields.Integer(required=False, description='payload'),
    'workflow_id': fields.Integer(attribute='wf_id')
})


task = api.model('Task', {
    'task_id': fields.Integer(readOnly=True, description='Task ID'),
    'task_ui_id': fields.String(required=True, description='Workflow name'),
    'name': fields.String(required=True, description='Task name'),
    'create_dt': fields.DateTime(required=False, description='Environment Create date'),
    'planned_start_dt': fields.DateTime(required=False, description='Schedule date'),
    'planned_end_dt': fields.DateTime(required=False, description='Schedule date'),
    'actual_start_dt': fields.DateTime(required=False, description='Schedule date'),
    'actual_end_dt': fields.DateTime(required=False, description='Schedule date'),
    'status_cd': fields.Integer(required=False, description='Status Code'),
    'status_description': fields.String(required=False, description='Status Description'),
    'owner': fields.String(required=False, description='Owner'),
    'ignore_failure': fields.String(required=False, description='Owner'),
    'stage_id': fields.Integer(attribute='stage_id'),
    'task_group_id': fields.Integer(attribute='task_group_id'),
    'service_id': fields.String(required=True, description='Service Code'),
    'action_id': fields.String(required=True, description='action id'),
    'service_name': fields.String(required=True, description='Service Code'),
    'action_name': fields.String(required=True, description='action name'),
    'duration': fields.String(required=False, description='Task duration'),
    'dag_task_name': fields.String(required=False, description='dag_task_name'),
    'wf_id': fields.Integer(required=False, description='workflow_id'),
    'input': Options(required=True, description='input'),
   # 'input': fields.Nested(tsk),
    'output': Options(required=True, description='output')
})

stage_with_tasks = api.inherit('Stages with tasks', stage, {
    'tasks': fields.List(fields.Nested(task))
})

workflow_with_stages = api.inherit('workflow with stages', workflow, {
    'stages': fields.List(fields.Nested(stage_with_tasks))
})

environment_with_workflow = api.inherit(
    'environment with workflows', environment, {
        'workflows': fields.List(
            fields.Nested(workflow_with_stages))})

release_with_artifacts = api.inherit('release', release, {
    'artifacts': fields.List(fields.Nested(release_link)),
    'environments': fields.List(fields.Nested(environment_with_workflow))
})

impacted_application = api.model('impacted_application', {
    'name': fields.String(required=True, description='Application Name'),
    'status': fields.String(readOnly=True, description='Application Status'),
})


impacted_systems_data = api.model('impacted_systems_data', {
    'status': fields.String(required=True, description='status'),
    'os': fields.String(required=True, description='operating system'),
    'platform': fields.String(required=True, description='platform'),
    'ip': fields.String(required=True, description='hostname/ip'),
    'applications':fields.List(fields.Nested(impacted_application))
})

infra_release_impacted_systems = api.inherit('Imapacted systems for an infra release', environment,{
    'impactedSystems': fields.List(fields.Nested(impacted_systems_data))
})


infra_release_impacted_application = api.model('infra_release_impacted_application', {
    'impacted_application_id': fields.Integer(readOnly=True, description='primary key for impacted applications'),
    'release_id': fields.Integer(required=True, description='Release Id'),
    'computer_system_name': fields.String(required=True, description='computer system name'),
    'application_name' : fields.String(required=True, description='Application name'),
    'environment': fields.String(required=True, description='environment'),
    'platform': fields.String(required=True, description='platform'),
    'platform_from_excel': fields.String(required=False, description='platform from excel'),
    'operating_system': fields.String(required=True, description='operating system'),
    'test_type_prod': fields.String(required=False, description='test type production'),
    'test_type_non_prod': fields.String(required=False, description='test type non production'),
    'app_owner_name': fields.String(required=False, description='app owner name'),
    'tester_name': fields.String(required=False, description='tester_name'),
    'test_folder_name': fields.String(required=True, description='test folder name'),
    'test_set_or_folder': fields.String(required=True, description='test set or folder'),
    'opt_out': fields.Boolean(required=False, description='opt out for testing')
})


action = api.model('Action', {
    'action_id': fields.String(readOnly=True, description='Action ID'),
    'name': fields.String(required=True, description='Task name'),
    'description': fields.String(required=True, description='Task name'),
    'service_id': fields.String(attribute='service_id')
})

service = api.model('Service', {
    'service_id': fields.String(readOnly=True, description='Task ID'),
    'name': fields.String(required=True, description='Task name'),
    'category': fields.String(required=True, description='Task name'),
    'comments': fields.String(required=True, description='Task name'),
    'actions': fields.List(fields.Nested(action))
})


service_fields = api.model('ServiceFields', {
    'service_field_id': fields.String(readOnly=True, description='Service Field ID'),
    'key': fields.String(required=True, description='Task name'),
    'label': fields.String(required=True, description='Task name'),
    'controlType': fields.String(required=True, description='Task name'),
    'required': fields.Boolean(required=False, description='Task name'),
    'placeholder': fields.String(required=False, description='Task name'),
    'order': fields.Integer(required=True, description='Task name'),
    'options': Options(required=False, description='Task name'),
    'field_type': fields.String(required=True, description='input/output'),
    'description': fields.String(required=True, description='Task name'),
    'service_id': fields.String(attribute='service_id'),
    'action_id': fields.String(attribute='action_id')
})

output_fields = api.model('OutputFields', {
    'output_field_id': fields.String(readOnly=True, description='Output Field ID'),
    'output_field_name': fields.String(required=False, description='Task name'),
    # 'isActive': fields.Boolean(required=False, description='flag to check if the output field is needed'),
    'service_id': fields.String(attribute='service_id'),
    'action_id': fields.String(attribute='action_id')
})


operating_system = api.model('Operating_System', {
    'os_id': fields.Integer(required=True, description='Operating System Id'),
    'name': fields.String(required=True, description='Operating System Name'),
    'platform_id': fields.Integer(required=True, description='Platform Id')
})

platforms_with_os = api.inherit('platform_with_os', platform, {
    'operating_systems': fields.List(fields.Nested(operating_system))
})

vnf_node_type = api.model('VnfNodeType', {
    'vnf_node_id': fields.String(required=True, description='VNF node Id'),
    'name': fields.String(required=True, description='VNF Name')
})

vnf_sites = api.model('VnfSites', {
    'vnf_site_id': fields.String(required=True, description='Vnf Site Id'),
    'name': fields.String(required=True, description='Operating System Name'),
    'vnf_node_id': fields.String(required=True, description='Vnf Node Id')
})

vnf_node_type_with_sites = api.inherit('vnf_node_type_with_sites', vnf_node_type, {
    'vnf_sites': fields.List(fields.Nested(vnf_sites))
})

services_with_actions = api.inherit('services with actions', service, {
    'actions': fields.List(fields.Nested(action))
})

category = api.model('Service Category', {
    'name': fields.String(required=True, description='Operating System Id')
})

services_by_category = api.inherit('services with actions', category, {
    'services': fields.List(fields.Nested(services_with_actions))
})

actions_with_fields = api.inherit('actions with fields', action, {
    'service_fields': fields.List(fields.Nested(service_fields))
})

services_with_actions_fields = api.inherit('services with actions and fields', service, {
    'actions': fields.List(fields.Nested(actions_with_fields))
})

task_response = api.model('Task Stats', {
    'dag_id': fields.String(required=True, description='DAG ID'),
    'task_id': fields.String(required=True, description='Task ID'),
    'status_cd': fields.Integer(required=True, description='Status Code'),
    'status_description': fields.String(required=False, description='Status Description'),
    'output': fields.String(required=True, description='Output')
})


template = api.model('Template', {
    'template_id': fields.Integer(readOnly=True, description='The unique identifier of template'),
    'template_name': fields.String(required=True, description='Template name'),
    'template_version': fields.Integer(required=False, description='Template version'),
    'template_json': fields.Raw(required=True, description='Template Json')

})


template_id_and_version = api.model('Template_id_and_version', {
    'template_id': fields.Integer(readOnly=True, description='The unique identifier of template'),
    'template_version': fields.Integer(required=True, description='Template version')
})

templates_drop_down = api.model('TemplatesDropDown', {
    'template_name': fields.String(required=True, description='Template name'),
    'template_details': fields.Nested(template_id_and_version)
})


release_names = api.model('ReleaseName', {
    'release_names': fields.List(fields.String)
})

# env_clone = api.model('Env_Clone', {
#     'env_id': fields.Integer(required=False, description='newly created env id'),
#     'env_name': fields.String(required=True, description='name of new new environment'),
#     'env_type': fields.String(required=True, description='type for new environment'),
#     'wf_id': fields.Integer(required=False, description='created workflow id')
# })

rls_clone = api.model('Rls_Clone', {
    'name': fields.String(required=True, description='name of new release'),
    'release_dt': fields.String(required=True, description='date for new release')
})


frequency = api.model('Frequency', {
    'frequency_cd': fields.Integer(readOnly=True, description='The unique identifier of frequency'),
    'frequency_description': fields.String(required=True, description='Frequency name'),
    'dag_usage': fields.String(required=True, description='Code Usage'),
    'comments': fields.String(required=False, description='details of the frequency'),
    'cron_expression': fields.String(required=False, description='cron expression')

})

env_type_cd = api.model('EnvTypeCd', {
    'env_type_cd': fields.Integer(readOnly=True, description='The unique identifier of environment type'),
    'env_type_description': fields.String(required=True, description='Environment type description')
})

jenkins = api.model('Jenkins', {
    'job_name': fields.String(required=True, description='jenkins job name'),
    'url': fields.String(required=True, description='jenkins server url'),
    'username': fields.String(required=True, description='jenkins username'),
    'token': fields.String(required=False, description='jenkins token/password')

})


release_plan = api.model('ReleasePlan', {
    'release_plan_id': fields.Integer(readOnly=True, description='The unique identifier of release plan'),
    'release_type_cd': fields.Integer(required=True, description='Release type code'),
    'color_pref': fields.String(readOnly=True, description='Release color derived from release type code'),
    'release_plan_name': fields.String(required=True, description='Release Plan Name'),
    'release_plan_description': fields.String(required=False, description='Release Plan Description'),
    'release_owner': fields.String(required=True, description='Release Plan owner'),
    'create_dt': fields.DateTime(required=False, description='Release Plan Created Date'),
    'release_dt': fields.DateTime(required=True, description='Planned Release Date'),
})


master_application = api.model('MasterApplication', {
    'master_application_id': fields.Integer(readOnly=True, description='The unique identifier for master application'),
    'computer_system_name': fields.String(required=True, description='computer system name'),
    'application_name' : fields.String(required=True, description='Application name'),
    'environment': fields.String(required=True, description='environment'),
    'platform': fields.String(required=True, description='platform'),
    'platform_from_excel': fields.String(required=False, description='platform from excel'),
    'operating_system': fields.String(required=True, description='operating system'),
    'test_type_prod': fields.String(required=False, description='test type production'),
    'test_type_non_prod': fields.String(required=False, description='test type non production'),
    'app_owner_name': fields.String(required=False, description='app owner name'),
    'tester_name': fields.String(required=False, description='tester_name'),
    'test_set_or_folder': fields.String(required=True, description='test set or folder'),
})


opt_out_application = api.model('opt_out_application', {
    'application_name': fields.String(required=True, description='Application Name'),
    'opt_out': fields.Boolean(required=False, description='opt out for testing')
})