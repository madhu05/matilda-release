import collections
import uuid
import requests
import json
import os
import itertools
from matilda_release.db.sqlalchemy import api as IMPL

from datetime import datetime
from six import iteritems

from matilda_release.db import api as db_api
from matilda_release.db.sqlalchemy import models
from matilda_release.api.v2.model.model import service, Options

def test_create_service():

    args = {'name': 'demo', 'category': 'Tracking', 'comments': '1.0;Matilda'}
    resp = IMPL.create_service(args)

    assert resp['name'] == args.get('name')
    assert resp['category'] == args.get('category')


def test_create_action():


    args= {'name': 'test_sample', 'description': 'demo', 'service_id': 1}
    resp = IMPL.create_action(args)

    assert resp['name'] == args.get('name')
    assert resp['service_id'] == args.get('service_id')
    assert resp['description'] == args.get('description')


def test_get_service():
    def get_actions(action_id=None, service_id=None):
        ac_list = db_api.get_action(action_id=action_id, service_id=service_id)
        res = []
        for item in ac_list:
            res.append(item.to_dict())
        return res

    sv_list = db_api.get_service(service_id=None)
    resp = []
    print('service list {}'.format(sv_list))
    for item in sv_list:
        svc = item.to_dict()
        for key in service:
            if key not in svc.keys():
                svc[key] = None
                svc['actions'] = get_actions(service_id=svc.get('service_id'))
        resp.append(svc)

    db_values = IMPL.get_service(service_id=None)

    """  Checking for the first value """
    print(resp[0])
    assert resp[0]['service_id'] == db_values[0]['service_id']
    assert resp[0]['name'] == db_values[0]['name']
    assert resp[0]['category'] == db_values[0]['category']

    """ Checking for actions with service_id = 1 i.e first value """
    actions_first = get_actions(service_id=1)
    print(actions_first)

    assert resp[0]['actions'][0]['action_id'] == actions_first[0]['action_id']
    assert resp[0]['actions'][0]['name'] == actions_first[0]['name']
    assert resp[0]['actions'][0]['description'] == actions_first[0]['description']
    assert resp[0]['actions'][0]['service_id'] == actions_first[0]['service_id']


def test_get_service_fields():
    svf_list = db_api.get_service_fields(service_id=1, action_id=1)
    """ Checking with values service_id = 1 and action_id = 1"""
    resp = []
    for svf in svf_list:
        svf = svf.to_dict()
        svf['controlType'] = svf['control_type']
        required = svf.get('required')
        if required is not None:
            svf['required'] = bool(int(svf.get('required')))
        else:
            svf['required'] = False
        options = svf.get('options')
        if isinstance(options, list):
            op = Options()
            svf['options'] = op.format(options)
        resp.append(svf)

    print(resp[0])


    assert resp[0]['service_field_id'] == svf_list[0]['service_field_id']
    assert resp[0]['key'] == svf_list[0]['key']
    assert resp[0]['label'] == svf_list[0]['label']
    assert resp[0]['placeholder'] == svf_list[0]['placeholder']
    assert resp[0]['control_type'] == svf_list[0]['control_type']
    #assert resp[0]['required'] == svf_list[0]['required']
    assert resp[0]['order'] == svf_list[0]['order']
    assert resp[0]['options'] == svf_list[0]['options']
    assert resp[0]['field_type'] == svf_list[0]['field_type']
    assert resp[0]['description'] == svf_list[0]['description']
    assert resp[0]['service_id'] == svf_list[0]['service_id']
    assert resp[0]['action_id'] == svf_list[0]['action_id']













