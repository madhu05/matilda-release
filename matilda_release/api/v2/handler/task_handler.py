from datetime import datetime
from six import iteritems
from ast import literal_eval
from matilda_release.db import api as db_api
from matilda_release.db.sqlalchemy import models
from matilda_release.api.v2.model.model import task
from matilda_release.util import encoder
from matilda_release.util import json_helper
from matilda_release.util.status_helper import StatusDefinition as stts_dfn
from matilda_release.util import status_helper as stts_hlpr
from matilda_release.util import status_engine as stts_engine
from werkzeug.exceptions import BadRequest

from matilda_release.api.v2.handler import service_handler as sh


enc = encoder.AESCipher()
# stg = lambda: matilda_release.api.v2.handler.stage_handler

def create_task(stage_id, args):
    resp = []
    if isinstance(args, list):
        for item in args:
            tk = _map_task(stage_id, item, item.get('order', args.index(item)))
            #print('tk args',tk)

            resp.append(db_api.create_task(tk)[0])
    else:
        tk = _map_task(stage_id, args)
        return db_api.create_task(tk)[0]
    for wf in resp:
        response_input = wf.get('input')
        response_output = wf.get('output')
        if response_input!=None and len(response_input)!=0:
            wf['input'] = enc.decrypt(response_input)
        if response_output!=None and len(response_output)!=0:
            try:
                wf['output'] = enc.decrypt(response_output)
                eval(wf['output'])
            except Exception as e:
                wf['output'] = "{'error':'unable to decrypt output'}"
        for k, v in iteritems(wf):
            if isinstance(v, datetime):
                wf[k] = datetime.strftime(v, '%Y-%m-%dT%H:%M:%S.%fZ') if v is not None else None

    return resp

def _map_task(stage_id, args, wf_id=None, order=0):
    tk = models.Task()
    if stage_id != 0:
        tk.stage_id = stage_id
    tk.create_dt = datetime.now()
    tk.task_ui_id = args.get('task_ui_id')
    tk.status_cd = args.get('status_cd', stts_dfn.defined.status_cd)
    tk.wf_id = wf_id
    tk.dag_task_name = args.get('name') + '_' + str(wf_id)
    #print('task_args',args)
    if args.get('actual_end_dt') is not None:
        tk.actual_end_dt = datetime.strptime(args.get('actual_end_dt'), '%Y-%m-%dT%H:%M:%S.%fZ')
    if args.get('actual_start_dt') is not None:
        tk.actual_start_dt = datetime.strptime(args.get('actual_start_dt'), '%Y-%m-%dT%H:%M:%S.%fZ')
    if args.get('planned_end_dt') is not None:
        tk.planned_end_dt = datetime.strptime(args.get('planned_end_dt'), '%Y-%m-%dT%H:%M:%S.%fZ')
    tk.planned_start_dt = None
    tk.name = args.get('name')
    tk.order = order
    tk.ignore_failure = args.get('ignore_failure', False)
    tk.service_id = args.get('service_id')
    tk.action_id = args.get('action_id')
    # a = enc.encrypt(str(args.get('input')))
    # tk.input = json.dumps(a.decode()).replace("'", '"')[1:-1]
    task_input = args.get('input')
    task_output = args.get('output')
    if task_input!=None and len(task_input)!=0:
        tk.input = enc.encrypt(json_helper.create_dict_from_json_string(args.get('input')))
        tk.status_cd = stts_dfn.configured.status_cd
    else:
        tk.status_cd = stts_dfn.defined.status_cd
    if task_output != None and len(task_output)!=0:
        tk.output = enc.encrypt(json_helper.create_dict_from_json_string(args.get('output')))
    return tk

def get_task(task_id=None, dag_task_name=None, stage_id=None):

    task_list = db_api.get_task(task_id=task_id, dag_task_name=dag_task_name, stage_id=stage_id)
    for item in task_list:
        item['service_name'], item['action_name'] = _get_service_action(item['service_id'], item['action_id'])
        if item.get('input') is not None and item.get('input') != '':
            decrypted_input = enc.decrypt(item['input'])
            item['input'] = decrypted_input
            print("item['input'] - {}".format(item['input']))
        if item.get('output') is not None and item.get('output') != '':
            try:
                decrypted_output = enc.decrypt(item['output'])
                eval(decrypted_output)
            except Exception as e:
                decrypted_output = "{'error':'unable to decrypt output'}"

            item['output'] = decrypted_output
            print("item['output'] - {}".format(item['output']))
        item['status_description'] = stts_hlpr.get_status(item.get('status_cd')).status_description

        for key in task:
            if key not in item.keys():
                item[key] = None
    return task_list

def _get_service_action(service_id, action_id):
    svc = sh.get_services(service_id=service_id, by_category=False)
    if isinstance(svc, list):
        svc = svc[0]
    for ac in svc['actions']:
        if action_id == ac['action_id']:
            return svc['name'].replace('_', ' ').title(), ac['name'].replace('_', ' ').title()

def update_task_stats(task_id=None, dag_task_name=None, data=None):
    if task_id is None and dag_task_name is None:
        raise BadRequest('task_id or dag_task_name is needed to update task status')
    return stts_engine.check_and_update_task(task_id=task_id, dag_task_name=dag_task_name,  data=data)

