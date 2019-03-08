import collections
import uuid
import requests
import json
import os

from datetime import datetime
from six import iteritems
from werkzeug.exceptions import BadRequest

from matilda_release.db import api as db_api
from matilda_release.db.sqlalchemy import models
from matilda_release.util.status_helper import StatusDefinition as stts_dfn
from matilda_release.util.status_helper import EnvTypeDefinition as env_dfn
from matilda_release.util import status_helper as stts_hlpr


def create_environment(release_id, args):
    print(release_id, args)
    if check_env_name(release_id=release_id, env_name=args.get('name')):
        raise BadRequest(
            'Environment Name {} already exists for the release'.format(
                args.get('name')))

    env = models.Environment()
    env.release_id = release_id
    env.name = args.get('name')
    env.env_type_cd = args.get('env_type_cd')

    if env.env_type_cd is None or env.env_type_cd == 0:
        env.type_cd = env_dfn.development.env_type_cd

    if args.get('start_dt') is not None:
        env.start_dt = datetime.strptime(
            args.get('start_dt'), '%Y-%m-%dT%H:%M:%S.%fZ')
    env.create_dt = datetime.now()
    env.status_cd = stts_dfn.defined.status_cd

    resp = db_api.add_env_to_release(env)

    resp['status_description'] = stts_hlpr.get_status(
        env.status_cd).status_description
    resp['env_type_description'] = stts_hlpr.get_env_type(
        env.env_type_cd).env_type_description
    resp['start_dt'] = datetime.strftime(
        resp['start_dt'],
        '%Y-%m-%dT%H:%M:%S') if resp['start_dt'] is not None else None
    resp['create_dt'] = datetime.strftime(
        resp['create_dt'],
        '%Y-%m-%dT%H:%M:%S') if resp['create_dt'] is not None else None
    return resp


def check_env_name(release_id, env_name):
    # filters = {
    #     'name': env_name
    # }
    env_resp = db_api.get_environment(release_id=release_id, name=env_name)
    if len(env_resp) > 0:
        return True
    return False


def get_environment(release_id=None, env_id=None, filters=None, env_type_cd=None, env_name=None):
    env_list = db_api.get_environment(
        release_id=release_id,
        env_id=env_id,
        filters=filters, env_type_cd=env_type_cd, name=env_name)
    for item in env_list:
        item['status_description'] = stts_hlpr.get_status(
            item.get('status_cd')).status_description
        item['env_type_description'] = stts_hlpr.get_env_type(
            item.get('env_type_cd')).env_type_description
    return env_list


def get_environments(release_id=None, extended=True, env_id=None):
    from matilda_release.api.v2.handler import workflow_handler
    env_list = get_environment(release_id=release_id, env_id=env_id)
    resp = []
    for ed in env_list:
        ed['status_description'] = stts_hlpr.get_status(
            ed.get('status_cd')).status_description
        ed['env_type_description'] = stts_hlpr.get_env_type(
            ed.get('env_type_cd')).env_type_description
        ed['create_dt'] = datetime.strftime(
            ed['create_dt'],
            '%Y-%m-%dT%H:%M:%S') if ed['create_dt'] is not None else None
        ed['release_id'] = release_id
        if extended:
            wfs = workflow_handler.get_workflow(env_id=ed.get('env_id'))
            for wf in wfs:
                wf['release_id'] = release_id
            ed['workflows'] = wfs
        resp.append(ed)
    return resp


def get_environment_details(release_id=0, env_id=0):
    return get_environments(
        release_id=release_id,
        extended=True,
        env_id=env_id)


def get_env_execution_stats(env_id):
    envs = db_api.get_release_environment_execution_stats(env_id)
    resp = []
    for env in envs:
        resp.append(env.to_dict())
    return resp


def update_environment(env_id, data):
    args = {}
    if 'status_cd' in data.keys():
        args['status_cd'] = data.get('status_cd')

    db_api.update_environment(env_id, args)


def start_environment(env_id, rls_id):
    from matilda_release.api.v2.handler import workflow_handler
    wfs = workflow_handler.get_workflow(env_id=env_id)
    resp = {}
    if len(wfs) > 0:
        resp = workflow_handler.deploy_workflow(
            wf_id=wfs[0].get('wf_id'), rls_id=rls_id, env_id=env_id)
    return resp


def clone_environment(
        release_id,
        source_env_id,
        target_env_name,
        target_env_type_cd):

    from matilda_release.api.v2.handler import workflow_handler
    environment_to_clone = get_environment(env_id=source_env_id)

    for env in environment_to_clone:
        new_env = dict.copy(env)
        new_env['id'] = 0
        new_env['name'] = target_env_name
        new_env['env_type_cd'] = target_env_type_cd
        new_env['status_cd'] = stts_dfn.defined.status_cd
        new_env['start_dt'] = None
        new_env['created_dt'] = None
        new_env['end_dt'] = None
        new_created_environment = create_environment(release_id, new_env)
        new_env_id = new_created_environment.get('env_id')
        wfs = workflow_handler.get_workflow_with_stages(
            rls_id=release_id, env_id=source_env_id)
        if len(wfs) > 1:
            raise BadRequest(
                'Env has more than one work flow, env_id={}'.format(source_env_id))
        if wfs is not None and len(wfs) > 0:
            temp_wfs = wfs[0]
            temp_wfs['wf_id'] = 0
            temp_wfs['release_id'] = release_id
            temp_wfs['dag_name'] = None
            temp_wfs['create_dt'] = None
            temp_wfs['planned_start_dt'] = None
            temp_wfs['actual_start_dt'] = None
            temp_wfs['planned_end_dt'] = None
            temp_wfs['actual_end_dt'] = None
            temp_wfs['env_id'] = new_env_id
            temp_wfs['status_cd'] = stts_dfn.defined.status_cd
            temp_wfs['status_description'] = stts_dfn.defined.status_description
            for stage in temp_wfs.get('stages'):
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
            resp = workflow_handler.create_workflow(
                new_env_id, None, temp_wfs, include_env=True)

            return resp


def get_env_type_cd():
    return db_api.get_env_type_cd()

