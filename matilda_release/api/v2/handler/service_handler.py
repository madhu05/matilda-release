import collections
import uuid
import requests
import json
import os
import itertools

from datetime import datetime
from six import iteritems

from matilda_release.db import api as db_api
from matilda_release.db.sqlalchemy import models
from matilda_release.api.v2.model.model import service, Options

def create_service(args):
    sv = models.Service()
    sv.service_id = args.get('service_id')
    sv.name = args.get('name')
    sv.category = args.get('category')
    sv.comments = args.get('comments')
    service_from_db = db_api.get_service(service_id=sv.service_id)
    if service_from_db is not None and len(service_from_db)>0:
        print('service already exists, updating existing service')
        resp = db_api.update_service(service_id=sv.service_id, data=sv)
    else:
        resp = db_api.create_service(sv)
    return resp

def create_action(service_id, args):
    ac = models.Action()
    ac.service_id = service_id
    ac.action_id = args.get('action_id')
    ac.name = args.get('name')
    ac.description = args.get('description')
    action_from_db = db_api.get_action(service_id=service_id, action_id=ac.action_id)
    if action_from_db is not None and len(action_from_db)>0:
        print('action already exists, updating existing action')
        resp = db_api.update_action(action_id=ac.action_id, data=ac)
    else:
        resp = db_api.create_action(ac)
    return resp

def create_service_fields(service_id, action_id, args):
    svf = models.ServiceFields()
    svf.service_id = service_id
    svf.action_id = action_id
    svf.service_field_id = args.get('service_field_id')
    svf.description = args.get('description')
    svf.order = args.get('order')
    svf.control_type = args.get('controlType')
    svf.field_type = args.get('field_type')
    svf.key = args.get('key')
    svf.label = args.get('label')
    svf.options = args.get('options')
    svf.placeholder = args.get('placeholder')
    args_required = args.get('required', False)
    print('args {}'.format(args_required))
    if args_required is not None:
        svf.required = eval(args_required.title())
        print('svf required:{}'.format(svf.required))
    else:
        svf.required = False
        print('else svf{}'.format(svf.required))

    service_field_from_db = db_api.get_service_fields(service_id=service_id, action_id=action_id, service_field_id=svf.service_field_id)
    if service_field_from_db is not None and len(service_field_from_db)>0:
        print('service field already exists, updating existing service field')
        svf.service_field_id = service_field_from_db[0].get('service_field_id')
        resp = db_api.update_service_fields(service_field_id=svf.service_field_id, data=svf)
    else:
        resp = db_api.create_service_fields(svf)
    print('resp:{}'.format(resp))
    return resp

def create_output_fields(service_id, action_id, args):
    sof = models.ServiceActionOutputField()
    sof.service_id = service_id
    sof.action_id = action_id
    sof.output_field_id = args.get('output_field_id')
    sof.output_field_name = args.get('output_field_name')

    output_field_from_db = db_api.get_output_fields(service_id=service_id, action_id=action_id, output_field_id=sof.output_field_id)
    if output_field_from_db is not None and len(output_field_from_db)>0:
        print('service field already exists, updating existing service field')
        resp = db_api.update_output_fields(output_field_id=sof.output_field_id, data=sof)
    else:
        resp = db_api.create_output_fields(sof)
    print('resp:{}'.format(resp))
    return resp

def get_services(service_id=None, by_category=True):
    sv_list = db_api.get_service(service_id=service_id)
    resp = []
    print ('service list {}'.format(sv_list))
    for item in sv_list:
        svc = item.to_dict()
        for key in service:
            if key not in svc.keys():
                svc[key] = None
                svc['actions'] = get_actions(service_id=svc.get('service_id'))
        resp.append(svc)
    if by_category:
        # resp = get_services_by_category(resp)
        resp = get_services_by_category_new(resp)
    print ('Service resp {}'.format(resp))
    return resp

# not using this method since lamba consolidation is not happening correctly for items not in sequence
def get_services_by_category(data):
    svc_resp = []
    for key, group in itertools.groupby(data, key=lambda x: x['category']):
        tmp = {}
        tmp['name'] = key
        tmp['services'] = list(group)
        svc_resp.append(tmp)
    return svc_resp

def get_services_by_category_new(data):
    svc_resp = []
    temp_category = dict()
    for iter in data:
        category_name = iter.get('category')
        # print(iter)
        # print(iter.get('category'))
        if(category_name in temp_category):
            temp_category[category_name].append(iter)
        else:
            temp_category[category_name] = list()
            temp_category[category_name].append(iter)

    for k,v in temp_category.items():
        tmp = {}
        tmp['name'] = k
        tmp['services'] = v
        svc_resp.append(tmp)
    # print(svc_resp)
    return svc_resp

def get_actions(action_id=None, service_id=None):
    ac_list = db_api.get_action(action_id=action_id, service_id=service_id)
    resp = []
    for item in ac_list:
        resp.append(item.to_dict())
    return resp

def delete_unused_services_from_db(service_list_arg):
    is_list = isinstance(service_list_arg, list)

    services_from_db = db_api.get_service()
    service_id_list_to_be_deleted_in_db = list()

    for service in services_from_db:
        match_found = False
        if is_list:
            for service_arg in service_list_arg:
                # print('{}:{}'.format(service.get('name'), service_arg.get('name')))
                if service.get('service_id') == service_arg.get('service_id'):
                    match_found = True
        else:
            if service.get('service_id') == service_arg.get('service_id'):
                match_found = True

        if not match_found:
            service_id_list_to_be_deleted_in_db.append(service.get('service_id'))

    for service_id_to_delete in service_id_list_to_be_deleted_in_db:
        db_api.delete_service(service_id=service_id_to_delete)

def delete_unused_actions_from_db(service_id, action_list_arg):

    actions_from_db = db_api.get_action(service_id=service_id)
    action_id_list_to_be_deleted_in_db = list()

    for action in actions_from_db:
        match_found = False
        for action_item in action_list_arg:
            #print('{}:{}'.format(action.get('name'), action_item.get('name')))
            if action.get('action_id') == action_item.get('action_id'):
                match_found = True

        if not match_found:
            action_id_list_to_be_deleted_in_db.append(action.get('action_id'))

    for action_id_to_delete in action_id_list_to_be_deleted_in_db:
        db_api.delete_action(action_id=action_id_to_delete)

def delete_unused_service_fields_from_db(service_id, action_id, service_fields_list_arg):

    service_fields_from_db = db_api.get_service_fields(service_id=service_id, action_id=action_id)
    service_field_id_list_to_be_deleted_in_db = list()

    for service_fields in service_fields_from_db:
        match_found = False
        for service_field_item in service_fields_list_arg:
            if service_fields.get('service_field_id') == service_field_item.get('service_field_id'):
                match_found = True

        if not match_found:
            service_field_id_list_to_be_deleted_in_db.append(service_fields.get('service_field_id'))

    for service_field_id_to_delete in service_field_id_list_to_be_deleted_in_db:
        db_api.delete_service_field(service_field_id=service_field_id_to_delete)


def delete_unused_output_fields_from_db(service_id, action_id, output_fields_args_list):

    output_fields_from_db = db_api.get_output_fields(service_id=service_id, action_id=action_id)
    output_field_id_list_to_be_deleted_in_db = list()

    for output_fields in output_fields_from_db:
        match_found = False
        for output_field_item in output_fields_args_list:
            if output_fields.get('output_field_id') == output_field_item.get('output_field_id'):
                match_found = True

        if not match_found:
            output_field_id_list_to_be_deleted_in_db.append(output_fields.get('output_field_id'))

    for output_field_id_to_delete in output_field_id_list_to_be_deleted_in_db:
        db_api.delete_output_field(output_field_id=output_field_id_to_delete)

def create_service_stack(args, delete_unused_services=False, delete_unused_actions=False, delete_unused_service_fields=False, delete_unused_output_fields=False):
    resp = []
    print ("Is it true? {} ".format(isinstance(args, list)))

    is_list = isinstance(args, list)

    if delete_unused_services:
        delete_unused_services_from_db(service_list_arg=args)


    if is_list:
        for item in args:
            resp = _create_svc_fls(item, delete_unused_actions=delete_unused_actions, delete_unused_service_fields=delete_unused_service_fields, delete_unused_output_fields=delete_unused_output_fields)
    else:
        resp = _create_svc_fls(args, delete_unused_actions=delete_unused_actions, delete_unused_service_fields=delete_unused_service_fields, delete_unused_output_fields=delete_unused_output_fields)
    return resp

def _create_svc_fls(args, delete_unused_actions=False, delete_unused_service_fields=False, delete_unused_output_fields=False):
    resp = collections.defaultdict
    svc_resp = create_service(args)
    if isinstance(svc_resp, list):
        service_id = svc_resp[0].get('service_id')
    else:
        service_id = svc_resp.get('service_id')

    if 'actions' in args.keys():
        action_list = args.get('actions')

        if delete_unused_actions:
            delete_unused_actions_from_db(service_id=service_id, action_list_arg=action_list)

        for action_item in action_list:
            ac_resp = create_action(service_id, action_item)
            # print('ac_resp:{}'.format(ac_resp))
            if isinstance(ac_resp, list):
                action_id = ac_resp[0].get('action_id')
            else:
                action_id = ac_resp.get('action_id')
            if 'service_fields' in action_item.keys():
                fl_list = action_item.get('service_fields')

                if delete_unused_service_fields:
                    delete_unused_service_fields_from_db(service_id=service_id, action_id=action_id, service_fields_list_arg=fl_list)

                for fl in fl_list:
                    field_resp = create_service_fields(service_id=service_id, action_id=action_id, args=fl)

            if 'output_fields' in action_item.keys():
                of_list = action_item.get('output_fields')

                if delete_unused_output_fields:
                    delete_unused_output_fields_from_db(service_id=service_id, action_id=action_id, output_fields_args_list=of_list)

                for of in of_list:
                    field_resp = create_output_fields(service_id=service_id, action_id=action_id, args=of)
    return resp

def get_service_fields(service_id, action_id):
    svf_list = db_api.get_service_fields(service_id=service_id, action_id=action_id)
    resp = []
    for svf in svf_list:
        svf = svf.to_dict()
        print ('control type {}'.format(svf['control_type']))
        svf['controlType'] = svf['control_type']
        required = svf.get('required')
        if required is not None:
            svf['required'] = bool(int(svf.get('required')))
        else:
            svf['required'] = False
        options = svf.get('options')
        print ('options {}'.format(options))
        if isinstance(options, list):
            op = Options()
            svf['options'] = op.format(options)
        print ('svf {}'.format(svf))
        resp.append(svf)
    print ('field resp {}'.format(resp))
    return resp

def get_output_fields(service_id, action_id):
    output_list = db_api.get_output_fields(service_id, action_id)
    # resp = []
    # for svf in svf_list:
    #     svf = svf.to_dict()
    #     print ('control type {}'.format(svf['control_type']))
    #     svf['controlType'] = svf['control_type']
    #     required = svf.get('required')
    #     if required is not None:
    #         svf['required'] = bool(int(svf.get('required')))
    #     else:
    #         svf['required'] = False
    #     options = svf.get('options')
    #     print ('options {}'.format(options))
    #     if isinstance(options, list):
    #         op = Options()
    #         svf['options'] = op.format(options)
    #     print ('svf {}'.format(svf))
    #     resp.append(svf)
    print ('field resp {}'.format(output_list))
    return output_list


# print(db_api.get_service(name='AgileCentral'))
#print(db_api.get_action(name='project_data'))

# print(db_api.create_output_fields({'output_field_id': 'test_op', 'output_field_name':'test_op_field_name', 'service_id':'sv1', 'action_id':'sv1_ac1'}))

# print(db_api.get_output_fields(service_id='sv1', action_id='sv1_ac1'))

# print(db_api.update_output_fields(output_field_id='test_op', data={'output_field_id': 'test_op', 'output_field_name':'test_op_field_nameeeee', 'service_id':'sv1', 'action_id':'sv1_ac1'}))

#db_api.update_action(action_id='sv31_ac1', data={'action_id':'sv31_ac1', 'name':'create ami', 'description':'create ami', 'service_id':'sv31'})