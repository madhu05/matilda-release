import collections
import uuid
import requests
import json
import os
import logging
from ast import literal_eval
import xmltodict


from datetime import datetime
from six import iteritems

from matilda_release.db import api as db_api
from matilda_release.db.sqlalchemy import models
from matilda_release.api.v2.model.model import workflow
from werkzeug.exceptions import BadRequest

from matilda_workflow.dag import dag_builder as db
from matilda_release.util.status_helper import StatusDefinition as stts_dfn
from matilda_release.util import status_helper as stts_hlpr
from matilda_release.util import status_engine as stts_engine
from matilda_release.util.status_helper import ReleaseTypeCdDefinition as rls_dfn
from matilda_plugin.plugins.jenkins_plugin.jenkins_plugin import JenkinsPlugin


log = logging.getLogger(__name__)


def create_workflow(env_id, wf_id, args, include_env=False, update_flag=False):
    if update_flag:
        clear_workflows(env_id)

    resp = []
    if not isinstance(args, list):
        args = [args]

    for item in args:
        wf = _map_wf(env_id, item, item.get('order', args.index(item)), wf_id)
        wf_resp = db_api.create_workflow(wf)

        from matilda_release.api.v2.handler import stage_handler
        resp = stage_handler.create_stage(wf_resp['wf_id'], item['stages'])
        wf_resp['stages'] = resp

        for k, v in iteritems(wf_resp):
            print ('WF Key {} value {} type {}'.format(k, v, type(v)))
            if isinstance(v, datetime):
                wf_resp[k] = datetime.strftime(v,'%Y-%m-%dT%H:%M:%S.%fZ') if v is not None else None

        resp.append(wf_resp)

    # TODO: Replace with event update
    stts_engine.check_and_update_stage(wf_id=resp[0].get('wf_id'))

    if include_env:
        resp = update_resp_with_env(env_id, resp)
    print ('WF Create final response from handler {}'.format(resp))
    return resp


def update_resp_with_env(env_id, wf_list):
    from matilda_release.api.v2.handler import environment_handler
    env_details = environment_handler.get_environment_details(release_id=0, env_id=env_id)
    if isinstance(env_details, list) and len(env_details) > 0:
        env_details = env_details[0]
    print('Workflows here {}'.format(wf_list))
    env_details['workflows'] = wf_list
    print ('Env details added')
    return env_details


def clear_workflows(env_id):
    workflows = db_api.get_workflow(env_id)
    if workflows is not None and len(workflows) > 0:
        db_api.delete_workflow(env_id=env_id)
        print('remove exising workflow and create new. This will be removed soon. Not a safe practice')

def new_environment(args,env_type_cd):
    env = models.Environment()
    print('args',args)
    env.release_id = args.get('release_id')
    env.name = args.get('name')
    env.type_cd = env_type_cd
    if args.get('start_dt') is not None:
       env.start_dt = datetime.strptime(args.get('start_dt'), '%Y-%m-%dT%H:%M:%S.%fZ')
    env.create_dt = datetime.now()
    if args.get('end_dt') is not None:
       print ('End data {}'.format(args.get('end_dt')))
       #env.end_dt = datetime.strptime(args.get('end_dt'), '%Y-%m-%d')
    db_api.add_env_to_release(env)

def _map_wf(env_id, args, order=0, wf_id=None):
    wf = models.Workflow()
    if wf_id is not None:
       wf.wf_id = wf_id
    wf.env_id = env_id
    wf.create_dt = datetime.now()
    wf.name = args.get('name')
    wf.dag_name = derive_dag_name(wf_name=wf.name, env_id=env_id)
    wf.ignore_failure = args.get('ignore_failure', False)
    wf.planned_start_dt = args.get('planned_start_dt')
    wf.planned_end_dt = args.get('planned_end_dt')
    wf.actual_start_dt = args.get('actual_start_dt')
    wf.actual_end_dt = args.get('actual_end_dt')
    wf.status_cd = args.get('status_cd', stts_dfn.defined.status_cd)
    wf.description = args.get('description')
    wf.order = order
    wf.owner = args.get('owner', '')
    wf.frequency_cd = args.get('frequency_cd', 1)
    # if 'stages' in args.keys():
    #     stage_list = []
    #     from matilda_release.api.v2.handler import stage_handler
    #     for stage_item in args['stages']:
    #         stage_list.append(stage_handler._map_stage(0, stage_item, wf))
    #     wf.stages = stage_list
    return wf

def _map_stages():
    from matilda_release.api.v2.handler import stage_handler
    stage_handler._map_stage()


def get_workflow(env_id=None, wf_id=None):
    wf_list = db_api.get_workflow(env_id, wf_id)
    print ('workflow list {}'.format(wf_list))
    resp = []
    for item in wf_list:
        # item = item.to_dict()
        item['status_description'] = stts_hlpr.get_status(item.get('status_cd')).status_description
        item['frequency_description'] = stts_hlpr.get_frequency(item.get('frequency_cd')).frequency_description
        for key in workflow:
            if key not in item.keys():
                item[key] = None
        resp.append(item)
    print ('WF Result {}'.format(resp))
    return resp

def get_workflow_with_stages(rls_id=None, env_id=None, wf_id=None, include_env=False):
    from matilda_release.api.v2.handler import release_handler as rlsh, environment_handler as eh, stage_handler
    rls_info = db_api.get_release_details(release_id=rls_id)
    rls_type_cd = rls_info[0]['release_type_cd']
    rls = rlsh.get_release(release_id=rls_id, release_type_cd=rls_type_cd)
    if env_id != None:
       env = eh.get_environment_details(release_id=None, env_id=env_id)
    wf_list = get_workflow(env_id, wf_id)
    wf_resp = []
    print ('workflow list {}'.format(wf_list))
    for item in wf_list:
        # item = item.to_dict()
        for key in workflow:
            if key not in item.keys():
                item[key] = None
        stage_list = stage_handler.get_stages_with_tasks(item.get('wf_id'))
        item['release'] = rls[0].get('name')
        item['release_id'] = rls[0].get('release_id')
        if 'env' in locals():
           item['environment_name'] = env[0].get('name')
        item['stages'] = stage_list
        resp = calculate_progress(stage_list)
        item['overall_progress'] = resp['overall_progress']

        # item['status_cd'] = resp.get('status_cd')
        # item['status_description'] = resp.get('status_description')

        wf_resp.append(item)
    print ('Here you go {}'.format(wf_resp))

    if include_env:
        env_details = eh.get_environment_details(release_id=0, env_id=env_id)
        if isinstance(env_details, list):
            env_details = env_details[0]
            env_details['workflows'] = wf_resp
            return env_details

    return wf_resp

#def get_workflow(env_id=None, wf_id=None, extended=False, rls_id=None):
#    rls = rlsh.get_release(release_id=rls_id)
#    env = eh.get_environment_details(release_id=None, env_id=env_id)
#    wf_list = db_api.get_workflow(env_id, wf_id)
#    print ('workflow list {}'.format(wf_list))
#    resp = []
#    for item in wf_list:
#        item = item.to_dict()
#        for key in workflow:
#            if key not in item.keys():
#                item[key] = None
#        if extended:
#           stage_list = stage_handler.get_stages_with_tasks(item.get('wf_id'))
#           item['release'] = rls[0].get('name')
#           item['release_id'] = rls[0].get('release_id')
#           item['environment_name'] = env[0].get('name')
#           item['stages'] = stage_list
#           oresp = calculate_progress(stage_list)
#           item['overall_progress'] = oresp['overall_progress']
#           item['status'] = oresp['status']
#        resp.append(item)
#    print ("ANANDA WF: {}".format(resp))
#    return resp
#
#def get_workflow_with_stages(rls_id=None, env_id=None, wf_id=None):
#    rls = rlsh.get_release(release_id=rls_id)
#    env = eh.get_environment_details(release_id=None, env_id=env_id)
#    wf_resp = get_workflow(env_id, wf_id,True, rls_id)
#    return wf_resp

def create_infra_releaseenv(tasks,ip,os1):
    for i in range(len(tasks)):
        payload = tasks[0]['payload']
        print('payload %%%%',payload,type(payload),literal_eval(payload))
        loader = literal_eval(payload)
        print('tasks $$$$$', loader['host'],type(loader['host']))
        with open(loader['host'],'w') as f:
            f.write('['+ os1 +']'+'\n')
            #for j in range(len(ip)):
            f.write(ip[0]+ ' ansible_user=' + loader['source_user'] + ' ansible_password='+ loader['source_password'] + '\n')

    if os1 == 'centos':
        with open(str(os.getenv('AIRFLOW_HOME')) + '/dags/vault-yum.yml','w') as f2:
            f2.write(loader['source_user'] + ': ')
            f2.write('"' + loader['source_password'] + '"')
    elif os1 == 'ubuntu':
        with open(str(os.getenv('AIRFLOW_HOME')) + '/dags/vault-apt.yml','w') as f2:
            f2.write(loader['source_user'] + ': ')
            f2.write('"' + loader['source_password'] + '"')

def deploy_workflow(wf_id,rls_id=None,env_id=None):
    from matilda_release.api.v2.handler import service_handler, release_handler
    print ('Launching workflow',wf_id)
    wf = get_workflow_with_stages(rls_id=rls_id,env_id=env_id,wf_id=wf_id)
    print ('workflow output {}'.format(wf))
    tasks = []
    wf = wf[0]
    stages = wf.get('stages', [])
    for stage in stages:
        for item in stage.get('tasks',[]):
            component = service_handler.get_services(item.get('service_id'), False)[0]
            com_ac = service_handler.get_actions(item.get('action_id'))[0]
            print('Component {} action {}'.format(component, com_ac))
            print('Component Name {} Action {}'.format(component.get('name'), com_ac.get('name')))
            task = dict()
            task['wf_id'] = item.get('wf_id')
            task['dag_task_name'] = item.get('dag_task_name')
            task['name'] = item.get('name')
            task['component'] = component.get('name').replace(' ', '_')
            task['action'] = com_ac.get('name').replace(' ', '_')
            task['payload'] = item.get('input')
            tasks.append(task)

    print ('tasks to post {}'.format(tasks))
    print ('length of tasks {}'.format(len(tasks)))
    wf_req = collections.defaultdict()
    for k, v in iteritems(wf):
        if k not in ('stages', 'tasks'):
            wf_req[k] = v
    wf_req['tasks'] = tasks
    print("wf_req - {}".format(wf_req))

    rls_info = db_api.get_release_details(release_id=wf['release_id'])
    #print('rls_info###############',rls_info, tasks)
    if (rls_info[0]['release_type_cd'] == rls_dfn.infrastructure.release_type_cd and tasks[0]['action'] == 'run_playbook_hostfile'):
        impact = release_handler.get_impacted_systems(release_id = wf['release_id'])
        #print('impact_systemds %%%%%%%%%%%%%',impact,len(impact))
        ip = []
        os1 = 'None'
        index = 0;
        for i in range(len(impact)):
            if wf['environment_name'] == impact[i]['name']:
                index =i
                #print('interested impact $$$$$$',impact[i]['impactedSystems'],len(impact[i]['impactedSystems']))
                imp_sys = impact[i]['impactedSystems']
                if 'centos' in imp_sys[0]['os'].lower():
                    os1 = 'centos'
                    #print("os is ********",os1)
                elif 'ubuntu' in imp_sys[0]['os'].lower():
                    os1 = 'ubuntu'
                elif 'windows' in imp_sys[0]['os'].lower():
                    os1 = 'windows'
                for j in range(len(imp_sys)):
                    ip.append(imp_sys[j]['ip'])

                break
        test_str = str(os.getenv('AIRFLOW_HOME'))
        #print('ip addr &&&&&&&&',ip,test_str)
        create_infra_releaseenv(tasks,ip,os1)

        #print('Dev $$$$$$',impact[0],len(impact[0]['impactedSystems']))
        #print('Test $$$$$$',impact[1],len(impact[1]['impactedSystems']))
        #print('Prod $$$$$$',impact[2],len(impact[2]['impactedSystems']))
    builder = db.DAGBuilder()
    builder.construct_dag(wf_req)

    # below line of code is added to update the workflow and change the status to in progress and call the status helper to update the env
    workflow_from_db = db_api.get_workflow(wf_id=wf_id)
    for workflow in workflow_from_db:
        workflow['status_cd'] = stts_dfn.inProgress.status_cd
        print('workflow:{}'.format(workflow))
        db_api.update_workflow(wf_id=wf_id, data=workflow)
    stts_engine.check_and_update_workflow(wf_id=wf_id)



def calculate_progress(stages):
    task_count = {
        'configured' : 0,
        'success' : 0,
        'total': 0,
        'overall_progress': 0
    }
    status_cd = None
    for stage in stages:
        tasks = stage['tasks']
        for task in tasks:
            task_status_cd_from_db = task['status_cd']
            if task_status_cd_from_db == stts_dfn.success.status_cd:
                task_count['success'] += 1
            task_count['total'] += 1

    if task_count['total'] > 0:
        task_count['overall_progress'] = int(task_count.get('success')/task_count.get('total') * 100)
    print ("WF PROGRESS {}".format(task_count))
    return task_count


# def check_and_update_stage(wf_id):
#     stage_list = stage_handler.get_stage()
#     wf_status = db_api.get_workflow(env_id=None, wf_id=wf_id)
#     wf = {
#         'status': wf_status
#     }
#     for stage in stage_list:
#         if stage['status'] == 'in progress':
#             wf['status'] = 'in progress'
#         elif stage['status'].lower() in ['success', 'failed']:
#             wf['status'] = stage['status']
#         break
#     if wf_status != wf['status']:
#         if wf_status == 'in progress':
#             wf['actual_start_dt'] = datetime.now()
#         elif wf['status'] in ['success', 'failed']:
#             wf['actual_end_dt'] = datetime.now()
#     resp = db_api.update_stage(wf_id, wf)
#     return resp


def create_template(args):
    resp = dict()
    template_version = db_api.get_max_template_version(template_name=args.get('template_name'))
    args['template_version'] = template_version+1
    template_json = args.get('template_json')
    template_json['wf_id'] = 0
    template_json['release_id'] = 0
    template_json['dag_name'] = None
    template_json['create_dt'] = None
    template_json['planned_start_dt'] = None
    template_json['actual_start_dt'] = None
    template_json['planned_end_dt'] = None
    template_json['actual_end_dt'] = None
    template_json['env_id'] = 0
    template_json['status_cd'] = stts_dfn.defined.status_cd
    template_json['status_description'] = stts_dfn.defined.status_description
    for stage in template_json.get('stages'):
        stage['stage_id'] = 0
        stage['wf_id'] = 0
        stage['create_dt'] = None
        stage['planned_start_dt'] = None
        stage['actual_start_dt'] = None
        stage['planned_end_dt'] = None
        stage['actual_end_dt'] = None
        stage['status_cd'] = stts_dfn.defined.status_cd
        stage['status_description'] = stts_dfn.defined.status_description
        for task in stage.get('tasks'):
            task['task_id'] = 0
            task['dag_task_name'] = None
            task['wf_id'] = 0
            task['stage_id'] = 0
            task['create_dt'] = None
            task['planned_start_dt'] = None
            task['actual_start_dt'] = None
            task['planned_end_dt'] = None
            task['actual_end_dt'] = None
            task['status_cd'] = stts_dfn.defined.status_cd
            task['status_description'] = stts_dfn.defined.status_description
            task['duration'] = None
            task['output'] = None
    template_resp = db_api.create_template(args)
    resp.update(template_resp)
    return resp

def get_template(template_id=None, template_name=None):
    resp = db_api.get_template(template_id=template_id, template_name=template_name)
    return resp

def get_templates_drop_down_values(template_name=None):
    data_to_process = get_template(template_name=template_name)
    initial_template_dict = dict()
    print('data to process:{}'.format(data_to_process))
    for data in data_to_process:
        # print('data:{}'.format(data))
        template_name_from_db = data.get('template_name')
        # print(initial_template_dict.get(template_name_from_db))
        if initial_template_dict.get(template_name_from_db) == None:
            initial_template_dict[template_name_from_db] = list()
        create_versions_dict = dict()
        create_versions_dict['template_id'] = data.get('template_id')
        create_versions_dict['template_version'] = data.get('template_version')
        initial_template_dict[template_name_from_db].append(create_versions_dict)

    final_template_list = list()

    for k,v in initial_template_dict.items():
        temp_dict_template = dict()
        temp_dict_template['template_name'] = k
        temp_dict_template['template_details'] = v
        final_template_list.append(temp_dict_template)

    # print(final_template_list)
    return final_template_list



def get_frequency(frequency_cd=None):
    resp = db_api.get_frequency(frequency_cd=frequency_cd)
    return resp
# get_templates_drop_down_values('encrypted_template')

def create_frequency(args):
    resp = db_api.create_frequency(args)
    print(resp)
    return resp


def derive_dag_name(wf_name, env_id):
    return (db_api.get_release_name_env_name(env_id) + wf_name)

def get_jenkinsjob_parameters(args):
    resp = JenkinsPlugin(args)
    config = resp.get_job_config(args.get('job_name'))
    response = xmltodict.parse(config)
    parameters = response['project']['properties']['hudson.model.ParametersDefinitionProperty']['parametersDefinitions']['hudson.model.StringParameterDefinition']
    parameters_list = dict()
    for item in parameters:
        for k,v in item.items():
            if k == "name":
                parameters_list[v] = item.get('defaultValue')
    return parameters_list

# def update_workflows(env_id=None, args=None):
#     wf_list = db_api.get_workflow(env_id=env_id)
#     return_value = dict()
#     return_value['workflows']=list()
#
#     for iter in range(len(wf_list)):
#         print(wf_list)
#         print(args)
#         return_value = (update_workflow(workflow_dict=wf_list[iter], args=args))
#     return return_value
#
#
# def update_workflow(workflow_dict=None, wf_id=None, args=None):
#     from matilda_release.api.v2.handler import stage_handler
#     workflow = dict()
#     if workflow_dict is not None:
#         workflow = workflow_dict
#         wf_id = workflow_dict.get('wf_id')
#     elif wf_id is not None:
#         workflow = db_api.get_workflow(wf_id=wf_id)[0]
#     if wf_id is None:
#         raise BadRequest(' workflow id is needed for updating Workflow')
#     print('args:{}'.format(args))
#
#     for key in workflow:
#         for key_args, value in args.items():
#             if key == key_args:
#                 if value is not None:
#                     workflow[key] = value
#
#     stage_handler.update_stages(wf_id=wf_id, args=args.get('stages'))
#
#     print(workflow)
#
#     # if workflow.get('actual_end_dt') is not None:
#     #     workflow['actual_end_dt'] = datetime.strptime(workflow.get('actual_end_dt'), '%Y-%m-%dT%H:%M:%S.%fZ')
#     # if workflow.get('actual_start_dt') is not None:
#     #     workflow['actual_start_dt'] = datetime.strptime(workflow.get('actual_start_dt'), '%Y-%m-%dT%H:%M:%S.%fZ')
#     # if workflow.get('planned_end_dt') is not None:
#     #     workflow['planned_end_dt'] = datetime.strptime(workflow.get('planned_end_dt'), '%Y-%m-%dT%H:%M:%S.%fZ')
#     # if workflow.get('planned_start_dt') is not None:
#     #     workflow['planned_start_dt'] = datetime.strptime(workflow.get('planned_start_dt'), '%Y-%m-%dT%H:%M:%S.%fZ')
#     # if workflow.get('create_dt') is not None:
#     #     workflow['create_dt'] = workflow.get('create_dt')
#
#     db_api.update_workflow(wf_id=wf_id, data=workflow)
#
#     final_output =  get_workflow_with_stages(wf_id=workflow.get('wf_id'), include_env=True)
#     print('final_output:::::::::{}'.format(final_output))
#     return final_output
