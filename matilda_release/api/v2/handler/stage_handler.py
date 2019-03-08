import collections
import uuid
import requests
import json
import os

from datetime import datetime
from six import iteritems

from matilda_release.db import api as db_api
from matilda_release.db.sqlalchemy import models
from matilda_release.api.v2.model.model import stage

# from matilda_release.api.v2.handler import task_handler
from matilda_release.util.encoder import AESCipher
from matilda_release.util.status_helper import StatusDefinition as stts_dfn
from matilda_release.util import status_helper as stts_hlpr
from werkzeug.exceptions import BadRequest

def create_stage(wf_id, args):
    from matilda_release.api.v2.handler import task_handler
    resp = []
    print ("Is it true? {} ".format(isinstance(args, list)))
    if isinstance(args, list):
        for item in args:
            stage = _map_stage(wf_id, item, item.get('order', args.index(item)))
            st_resp = db_api.create_stage(stage)
            # if 'tasks' in item.keys():
            #     tk_resp = task_handler.create_task(st_resp.get('stage_id'), item['tasks'])
            #     st_resp['tasks'] = tk_resp
            # resp.append(st_resp)
    else:
        stage = _map_stage(wf_id, args)
        print("printing stage ************")
        st_resp = db_api.create_stage(stage)
        if 'tasks' in stage.keys():
            tk_resp = task_handler.create_task(st_resp.get('stage_id'), args['tasks'])
            st_resp['tasks'] = tk_resp
        resp.append(st_resp)
    for wf in resp:
        for k, v in iteritems(wf):
            if isinstance(v, datetime):
                wf[k] = datetime.strftime(v,'%Y-%m-%dT%H:%M:%S.%fZ') if v is not None else None
    return resp


def _map_stage(wf_id, args, wf=None, order=0):
    stage = models.Stage()
    if wf_id != 0:
        stage.wf_id = wf_id
    stage.create_dt = datetime.now()
    stage.stage_ui_id = args.get('stage_ui_id')
    stage.status_cd = args.get('status_cd', stts_dfn.defined.status_cd)
    if args.get('actual_end_dt') is not None:
        stage.actual_end_dt = datetime.strptime(args.get('actual_end_dt'), '%Y-%m-%dT%H:%M:%S.%fZ')
    if args.get('actual_start_dt') is not None:
        stage.actual_end_dt = datetime.strptime(args.get('actual_start_dt'), '%Y-%m-%dT%H:%M:%S.%fZ')
    if args.get('planned_end_dt') is not None:
        stage.actual_end_dt = datetime.strptime(args.get('planned_end_dt'), '%Y-%m-%dT%H:%M:%S.%fZ')
    if args.get('planned_start_dt') is not None:
        stage.actual_end_dt = datetime.strptime(args.get('planned_start_dt'), '%Y-%m-%dT%H:%M:%S.%fZ')
    stage.name = args.get('name')
    stage.order = order
    stage.owner = args.get('owner')
    if 'tasks' in args.keys():
        task_list = []
        from matilda_release.api.v2.handler import task_handler
        for task_item in args['tasks']:
            task_list.append(task_handler._map_task(0, task_item, wf_id))
        stage.tasks = task_list
    return stage


def get_stage(wf_id=None, stage_id=None):
    stage_list = db_api.get_stage(wf_id, stage_id)
    for item in stage_list:
        item['status_description'] = stts_hlpr.get_status(item.get('status_cd')).status_description
        for key in stage:
            if key not in item.keys():
                item[key] = None
    return stage_list

def get_stages_with_tasks(wf_id=None, stage_id=None):
    from matilda_release.api.v2.handler import task_handler
    stage_list = get_stage(wf_id, stage_id)
    enc = AESCipher()
    sg_resp = []
    for item in stage_list:
        # item = item.to_dict()
        for key in stage:
            if key not in item.keys():
                item[key] = None
        task_resp = task_handler.get_task(stage_id=item.get('stage_id'))
        print ('stage id {} and task list {}'.format(item.get('stage_id'), task_resp))
        item['tasks'] = task_resp
        sg_resp.append(item)
    print ('Stage list {}'.format(sg_resp))
    return sg_resp



# def update_stages(wf_id=None, args=None):
#     stage_list = db_api.get_stage(wf_id=wf_id)
#     return_value = dict()
#     return_value['stages']=list()
#     count = len(args)
#     init_value = 0
#     for iter in range(len(stage_list)):
#         if init_value < count:
#             init_value+=1
#             return_value['stages'].append(update_stage(stage_dict=stage_list[iter], args=args[iter]))
#         else:
#             db_api.delete_stage(stage_list[iter].get('stage_id'))
#     return return_value
#
#
# def update_stage(stage_dict=None, stage_id=None, args=None):
#     from matilda_release.api.v2.handler import task_handler
#     stage = dict()
#     if stage_dict is not None:
#         stage = stage_dict
#         stage_id = stage_dict.get('stage_id')
#     elif stage_id is not None:
#         stage = db_api.get_stage(stage_id_id=stage_id)[0]
#     if stage_id is None:
#         raise BadRequest('Task Id is need for updating Task')
#
#     for key in stage:
#         for key_args, value in args.items():
#             if key == key_args:
#                 if value is not None:
#                     stage[key] = value
#
#     tasks = task_handler.update_tasks(stage_id=stage_id, args=args['tasks'])
#
#     db_api.update_stage(stage_id=stage_id, data=stage)
#
#     output_stage =  get_stage(stage_id=stage.get('stage_id'))
#
#     # if output_stage.get('actual_end_dt') is not None:
#     #     output_stage['actual_end_dt'] = datetime.strptime(output_stage.get('actual_end_dt'), '%Y-%m-%dT%H:%M:%S.%fZ')
#     # if output_stage.get('actual_start_dt') is not None:
#     #     output_stage['actual_start_dt'] = datetime.strptime(output_stage.get('actual_start_dt'), '%Y-%m-%dT%H:%M:%S.%fZ')
#     # if output_stage.get('planned_end_dt') is not None:
#     #     output_stage['planned_end_dt'] = datetime.strptime(output_stage.get('planned_end_dt'), '%Y-%m-%dT%H:%M:%S.%fZ')
#     # if output_stage.get('planned_start_dt') is not None:
#     #     output_stage['planned_start_dt'] = datetime.strptime(output_stage.get('planned_start_dt'), '%Y-%m-%dT%H:%M:%S.%fZ')
#     # output_stage['tasks'] = tasks
#
#     return output_stage
