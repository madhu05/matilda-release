from matilda_release.db.sqlalchemy import api as IMPL
from matilda_release.util.status_helper import StatusDefinition as stts_dfn
from matilda_release.util.status_helper import ReleaseTypeCdDefinition as rls_type_cd
from matilda_release.util import status_helper as stts_hlpr

from werkzeug.exceptions import BadRequest

debug = False

def create_infra_release(args):
    #return r
    return IMPL.create_infra_release(args)

def create_release(args):
    return IMPL.create_release(args)

def create_project(args):
    return IMPL.create_project(args)

def create_application(args):
    return IMPL.create_application(args)

def create_app_release(args):
    return IMPL.create_app_release(args)

def create_vnf_release(args):
    return IMPL.create_vnf_release(args)

def add_link_to_release(args):
    return IMPL.add_link_to_release(args)


def add_link_items(args):
    return IMPL.add_link_items(args)


def add_env_to_release(args):
    return IMPL.add_env_to_release(args)


def add_release_conditions(args):
    return IMPL.add_release_conditions(args)


def add_release_execution_stats(args):
    return IMPL.add_release_execution_stats(args)

# def get_release_info(release_id=None, release_type=None, filters=None):
#     return IMPL.get_release_info(release_id, release_type, filters)


# def get_app_release_info(release_id, filters=None):
#     return IMPL.get_app_release_info(release_id, filters)
#
# def get_infra_release_info(release_id, filters=None):
#     return IMPL.get_infra_release_info(release_id, filters)

def get_release_links(release_id, link_id, filters=None):
    return IMPL.get_release_links(release_id, link_id, filters)

def get_release_link_items(release_link_id, link_item_id, filters=None):
    return IMPL.get_release_link_items(release_link_id, link_item_id, filters)

def create_release_link(rls_link):
    return IMPL.create_release_link(rls_link)

def create_release_link_item(rls_link):
    return IMPL.create_release_link_item(rls_link)

def get_release_conditions(release_id, release_env_id, filters=None):
    return IMPL.get_release_conditions(release_id, release_env_id, filters)

def get_release_type_cd(release_type_cd=None, release_type_description=None, filters=None):
    return IMPL.get_release_type_cd(release_type_cd=release_type_cd, release_type_description=release_type_description, filters=filters)

# def get_release_environments(release_id, filters=None):
#     return IMPL.get_release_environments(release_id, filters)

# def get_environment(release_id=None, env_id=None, filters=None):
#     envs = IMPL.get_environment(release_id=release_id, env_id=env_id)
#     response = list()
#     # print(type(tasks))
#     for env in envs:
#         temp_env = dict()
#         # print(task)
#         # print(type(task))
#         env_with_status_cd = env._asdict()
#         temp_env.update(env_with_status_cd.get('Environment', {}))
#         temp_env.update(env_with_status_cd.get('StatusCd', {}))
#         response.append(temp_env)
#     return response

def get_environment(release_id=None, env_id=None, name=None, filters=None, env_type_cd=None):
    return IMPL.get_environment(release_id=release_id, env_id=env_id, name=name, filters=filters, env_type_cd=env_type_cd)



# def get_release_environment_details(release_environment_id, filters=None):
#     return IMPL.get_release_environment_details(
#         release_environment_id, filters)


def get_release_environment_execution_stats(
        release_environment_id, filters=None):
    return IMPL.get_release_environment_execution_stats(
        release_environment_id, filters)

def save_req_data(args):
    IMPL.save_req_data(args)

def get_req_data(req_id):
    return IMPL.get_req_data(req_id)

def create_workflow(args):
    return IMPL.create_workflow(args)

# def get_workflow(env_id=None, wf_id=None):
#     workflows = IMPL.get_workflow(env_id=env_id, wf_id=wf_id)
#     response = list()
#     # print(type(tasks))
#     for workflow in workflows:
#         temp_workflow = dict()
#         # print(task)
#         # print(type(task))
#         workflow_with_status_cd = workflow._asdict()
#         temp_workflow.update(workflow_with_status_cd.get('Workflow', {}))
#         temp_workflow.update(workflow_with_status_cd.get('StatusCd',{}))
#         temp_workflow.update(workflow_with_status_cd.get('Frequency',{}))
#         response.append(temp_workflow)
#     return response

def get_workflow(env_id=None, wf_id=None):
    workflows = IMPL.get_workflow(env_id=env_id, wf_id=wf_id)
    response = list()
    for workflow in workflows:
        temp_workflow = workflow.to_dict()
        response.append(temp_workflow)

    return response

def create_stage(args):
    return IMPL.create_stage(args)

# def get_stage(wf_id=None, stage_id=None, filters=None):
#     stages = IMPL.get_stage(wf_id=wf_id, stage_id=stage_id)
#     response = list()
#     # print(type(tasks))
#     for stage in stages:
#         temp_stage = dict()
#         # print(task)
#         # print(type(task))
#         stage_with_status_cd = stage._asdict()
#         temp_stage.update(stage_with_status_cd.get('Stage', {}))
#         temp_stage.update(stage_with_status_cd.get('StatusCd', {}))
#         response.append(temp_stage)
#     return response

def get_stage(wf_id=None, stage_id=None, filters=None):
    stages = IMPL.get_stage(wf_id=wf_id, stage_id=stage_id)
    response = list()
    for stage in stages:
        temp_stage = stage.to_dict()
        response.append(temp_stage)

    return response

def create_task(args):
    args['wf_id']=get_stage(stage_id=args.get('stage_id'))[0].get('wf_id')
    return_value = IMPL.create_task(args)
    # print(return_value)
    # print(type(return_value))
    return_value['dag_task_name'] = return_value.get('name')+'_'+str(return_value.get('task_id'))
    # print(args)
    # print(return_value.get('task_id'))
    IMPL.update_task(task_id=return_value.get('task_id'), data=return_value)
    return get_task(task_id=return_value.get('task_id'))

# def get_task(task_id=None, stage_id=None):
#     tasks = IMPL.get_task(task_id=task_id, stage_id=stage_id)
#     response = list()
#     # print(type(tasks))
#     for task in tasks:
#         temp_task = dict()
#         # print(task)
#         # print(type(task))
#         task_with_status_cd = task._asdict()
#         temp_task.update(task_with_status_cd.get('Task', {}))
#         temp_task.update(task_with_status_cd.get('StatusCd', {}))
#         response.append(temp_task)
#
#     return response

def get_task(task_id=None, dag_task_name=None, stage_id=None, wf_id=None, name=None):
    tasks = IMPL.get_task(task_id=task_id, dag_task_name=dag_task_name, stage_id=stage_id, wf_id=wf_id, name=name)
    response = list()
    for task in tasks:
        temp_task = task.to_dict()
        response.append(temp_task)


    return response

def create_service(args):
    return IMPL.create_service(args)

def get_service(service_id=None, name=None, category=None, comments=None, filters=None):
    return IMPL.get_service(service_id=service_id,name=name, category=category,comments=comments, filters=filters)

def get_projects(project_id=None):
    return IMPL.get_projects(project_id)

def get_applications(application_id=None, project_id=None):
    return  IMPL.get_applications(application_id, project_id)

def create_action(args):
    return IMPL.create_action(args)

def get_action(action_id=None, service_id=None, name=None, description=None):
    return IMPL.get_action(action_id=action_id, service_id=service_id, name=name, description=description)

def get_platforms(platform_id, name, filters={}):
    return IMPL.get_platform(platform_id, name, filters)

def get_operating_systems(os_id, name, platform_id, filters={}):
    return IMPL.get_operating_system(os_id, name, platform_id, filters)

def get_vnf_nodes(vnf_node_id, name, filters={}):
    return IMPL.get_vnf_nodes(vnf_node_id, name, filters)

def get_vnf_sites(vnf_site_id, name, vnf_node_id, filters={}):
    return IMPL.get_vnf_sites(vnf_site_id, name, vnf_node_id, filters)

def create_service_fields(args):
    return IMPL.create_service_fields(args)

def get_service_fields(service_id=None, action_id=None, service_field_id=None, key=None, filters=None):
    return IMPL.get_service_fields(service_id=service_id, action_id=action_id, service_field_id=service_field_id, key=key, filters=filters)

def get_output_fields(service_id=None, action_id=None, output_field_id=None, filters=None):
    return IMPL.get_output_fields(service_id=service_id, action_id=action_id, output_field_id=output_field_id, filters=filters)

def update_environment(env_id, data):
    return IMPL.update_environment(env_id, data)

def update_stage(stage_id, data):
    return IMPL.update_stage(stage_id, data)

def update_workflow(wf_id, data):
    return IMPL.update_workflow(wf_id, data)

def update_task(task_id=None, dag_task_name=None, data=None):
    IMPL.update_task(task_id=task_id, dag_task_name=dag_task_name, data=data)
    return get_task(task_id=task_id)


def create_task(args):
    args['wf_id']=get_stage(stage_id=args.get('stage_id'))[0].get('wf_id')
    return_value = IMPL.create_task(args)
    # print(return_value)
    # print(type(return_value))
    return_value['dag_task_name'] = return_value.get('name')+'_'+str(return_value.get('task_id'))
    # print(args)
    # print(return_value.get('task_id'))
    IMPL.update_task(task_id=return_value.get('task_id'), data=return_value)
    return get_task(task_id=return_value.get('task_id'))



def create_template(args):
    return IMPL.create_template(args)

def get_template(template_id=None, template_name=None):
    return IMPL.get_template(template_id=template_id, template_name=template_name)

def get_frequency(frequency_cd=None):
    return IMPL.get_frequency(frequency_cd=frequency_cd)

def create_frequency(args):
    return IMPL.create_frequency(args)

def get_max_template_version(template_name=None):
    return IMPL.get_max_template_version(template_name=template_name)

def get_release_name_env_name(env_id):
    return IMPL.get_release_name_env_name(env_id=env_id)


def is_eligible_to_update_or_delete_task(stage_id=None, task_id=None):
    tasks = get_task(stage_id=stage_id, task_id=task_id)
    # print(type(stages))
    # print(stages)
    if type(tasks) is list:
        for task in tasks:
            # print(stage)
            status_cd = task.get('status_cd')
            if status_cd is not None and status_cd != 0 and status_cd != stts_dfn.defined.status_cd and status_cd != stts_dfn.configured.status_cd:
                raise BadRequest('Cannot Delete or update Task: {} since its not in Draft or Defined State'.format(task.get('name')))

    return True

def is_eligible_to_update_or_delete_stage(wf_id=None, stage_id=None):
    stages = get_stage(wf_id=wf_id, stage_id=stage_id)
    # print(type(stages))
    # print(stages)
    if type(stages) is list:
        for stage in stages:
            # print(stage)
            status_cd = stage.get('status_cd')
            if status_cd is not None and status_cd != 0 and status_cd != stts_dfn.defined.status_cd and status_cd != stts_dfn.configured.status_cd:
                raise BadRequest('Cannot Delete or update Stage: {} since its not in Draft or Defined State'.format(stage.get('name')))

    return True

def is_eligible_to_update_or_delete_workflow(env_id=None, wf_id=None):
    workflows = get_workflow(env_id=env_id, wf_id=wf_id)
    # print(type(stages))
    # print(stages)
    if type(workflows) is list:
        for workflow in workflows:
            # print(stage)
            status_cd = workflow.get('status_cd')
            if status_cd is not None and status_cd != 0 and status_cd != stts_dfn.defined.status_cd and status_cd != stts_dfn.configured.status_cd:
                raise BadRequest('Cannot Delete or update Workflow: {} since its not in Draft or Defined State'.format(workflow.get('name')))

    return True

def delete_task(stage_id=None, task_id=None):
    if stage_id is None and task_id is None:
        raise BadRequest('stage id or taks id is needed to delete tasks')
    if is_eligible_to_update_or_delete_task(stage_id=stage_id, task_id=task_id):
        return IMPL.delete_task(stage_id=stage_id, task_id=task_id)


def delete_stage(wf_id = None, stage_id=None):
    if wf_id is None and stage_id is None:
        raise BadRequest('workflow id or stage id is needed to delete stages')
    if is_eligible_to_update_or_delete_stage(wf_id=wf_id, stage_id=stage_id):
        stages = get_stage(wf_id=wf_id, stage_id=stage_id)
        for stage in stages:
            print('stage:{}'.format(stage))
            delete_task(stage_id=stage.get('stage_id'))
        return IMPL.delete_stage(stage_id=stage_id, wf_id=wf_id)


def delete_workflow(env_id=None, wf_id=None):
    if env_id is None and wf_id is None:
        raise BadRequest('environment id or workflow id is needed to delete workflow')
    if is_eligible_to_update_or_delete_workflow(env_id, wf_id):
        workflows = get_workflow(env_id, wf_id)
        for workflow in workflows:
            print(workflow)
            delete_stage(wf_id=workflow.get('wf_id'))
        return IMPL.delete_workflow(env_id=env_id, wf_id=wf_id)


def get_application_release_details(release_id=None, release_name=None, filters=None, extended=False):
    application_release_details = IMPL.get_application_release_Details(release_id=release_id, name=release_name,
                                                                       filters=filters)
    response = list()
    # print(type(tasks))
    for application_release_detail in application_release_details:
        temp_application_release_detail = dict()
        # print(task)
        # print(type(task))
        temp_application_release_detail_with_status_cd = application_release_detail._asdict()
        temp_application_release_detail.update(temp_application_release_detail_with_status_cd)
        temp_application_release_detail.update(temp_application_release_detail_with_status_cd.get('Release', {}))
        temp_application_release_detail.update(temp_application_release_detail_with_status_cd.get('AppReleaseInfo', {}))
        temp_application_release_detail.update(temp_application_release_detail_with_status_cd.get('StatusCd', {}))
        temp_application_release_detail.update(temp_application_release_detail_with_status_cd.get('ReleaseTypeCd', {}))
        temp_application_release_detail.update(temp_application_release_detail_with_status_cd.get('ReleasePlan', {}))
        response.append(temp_application_release_detail)

    return response

def derive_platform(PlatformObject):
    platform = dict()
    platform['name'] = PlatformObject.get('name')
    platform['platform_id'] = PlatformObject.get('platform_id')
    platform['status'] = PlatformObject.get('status')
    return  platform

def get_infrastructure_release_details(release_id=None, release_name=None, filters=None, extended=False):
    infrastructure_release_details = IMPL.get_infrastructure_release_Details(release_id=release_id, name=release_name,
                                                                       filters=filters)
    release_dict = dict()
    for infrastructure_release_detail in infrastructure_release_details:
        temp_infrastructure_release_detail = dict()
        temp_infrastructure_release_detail_with_status_cd = infrastructure_release_detail._asdict()
        release = temp_infrastructure_release_detail_with_status_cd.get('Release', {})
        platform = derive_platform(temp_infrastructure_release_detail_with_status_cd.get('Platform', {}))
        platform_name = platform.get('name')
        release_id = release.get('release_id')
        release_dict_to_update = release_dict.get(release_id)
        if release_dict_to_update is not None:
            release_platform = release_dict_to_update.get('platform')
            release_platform.append(platform)
            release_dict_to_update['platform'] = release_platform
            release_dict_to_update['platform_name']+=','+platform_name
            #release_dict[release_id] = release_dict_to_update
        else:
            temp_infrastructure_release_detail.update(release)
            temp_infrastructure_release_detail['platform'] = [platform]
            temp_infrastructure_release_detail['platform_name'] = platform_name
            temp_infrastructure_release_detail.update(temp_infrastructure_release_detail_with_status_cd.get('StatusCd', {}))
            temp_infrastructure_release_detail.update(temp_infrastructure_release_detail_with_status_cd.get('ReleaseTypeCd', {}))
            temp_infrastructure_release_detail.update(temp_infrastructure_release_detail_with_status_cd.get('ReleasePlan', {}))
            #test=temp_infrastructure_release_detail.get('status_cd')
            temp_infrastructure_release_detail['status_description']=stts_hlpr.get_status(temp_infrastructure_release_detail.get('status_cd')).status_description
            release_dict[release_id] = temp_infrastructure_release_detail

    return release_dict.values()


def get_vnf_release_details(release_id=None, release_name=None, filters=None, extended=False):
    vnf_release_details = IMPL.get_vnf_release_Details(release_id=release_id, name=release_name,
                                                                       filters=filters)
    response = list()
    # print(type(tasks))
    for vnf_release_detail in vnf_release_details:
        temp_vnf_release_detail = dict()
        # print(task)
        # print(type(task))
        temp_vnf_release_detail_with_status_cd = vnf_release_detail._asdict()
        temp_vnf_release_detail.update(temp_vnf_release_detail_with_status_cd)
        temp_vnf_release_detail.update(temp_vnf_release_detail_with_status_cd.get('Release', {}))
        temp_vnf_release_detail.update(temp_vnf_release_detail_with_status_cd.get('VnfRelease', {}))
        temp_vnf_release_detail.update(temp_vnf_release_detail_with_status_cd.get('StatusCd', {}))
        temp_vnf_release_detail.update(temp_vnf_release_detail_with_status_cd.get('ReleaseTypeCd', {}))
        temp_vnf_release_detail.update(temp_vnf_release_detail_with_status_cd.get('ReleasePlan', {}))
        response.append(temp_vnf_release_detail)

    return response



def get_base_release_details(release_id=None, release_name=None, filters=None, extended=False):
    release_details = IMPL.get_base_release_details(release_id=release_id, name=release_name,
                                                                       filters=filters)
    response = list()
    # print(type(tasks))
    for release_detail in release_details:
        temp_release_detail = dict()
        # print(task)
        # print(type(task))
        temp_release_detail_with_status_cd = release_detail._asdict()
        temp_release_detail.update(temp_release_detail_with_status_cd.get('Release', {}))
        temp_release_detail.update(temp_release_detail_with_status_cd.get('StatusCd', {}))
        temp_release_detail.update(temp_release_detail_with_status_cd.get('ReleaseTypeCd', {}))
        response.append(temp_release_detail)

    return response

def get_release(release_id=None, release_name=None, filters=None):
    releases = IMPL.get_release(release_id=release_id, name=release_name)
    response = list()

    for release in releases:
        temp_env = release.to_dict()
        response.append(temp_env)

    return response


def get_release_details(release_id=None, release_name=None, release_type_cd=None, filters=None, extended=False):
    if release_type_cd is not None:
        if release_type_cd == rls_type_cd.application.release_type_cd:
            return get_application_release_details(release_id=release_id, release_name=release_name)
        elif release_type_cd == rls_type_cd.infrastructure.release_type_cd:
            return get_infrastructure_release_details(release_id=release_id, release_name=release_name)
        elif release_type_cd == rls_type_cd.vnf.release_type_cd:
            return get_vnf_release_details(release_id=release_id, release_name=release_name)
    else:
        return get_base_release_details(release_id=release_id, release_name=release_name)


def update_release(release_id, data):
    return IMPL.update_release(release_id=release_id, data=data)


def get_env_type_cd(env_type_cd=None):
    return IMPL.get_env_type_cd(env_type_cd=env_type_cd)

def get_application_details(release_id=None,app_release_id=None,project_id=None,application_id=None):
    application = IMPL.get_application_details(release_id=release_id,app_release_id=app_release_id,
        project_id=project_id,application_id=application_id)
    response = list()
    for app in application:
        temp_app = app.to_dict()
        response.append(temp_app)
    return response

def create_env_type_cd(args):
    return IMPL.create_env_type_cd(args=args)


def delete_service(service_id=None):
    if service_id is None:
        raise BadRequest('service id is needed to delete service')
    services_from_db = get_service(service_id=service_id)
    for service in services_from_db:
        print(service)
        delete_action(service_id=service.get('service_id'))
    return IMPL.delete_service(service_id=service_id)


def delete_action(service_id = None, action_id=None):
    if service_id is None and action_id is None:
        raise BadRequest('service id or action id is needed to delete actions')
    actions_from_db = get_action(service_id=service_id, action_id=action_id)
    for action in actions_from_db:
        print(action)
        delete_service_field(action_id=action.get('action_id'))
        delete_output_field (action_id=action.get('action_id'))
    return IMPL.delete_action(service_id=service_id, action_id=action_id)


def delete_service_field(service_id=None, action_id=None, service_field_id=None):
    if service_id is None and action_id is None and service_field_id is None:
        raise BadRequest('service_id id or action_id or service_field_id is needed to delete service_fields')
    return IMPL.delete_service_field(service_id=service_id, action_id=action_id, service_field_id=service_field_id)

def update_action(action_id, data):
    IMPL.update_action(action_id=action_id, data=data)
    return get_action(action_id=action_id)

def update_service_fields(service_field_id, data):
    IMPL.update_service_fields(service_field_id=service_field_id, data=data)
    return get_service_fields(service_field_id=service_field_id)

def update_service(service_id, data):
    IMPL.update_service(service_id=service_id, data=data)
    return  get_service(service_id=service_id)

def create_output_fields(args):
    return IMPL.create_output_fields(args)

def update_output_fields(output_field_id, data):
    IMPL.update_output_fields(output_field_id=output_field_id, data=data)
    return get_output_fields(output_field_id=output_field_id)

def delete_output_field(service_id=None, action_id=None, output_field_id=None):
    if service_id is None and action_id is None and output_field_id is None:
        raise BadRequest('service_id id or action_id or output_field_id is needed to delete service_fields')
    return IMPL.delete_output_field(service_id=service_id, action_id=action_id, output_field_id=output_field_id)

def create_milestone(args):
    return IMPL.create_milestone(args)

def update_milestone(milestone_id=None, data=None):
    if milestone_id is None:
        raise BadRequest('milestone_id cannot be none for updating milestone')
    return IMPL.update_milestone(milestone_id, data)

def get_milestone(milestone_id=None, release_id=None, filters=None):
    return IMPL.get_milestone(milestone_id=milestone_id, release_id=release_id, filters=filters)

def create_milestone_status(args):
    return IMPL.create_milestone_status(args)

def update_milestone_status(milestone_status_cd, data):
    return IMPL.update_milestone_status(milestone_status_cd, data)

def get_milestone_status(milestone_status_cd=None, filters=None):
    return IMPL.get_milestone_status(milestone_status_cd=milestone_status_cd, filters=filters)

def create_milestone_type(args):
    return IMPL.create_milestone_type(args)

def update_milestone_type(milestone_type_cd, data):
    return IMPL.update_milestone_type(milestone_type_cd, data)

def get_milestone_type(milestone_type_cd=None, release_type_cd=None, filters=None):
    return IMPL.get_milestone_type(milestone_type_cd=milestone_type_cd, release_type_cd=release_type_cd, filters=filters)

def delete_milestone(release_id=None, milestone_id=None):
    if release_id is None and milestone_id is None:
        raise BadRequest('release id or milestone id needed to delete milestone')
    return IMPL.delete_milestone(release_id=release_id, milestone_id=milestone_id)

def delete_milestone_type(release_type_cd=None, milestone_type_cd=None):
    if release_type_cd is None and milestone_type_cd is None:
        raise BadRequest('release_type_cd or milestone_type_cd needed to delete milestone type cd')
    return IMPL.delete_milestone_type(release_type_cd=release_type_cd, milestone_type_cd=milestone_type_cd)

def create_release_plan(args):
    return IMPL.create_release_plan(args)

def update_release_plan(release_plan_id, args=None):
    if release_plan_id is None or release_plan_id==0:
        raise BadRequest('release_plan_id cannot be none for updating release_plan')
    return IMPL.update_release_plan(release_plan_id=release_plan_id, args=args)

def get_release_plan(release_plan_id=None, release_type_cd=None,filters=None):
    return IMPL.get_release_plan(release_plan_id=release_plan_id, release_type_cd=release_type_cd, filters=filters)

def delete_release_plan(release_plan_id):
    if release_plan_id is None or release_plan_id==0:
        raise BadRequest('release plan id needed for deletion')
    return IMPL.delete_release_plan(release_plan_id=release_plan_id)

def create_infra_category(args):
    return IMPL.create_infra_category(args)

def create_infra_subcomponent(args):
    return IMPL.create_infra_subcomponent(args)

def create_infra_component(args):
    return IMPL.create_infra_component(args)

def create_infra_metrics(args):
    return IMPL.create_infra_metrics(args)

def get_infra_category(category_id=None,category_name=None):
    categories = IMPL.get_infra_category(category_id=category_id,category_name=category_name)
    response = list()
    for cat in categories:
        temp_cat = cat.to_dict()
        response.append(temp_cat)
    return response
    #return IMPL.get_infra_category(args)
def get_infra_component(component_id=None,component_name=None):
    components = IMPL.get_infra_component(component_id=component_id,component_name=component_name)
    response = list()
    for comp in components:
        temp_comp = comp.to_dict()
        response.append(temp_comp)
    return response

def get_infra_subcomponent(subcomponent_id=None,subcomponent_name=None):
    subcomponents = IMPL.get_infra_subcomponent(subcomponent_id=subcomponent_id,subcomponent_name=subcomponent_name)
    response = list()
    for subcomp in subcomponents:
        temp_subcomp = subcomp.to_dict()
        response.append(temp_subcomp)
    return response


def get_infra_metrics(component_id=None,subcomponent_id=None,category_id=None,start_date=None,end_date=None):
    metrics = IMPL.get_infra_metrics(category_id=category_id,component_id=component_id,subcomponent_id=subcomponent_id,start_date=start_date,end_date=end_date)
    response = list()
    for subcomp in metrics:
        temp_subcomp = subcomp.to_dict()
        response.append(temp_subcomp)
    return response

def create_app_category(args):
    return IMPL.create_app_category(args)

def create_app_subcomponent(args):
    return IMPL.create_app_subcomponent(args)

def create_app_component(args):
    return IMPL.create_app_component(args)

def create_app_metrics(args):
    return IMPL.create_app_metrics(args)

def get_app_category(category_id=None,category_name=None):
    categories = IMPL.get_app_category(category_id=category_id,category_name=category_name)
    response = list()
    for cat in categories:
        temp_cat = cat.to_dict()
        response.append(temp_cat)
    return response

def get_app_component(component_id=None,component_name=None):
    components = IMPL.get_app_component(component_id=component_id,component_name=component_name)
    response = list()
    for comp in components:
        temp_comp = comp.to_dict()
        response.append(temp_comp)
    return response

def get_app_subcomponent(subcomponent_id=None,subcomponent_name=None):
    subcomponents = IMPL.get_app_subcomponent(subcomponent_id=subcomponent_id,subcomponent_name=subcomponent_name)
    response = list()
    for subcomp in subcomponents:
        temp_subcomp = subcomp.to_dict()
        response.append(temp_subcomp)
    return response


def get_app_metrics(component_id=None,subcomponent_id=None,category_id=None,start_date=None,end_date=None):
    metrics = IMPL.get_app_metrics(category_id=category_id,component_id=component_id,subcomponent_id=subcomponent_id,start_date=start_date,end_date=end_date)
    response = list()
    for subcomp in metrics:
        temp_subcomp = subcomp.to_dict()
        response.append(temp_subcomp)
    return response

def create_master_application(args):
    return IMPL.create_master_application(args=args)

def delete_master_application():
    return IMPL.delete_master_application()

def get_master_application(computer_system_name=None, platform=None, operating_system=None, filters=None):
    return IMPL.get_master_application(computer_system_name=computer_system_name, platform=platform, operating_system=operating_system, filters=filters)

def get_infra_release_impacted_application(release_id, computer_system_name=None, platform=None, operating_system=None, application_name = None, filters=None):
    return IMPL.get_infra_release_impacted_application(release_id=release_id, computer_system_name=computer_system_name, platform=platform, operating_system=operating_system, application_name=application_name, filters=filters)

def create_infra_release_impacted_application(args):
    return IMPL.create_infra_release_impacted_application(args=args)

def update_infra_release_impacted_application(impacted_application_id=None, data=None):
    if impacted_application_id is None:
        raise BadRequest('impacted_application_id cannot be none for updating milestone')
    return IMPL.update_infra_release_impacted_application(impacted_application_id, data)

def update_opt_out_for_application(release_id, application_name, opt_out):
    return IMPL.update_opt_out_for_application(release_id=release_id, application_name=application_name, opt_out=opt_out)