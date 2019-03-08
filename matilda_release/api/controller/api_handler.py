import collections
import uuid
import requests
import json
import os

from datetime import datetime
from six import iteritems

from matilda_release.db import api as db_api
from matilda_release.db.sqlalchemy import models
from matilda_release.service.features import jira_client



def create_release(args, type='app'):
    resp_args = args
    rel_id = '_'.join([args.get('releasename')[0:10], args.get('project').replace(' ','-').lower()[0:10],
                       args.get('application').replace(' ','-').lower()[0:10], args.get('releaseversion') ])
    if args.get('release_dt') is not None:
        args['release_dt'] = datetime.strptime(args['releaseschedule'], '%Y-%m-%d')
    if type == 'infra':
        args['infra_release_id'] = 'infra_' + rel_id
        resp_args['release_id'] = args['infra_release_id']
        args = map_create_release_params(args)
        resp = db_api.create_infra_release(args)
        type_release_id = resp.get('infra_release_id')
    else:
        args['app_release_id'] = 'app_' + rel_id
        resp_args['release_id'] = args['app_release_id']
        args = map_create_release_params(args)
        resp = db_api.create_app_release(args)
        type_release_id = resp.get('app_release_id')

    if 'selected_additional_releaseplans' in args.keys():
        link_artifacts(type_release_id, type, args['selected_additional_releaseplans'])

    resp_args['environment_list'] = get_default_environments()
    save_req_data(resp_args['release_id'], type, resp_args)
    return resp_args

def _check_release_params(args):
    pass

def map_create_release_params(rls):
    args = {
        'app_release_id': rls['app_release_id'],
        'name': rls['releasename'],
        'version': rls['releaseversion'],
        'release_id': rls['app_release_id'],
        'application': rls['application'],
        'comments': rls['description'],
        'release_dt': rls['releaseschedule'],
        'project': rls['project'],
        'status': 'Planning'
    }
    return args


def get_release(type='app', release_id=None, filter=None):
    if type == 'app':
        resp = db_api.get_app_release_info(release_id, filter)
        ert_resp = []
        for item in resp:
            rl_info = item.to_dict()
            links = get_release_links(rl_info.get('app_release_id'))
            rl_info['selected_additional_releaseplans'] = links
            ert_resp.append(rl_info)

        if release_id != None:
            ert_resp = get_workflow(release_id)

        return ert_resp

def get_release_links(release_id, type='app'):
    rel_links = db_api.get_release_links(release_id, type)
    data = []
    for rel_link in rel_links:
        rl = rel_link.to_dict()
        rl_items = db_api.get_release_link_items(rl.get('link_id'))
        rl_item_list = []
        for rl_item in rl_items:
            rl_item_list.append(rl_item.to_dict())
        rl['links'] = rl_item_list
        data.append(rl)
    resp = build_ui_link_resp(data)
    return resp

def build_ui_link_resp(rel_links):
    resp = collections.defaultdict
    for item in rel_links:
        resp[item.get('type')] = item.get('links', [])
    return resp


def link_artifacts(release_id, type, artifact_data):
    if type is None:
        type = 'app'

    for k, v in iteritems(artifact_data):
        rel_link_info = models.ReleaseLink()
        rel_link_info.link_id = str(uuid.uuid4())
        rel_link_info.release_id = release_id
        rel_link_info.release_type = type
        rel_link_info.name = None
        rel_link_info.source = None
        rel_link_info.url = None
        db_api.add_link_to_release(rel_link_info)
        for item in v:
            rel_link_item = models.ReleaseLinkItem()
            rel_link_item.link_id = rel_link_info.link_id
            rel_link_item.value = item.get('id')
            db_api.add_link_items(rel_link_item)

def create_environment(release_id, type, args):
    env = models.ReleaseEnv
    env.release_id = release_id
    env.release_type = type
    env.name = args.get('name')
    env.create_dt = args.get('create_dt', datetime.now())
    env.env_type = args.get('env_type')
    env.dependent_env = args.get('dependent_env')
    env.status = args.get('status' or 'Planning')
    resp = db_api.add_env_to_release(env)
    return resp.to_dict()

def get_environments(release_id, extended=True):
    env_list = db_api.get_release_environments(release_id=release_id)
    resp = []
    for env in env_list:
        ed = env.to_dict()
        if extended:
            ed_details = get_environment_details(ed.get('release_env_id'))
            ed_stats = get_env_execution_stats(ed.get('release_env_id'))
            ed['details'] = ed_details
            ed['stats'] = ed_stats
        resp.append(ed)
    return resp

def get_environment_details(env_id):
    envs = db_api.get_release_environment_details(env_id)
    resp = []
    for env in envs:
        resp.append(env.to_dict())
    return resp

def get_env_execution_stats(env_id):
    envs = db_api.get_release_environment_execution_stats(env_id)
    resp = []
    for env in envs:
        resp.append(env.to_dict())
    return resp

def get_artifact_types():
    data = {'artifact_types': ['Features', 'Test Suites', 'Wiki Links', 'Design Documents', 'Other']}
    return data

def get_artifacts(artifact_type, project=None, application=None):
    if artifact_type == 'Features':
        #epics = jira_client.get_features()
        #return _build_ui_resp(artifact_type, epics)
        with open('features.json') as f:
            data = json.load(f)
        return data
    elif artifact_type == 'TestSuites':
        # epics = jira_client.get_features()
        # return _build_ui_resp(artifact_type, epics)
        with open('test_suite.json') as f:
            data = json.load(f)
        return data


def _build_ui_resp(type, data):
    columns = []
    for k in data[0].keys():
        d = {
                "primaryKey": k,
                "header": k.replace('_', ' ').title()
            }
        columns.append(d)
    resp = {
        'title': type,
        'columns': columns,
        'rows': data
    }
    return resp

#TODO: Remove this later

def get_default_environments():
    env_list = ['dev', 'qa', 'prod']
    resp = []
    for env in env_list:
        ev = models.ReleaseEnv()
        ev.env_type = env.upper()
        ev.status = 'Not Configured'
        resp.append(ev.to_dict())
    return resp

def get_create_mock_environments(count):
    env_list = ['dev', 'qa', 'prod']
    resp = []
    for env in env_list:
        ev = models.ReleaseEnv()
        ev.env_type = env.upper()
        if env == 'dev':
            ev.status = 'Configured'
        else:
            ev.status = 'Not Configured'
        ev.stages = count
        evd = ev.to_dict()
        evd['Scheduled'] = count
        evd['Success'] = 0
        evd['Failed'] = 0
        evd['In Progress'] = 0
        resp.append(evd)
    return resp

def get_get_mock_environments(count):
    env_list = ['dev', 'qa', 'prod']
    resp = []
    for env in env_list:
        ev = models.ReleaseEnv()
        ev.env_type = env.upper()
        ev.status = 'Configured'
        ev.stages = count
        evd = ev.to_dict()
        evd['Scheduled'] = count
        evd['Success'] = 0.3 * count
        evd['Failed'] = 0.1 * count
        evd['In Progress'] = 0.6 * count
        resp.append(evd)
    return resp

def create_workflow(release_id, env, env_data):
    headers = {'Content-type': 'application/json', 'Accepts': 'application/json'}
    url = 'http://localhost:6031/matilda/wf/workflow/create'
    resp = requests.post(url=url, headers=headers, data=json.dumps(env_data))
    json_data = get_req_data(release_id)
    print ('JSON Data {}'.format(json_data))
    task_count = 0
    for item in env_data['workflowitems']:
        task_count += len(item['tasks'])
    json_data['environment_list'] = get_create_mock_environments(task_count)
    return json_data

def get_workflow(release_id, env, workflow_id):
    workflow_id = '1544512f3'
    headers = {'Content-type': 'application/json', 'Accepts': 'application/json'}
    url = 'http://localhost:6031/matilda/wf/workflow/' + workflow_id
    resp = requests.get(url=url, headers=headers)
    resp = resp.json()
    print(resp)
    json_data = get_req_data(release_id)
    task_count = 0
    for item in resp['workflowitems']:
        task_count += len(item['tasks'])
    json_data['environment_list'] = get_get_mock_environments(task_count)
    return json_data

def get_full_workflow(release_id, **kwargs):
    workflow_id = '1544512f3'
    headers = {'Content-type': 'application/json', 'Accepts': 'application/json'}
    url = 'http://localhost:6031/matilda/wf/workflow/' + workflow_id
    resp = requests.get(url=url, headers=headers)
    resp = resp.json()
    print(resp)
    return resp

def save_req_data(req_id, type, args):
    rd = models.ReleaseReqData
    rd.req_id = req_id
    rd.type = type or 'app'
    rd.req_data = args
    data = {
        'req_id': req_id,
        'type': type or 'app',
        'req_data': args
    }
    return db_api.save_req_data(data)

def get_req_data(req_id):
    resp = db_api.get_req_data(req_id)
    print ('Resp here {}'.format(resp))
    return resp.to_dict()

