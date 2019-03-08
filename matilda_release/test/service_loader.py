import collections
import os
import configparser
import json

from matilda_release.api.v2.handler import service_handler

def load_service_data(delete_unused_services=False, delete_unused_actions=False, delete_unused_service_fields=False, delete_unused_output_fields=False):
    path = "/opt/matilda/matilda-plugin/matilda_plugin/plugins"
    # path = "C:\\Users\\Cnet\\Desktop\\plugin_cleanup_code\\matilda-plugin\\matilda_plugin\\plugins"
    services = []
    overall_common_output_field_derived_flag = False
    #i = 0
    for subdir, dirs, files in os.walk(path):
        print (subdir)
        overall_common_output_fields  = os.path.join(subdir, 'common_plugin_output.json')
        overall_common_output_fields_content = dict()
        if not overall_common_output_field_derived_flag:
            with open(overall_common_output_fields, "rb") as fin:
                content_op_fields = json.load(fin)
            overall_common_output_fields_content = content_op_fields.get('overall_common_output_fields', [])
            overall_common_output_field_derived_flag = True
        # this list is used to compare if there is duplicate service name in file just to prevent it from getting overwritten
        service_name_list = list()
        service_id_list = list()
        for dir in dirs:
            action_name_list = list()
            action_id_list = list()
            # print(i)
            # if i in (range(0,28)):
            #     print('do nothing:{}'.format(i))
            #     i+=1
            #     os.path.join(subdir, dir, 'plugin.info')
            # else:
            #     print('do it:{}'.format(i))
            #     i+=1
            #     os.path.join(subdir, dir, 'plugin.info')
            #     break
            if '__' not in dir:
                print(os.path.join(subdir, dir))
                info = os.path.join(subdir, dir, 'plugin.info')
                details = os.path.join(subdir, dir, 'plugin.json')
                config = configparser.ConfigParser()
                config.read(info)
                service = {}
                service['service_id'] = config.get('DEFAULT', 'Service_Id')
                service['name'] = config.get('DEFAULT', 'Name')
                if service.get('name') in service_name_list:
                    raise Exception("Duplicate Service Name, should be unique.{}".format(service.get('name')))
                else:
                    service_name_list.append(service.get('name'))
                if service.get('service_id') in service_name_list:
                    raise Exception("Duplicate service id in file. should be unique:{}".format(service.get('service_id')))
                else:
                    service_id_list.append(service.get('service_id'))
                service['category'] = config.get('DEFAULT', 'Group')
                service['comments'] = ";".join([config.get('DEFAULT', 'Version'), config.get('DEFAULT', 'Developer')])
                actions = []
                with open(details, "rb") as fin:
                    content = json.load(fin)
                ac_ip = content.get('actions')
                plugin_common_output_fields_content = content.get('plugin_common_output_fields', [])
                for ac in ac_ip:
                    service_field_id_list = list()
                    service_field_key_list = list()
                    output_field_id_list = list()
                    output_field_name_list = list()
                    print ('ac {}'.format(ac))
                    action_details = ac.get('action_details')
                    print('action_details:'.format(action_details))
                    ac_dic = {}
                    ac_dic['name'] = action_details.get('action_name')
                    if ac_dic['name'] in action_name_list:
                        raise Exception(
                            "Duplicate Action Name for Service, should be unique. service name:{}, action name: {}".format(
                                service.get('name'), ac_dic.get('name')))
                    else:
                        action_name_list.append(ac_dic.get('name'))
                    ac_dic['description'] = action_details.get('action_name').replace('_', ' ').title()
                    ac_dic['action_id'] = service['service_id']+'_'+action_details.get('action_id')
                    if ac_dic['action_id'] in action_id_list:
                        raise Exception(
                            "Duplicate Action id for Service, should be unique. service name:{}, action id: {}".format(
                                service.get('name'), ac_dic.get('action_id')))
                    else:
                        action_id_list.append(ac_dic.get('action_id'))
                    action_specific_common_output_fields_content = action_details.get('action_specific_output_fields', [])
                    output_field_list=[]
                    output_field_list.extend(overall_common_output_fields_content)
                    output_field_list.extend(plugin_common_output_fields_content)
                    output_field_list.extend(action_specific_common_output_fields_content)
                    final_output_field_list = list()
                    # below line of code will be un commented once we have output fields
                    for output_field_details in output_field_list:
                        output_field = dict()
                        print('output_field_details:{}'.format(output_field_details))
                        output_field['output_field_id'] = service['service_id']+'_'+action_details.get('action_id')+'_'+output_field_details.get('output_field_id')

                        if output_field.get('output_field_id') in output_field_id_list:
                            raise Exception(
                                "Duplicate Output field id for Action, should be unique. service name:{}, action name: {}, output field id: {} ".format(
                                    service.get('name'), ac_dic.get('action_name'), output_field.get('output_field_id')))
                        else:
                            output_field_name_list.append(output_field.get('output_field_id'))

                        output_field['output_field_name'] = output_field_details.get('output_field_name')

                        if output_field.get('output_field_name') in output_field_name_list:
                            raise Exception(
                                "Duplicate Output field name for Action, should be unique. service name:{}, action name: {}, output field name: {} ".format(
                                    service.get('name'), ac_dic.get('name'), output_field.get('output_field_name')))
                        else:
                            output_field_name_list.append(output_field.get('output_field_name'))

                        final_output_field_list.append(output_field)
                    ac_dic['output_fields'] = final_output_field_list
                    print(ac_dic.get('output_fields'))
                    service_fields = []
                    sf_ip = []
                    sf_ip.extend(action_details.get('ui_fields', []))
                    sf_ip.extend(content.get('commonFields', []))
                    for sf in sf_ip:
                        sf_op = {}
                        sf_op['service_field_id'] = service['service_id']+'_'+action_details.get('action_id')+'_'+sf.get('service_field_id')

                        if sf_op.get('service_field_id') in service_field_id_list:
                            raise Exception(
                                "Duplicate Service Field Id for Service, should be unique. service name:{}, action name: {}, service field Id: {} ".format(
                                    service.get('name'), ac_dic.get('name'), sf_op.get('service_field_id')))
                        else:
                            service_field_id_list.append(sf_op.get('service_field_id'))

                        sf_op['key'] = sf.get('key')

                        if sf_op.get('key') in service_field_key_list:
                            raise Exception(
                                "Duplicate Service Field Key for Action, should be unique. service name:{}, action name: {}, service field key: {} ".format(
                                    service.get('name'), ac_dic.get('action_name'), sf_op.get('key')))
                        else:
                            service_field_key_list.append(sf_op.get('key'))

                        sf_op['label'] = sf.get('label')
                        sf_op['controlType'] = sf.get('controlType')
                        sf_op['required'] = sf.get('required')
                        sf_op['order'] = sf.get('order')
                        sf_op['options'] = str(sf.get('options')).replace('"','\\"')
                        sf_op['field_type'] = 'input'
                        sf_op['placeholder'] = sf.get('placeholder')
                        sf_op['description'] = sf.get('label')
                        service_fields.append(sf_op)
                    ac_dic['service_fields'] = service_fields
                    actions.append(ac_dic)
                service['actions'] = actions
                services.append(service)
    print ('Service list {}'.format(services))
    if services is not None and len(services) > 0:
        service_handler.create_service_stack(args=services, delete_unused_services=delete_unused_services, delete_unused_actions=delete_unused_actions, delete_unused_service_fields=delete_unused_service_fields, delete_unused_output_fields=delete_unused_output_fields)
        return services

load_service_data(delete_unused_services=True, delete_unused_actions=True, delete_unused_service_fields=True, delete_unused_output_fields=True)
