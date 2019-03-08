import logging,pytest,config,datetime,os,json,random
from flask import request
from flask_restplus import Resource
from matilda_release.api.v2.restplus import api
from matilda_release.api.v2.model.model import stage, stage_with_tasks
from matilda_release.api.v2.handler import stage_handler
from matilda_release.db.sqlalchemy import api as IMPL
from matilda_release.api.v2.handler import task_handler
from datetime import datetime
from matilda_release.db import api as db_api
from matilda_release.db.sqlalchemy import models
from matilda_release.api.v2.handler import task_handler
from matilda_release.util.status_helper import StatusDefinition as stts_dfn
arg1 = {"stage_id": 1, "stage_ui_id": "new", "name": "new", "create_dt": "2018-12-17T14:58:35","actual_end_dt": "2018-12-17T20:55:38",
         "status_cd": 1, "owner": "matilda", "order": 1, "workflow_id": 1}
arg2 = {"stage_id": 2,"name": "DemoHack", "stage_ui_id": "Hack", "create_dt": "2018-12-17T14:59:20","actual_end_dt": "2018-12-03T20:02:07", "status_cd": 1, "owner": "Hack", "order": 0, "workflow_id": 1}

args = [arg1,arg2]


def test_create_stage(wf_id=1, args=args):
    resp = []
    if isinstance(args, list):
        a = len(resp)
        for i in args:
            e = len(resp)
            print(resp)
            db = IMPL.get_stage(1,1)
            # assert args['stage_id'] == stage[0]['stage_id']
            assert args[0]['name'] == db[0]['name']
            assert args[0]['status_cd'] == db[0]['status_cd']
            assert args[0]['name'] == db[0]['name']
            assert args[0]['order'] == db[0]['order']
        else:
            resp = stage_handler.get_stage(1)
            db = IMPL.get_stage(1, 1)  # Values from database
            a = len(resp)
            for i in range(0, a):
                if resp[0]['name'] == db[0]['name']:
                    e = resp[i]
                    assert resp[0]['name'] == db[0]['name']
                    assert resp[0]['status_cd'] == db[0]['status_cd']
                    assert resp[0]['owner'] == db[0]['owner']
                    assert resp[0]['order'] == db[0]['order']


def test_get_stage(wf_id=None, stage_id=None):
    stage_list = db_api.get_stage(1, 1)
    db = IMPL.get_stage(1, 1)
    assert stage_list[0]['name'] == db[0]['name']
    assert stage_list[0]['status_cd'] == db[0]['status_cd']
    assert stage_list[0]['owner'] == db[0]['owner']
    assert stage_list[0]['order'] == db[0]['order']


def get_stages_with_tasks(wf_id=None, stage_id=None):
    task_resp = task_handler.get_task(1)
    db = IMPL.get_stage(1, 1)
    assert task_resp[0]['name'] == db[0]['name']
    assert task_resp[0]['status_cd'] == db[0]['status_cd']
    assert task_resp[0]['owner'] == db[0]['owner']
    assert task_resp[0]['order'] == db[0]['order']






