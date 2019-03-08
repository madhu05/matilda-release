import logging
import random
from datetime import datetime

from six import iteritems
from werkzeug.exceptions import BadRequest

from matilda_release.api.v2.handler import environment_handler as env
from matilda_release.api.v2.handler import release_plan_handler
from matilda_release.api.v2.model.model import release
from matilda_release.db import api as db_api
from matilda_release.db.sqlalchemy.models import Release, AppReleaseInfo, InfraRelease, VnfRelease
from matilda_release.mock_data.mock_data_helper import  MockDataHelper
from matilda_release.util import status_helper as stts_helper
from matilda_release.util.status_helper import ReleaseTypeCdDefinition as rls_type_cd
from matilda_release.util.status_helper import StatusDefinition as stts_dfn

log = logging.getLogger(__name__)
debug = False
# initializing mock data helper object.
mdh = MockDataHelper()

def get_release(release_id=None, release_type_cd=rls_type_cd.application.release_type_cd, filters=None, extended=False):
    from matilda_release.api.v2.handler import environment_handler
    resp = []
    rls_info = db_api.get_release_details(release_id=release_id,release_type_cd=release_type_cd,filters=filters)
    log.debug('Release ID {}, Release Info {}'.format(release_id, rls_info))
    print ('release db data {}'.format(rls_info))
    #result = _map_release_resp(rls_info)
    #print ('RESULT AFTER MAP {}'.format(result))
    for rls in rls_info:
        release_id = rls.get('release_id')
        for key in release:
            if key not in rls.keys():
                rls[key] = None
        if extended:
            env_list = environment_handler.get_environments(release_id, True)
            print ('env list for rls : {}'.format(env_list))
            rls['environments'] = env_list
        resp.append(rls)
    return resp

# def _map_release_resp(rls_list):
#     result = []
#     for rls in rls_list:
#         resp = {}
#         resp.update(rls._asdict())
#         resp.update(rls._asdict().get('Release', {}))
#         resp.update(rls._asdict().get('AppReleaseInfo', {}))
#         #resp.update(rls._asdict().get('Project', {}))
#         #resp.update(rls._asdict().get('Applicatiion', {}))
#         result.append(resp)
#     return result

def get_project(project_id):
    from matilda_release.api.v2.handler import project_handler
    resp = project_handler.get_projects(project_id)
    if len(resp) > 0:
        return resp[0]
    return None


def get_application(application_id):
    from matilda_release.api.v2.handler import application_handler
    resp = application_handler.get_applications(application_id)
    if len(resp) > 0:
        return resp[0]
    return None

def get_release_count():
    resp=[]
    type_cd = db_api.get_release_type_cd()
    out = db_api.get_release()
    response_cd = list()

    for cd in type_cd:
        temp_env = cd.to_dict()
        response_cd.append(temp_env)
    for typ in response_cd:
        temp = {}
        temp['release_type_cd']=typ.get('release_type_cd')
        temp['count']=sum(1 for item in out if item['release_type_cd']==typ.get('release_type_cd'))
        resp.append(temp)
        print(resp)
    print(resp)
    '''for typ in cd:
        resp = db_api.get_release(release_type_cd=typ.get('release_type_cd'))'''
    return resp

def get_status_count(release_type_cd=None):
    resp = {}
    rsp={}
    out = db_api.get_release()
    resp[stts_dfn.defined.status_description]=sum(1 for item in out if item['release_type_cd']==release_type_cd and item['status_cd']==stts_dfn.defined.status_cd)
    resp[stts_dfn.configured.status_description]=sum(1 for item in out if item['release_type_cd']==release_type_cd and item['status_cd']==stts_dfn.configured.status_cd)
    resp[stts_dfn.inProgress.status_description]=sum(1 for item in out if item['release_type_cd']==release_type_cd and item['status_cd']==stts_dfn.inProgress.status_cd)
    resp[stts_dfn.success.status_description]=sum(1 for item in out if item['release_type_cd']==release_type_cd and item['status_cd']==stts_dfn.success.status_cd)
    resp[stts_dfn.failed.status_description]=sum(1 for item in out if item['release_type_cd']==release_type_cd and item['status_cd']==stts_dfn.failed.status_cd)
    rsp['status']=resp
    return rsp

def get_release_type():
    return db_api.get_release_type_cd()

def clone_release(release_id, name, date):
    from matilda_release.api.v2.handler import environment_handler
    args = {}
    release_to_clone = db_api.get_release_details(release_id=release_id,release_type_cd=None)
    if release_to_clone is not None:
        release_list = get_release(release_id=release_id, release_type_cd=release_to_clone[0]['release_type_cd'], filters=None, extended=False)
        print("release_to_clone ****",release_to_clone,release_to_clone[0]['release_id'])
        args['release_id'] = release_to_clone[0]['release_id']
        args['name'] = name
        args['version'] = release_to_clone[0]['version']
        args['release_type_cd'] = release_to_clone[0]['release_type_cd']
        args['release_dt'] = date
        args['status_cd'] = release_to_clone[0]['status_cd']
        args['description'] = release_to_clone[0]['description']

        if args['release_type_cd'] == rls_type_cd.infrastructure.release_type_cd and release_list is not None:
            args['os_id'] = release_list[0]['InfraRelease']['os_id']
            args['platform_id'] = release_list[0]['InfraRelease']['platform_id']
        elif args['release_type_cd'] == rls_type_cd.application.release_type_cd and release_list is not None:
            args['application_id'] = release_list[0]['AppReleaseInfo']['application_id']
            args['project_id'] = release_list[0]['AppReleaseInfo']['project_id']
        resp_args = create_release(args)
        env_list = db_api.get_environment(release_id=release_id)
        for env in env_list:
            '''env['start_dt'] = datetime.strftime(env['start_dt'], '%Y-%m-%dT%H:%M:%S')'''
            #print("release id !!!!!!!",args['release_id'],release_id)
            #print('env%%%%%%', env,type(env['start_dt']))
            resp_env = environment_handler.clone_environment(release_id, env['env_id'], env['name'], env['type'])
            #print('resp_args &&&&&',resp_args,resp_env)
            if resp_env is not None:
                resp_args.update(resp_env)
        
    #print("env_list",env_list)
    #print("args ****",args)
    #print("length ******",len(env_list),env_list[0]["env_id"],env_list[0]["name"],env_list[0]["type"],release_to_clone[0]['release_type'])
    #print('resp_args $$$$',resp_args)
    return resp_args

def create_release(args):
    release_type_cd = args['release_type_cd']
    resp_args = args
    print("data is", db_api.get_release_plan(release_plan_id=args.get('release_plan_id')))
    release_plan_from_db = db_api.get_release_plan(release_plan_id=args.get('release_plan_id'))[0]._asdict().get('ReleasePlan')

    if release_plan_from_db.get('release_type_cd') != release_type_cd:
        raise BadRequest('release type code of release plan and release are not matching')
    resp_args['release_plan_name'] = release_plan_from_db.get('release_plan_name')
    release = create_master_release(args)
    resp_args['release_id'] = release.get('release_id')
    release_plan_from_db = db_api.get_release_plan(release_plan_id=release.get('release_plan_id'))[0]._asdict()
    resp_args['release_plan_name'] = release_plan_from_db.get('release_plan_name')
    log.debug('Creating {} release'.format(release_type_cd))
    resp = {}
    if release_type_cd == rls_type_cd.infrastructure.release_type_cd:
        platform = args.get('platform')
        if type(platform) is not list:
            platform = [platform]
        platform_name = ''
        for iter_platform in platform:
            if platform_name !='':
                platform_name +=','
            platform_name+=iter_platform.get('name')
            infra_vo = InfraRelease()
            infra_vo.platform_id = iter_platform.get('platform_id')
            infra_vo.release_id = release.get('release_id')
            resp = db_api.create_infra_release(infra_vo)
            resp['platform_name']=platform_name


    elif release_type_cd == rls_type_cd.application.release_type_cd:
        app_vo = AppReleaseInfo()
        app_vo.application_id = args.get('application_id')
        app_vo.project_id = args.get('project_id')
        app_vo.release_id = release.get('release_id')
        resp = db_api.create_app_release(app_vo)
    elif release_type_cd == rls_type_cd.vnf.release_type_cd:
        app_vo = VnfRelease()
        app_vo.vnf_site_id = args.get('vnf_site_id')
        app_vo.vnf_node_id = args.get('vnf_node_id')
        app_vo.release_id = release.get('release_id')
        resp = db_api.create_vnf_release(app_vo)

    for k, v in iteritems(resp):
        resp_args[k] = v

    if 'selected_additional_releaseplans' in args.keys():
        pass
    return resp_args


def create_master_release(args):
    rls_info = Release()
    rls_info.description = args.get('description')
    rls_info.name = args.get('name')
    rls_info.release_plan_id = args.get('release_plan_id')
    rls_info.status_cd = stts_dfn.defined.status_cd
    rls_info.release_type_cd = args.get('release_type_cd')
    rls_info.description = args.get('description')
    rls_info.create_dt = datetime.now()
    rls_info.release_dt = datetime.strptime(args.get('release_dt'), '%Y-%m-%dT%H:%M:%S.%fZ')
    resp = db_api.create_release(rls_info)
    return resp

#print(create_release(args=release_payload()))


def get_platform(platform_id=None, name=None):
    resp = []
    platforms = db_api.get_platforms(platform_id, name)
    for platform in platforms:
        os_list = get_operating_system(platform_id=platform.get('platform_id'))
        platform['operating_systems'] = os_list
        resp.append(platform)
    return resp


def get_operating_system(os_id=None, name=None, platform_id=None):
    operating_systems = db_api.get_operating_systems(os_id, name, platform_id)
    return operating_systems

def get_vnf_nodes(vnf_node_id=None, name=None):
    resp = []
    vnf_nodes = db_api.get_vnf_nodes(vnf_node_id, name)
    for vnf_node in vnf_nodes:
        vnf_sites = get_vnf_sites(vnf_node_id=None)
        vnf_node['vnf_sites'] = vnf_sites
        resp.append(vnf_node)
    return resp

def get_vnf_sites(vnf_site_id=None, name=None, vnf_node_id=None):
    vnf_sites = db_api.get_vnf_sites(vnf_site_id, name, vnf_node_id)
    return vnf_sites


def get_impacted_systems_for_platform_os(platform, os):
        servers = mdh.get_servers()
        impacted_servers = dict()

        for server in servers:
            if server.get('platform') == platform and server.get('os') == os:
                env_type_temp = server.get('env_type')
                if impacted_servers.get(env_type_temp) == None:
                    impacted_servers[env_type_temp] = list()

                #print('match:'+ str(server))
                server['applications'] = get_impacted_applications_for_server(server.get('ip'))
                impacted_servers[env_type_temp].append(server)
            # else:
            #     print('match_failed:' +str(server))
        # print('available_environments {}'.format(impacted_servers))
        return impacted_servers


def get_infra_impacted_systems_for_platform(platform):
    return db_api.get_master_application(platform=platform)


def get_impacted_systems_for_node_site(vnf_node,vnf_site):
    servers = mdh.get_vnfs()
    impacted_servers = dict()

    for server in servers:
        if server.get('vnf_node') == vnf_node and server.get('vnf_site') == vnf_site:
            env_type_temp = server.get('env_type')
            if impacted_servers.get(env_type_temp) == None:
                impacted_servers[env_type_temp] = list()

            # print('match:'+ str(server))
            server['applications'] = get_impacted_applications_for_server(server.get('ip'))
            impacted_servers[env_type_temp].append(server)
        # else:
        #     print('match_failed:' +str(server))
    # print('available_environments {}'.format(impacted_servers))
    return impacted_servers

def get_impacted_applications_for_server(ip):
    applications = mdh.get_applications()
    impacted_applications = list()
    for application in applications:
        if application.get('server_ip') == ip:
            #print('match app:' + str(application))
            impacted_applications.append(application)
        # else:
        #     print('no matching app:' + str(application))
    #print(impacted_applications)
    return impacted_applications


def get_infra_release_impacted_application(release_id, computer_system_name=None, platform=None, operating_system=None, create_environment=False, filters=None):
    data_from_db = db_api.get_infra_release_impacted_application(release_id, computer_system_name=computer_system_name, platform=platform, operating_system=operating_system, filters=filters)
    if data_from_db is not None and type(data_from_db) is list and len(
            data_from_db) > 0:
        response = [] 
        for item in data_from_db:
            response.append(item.to_dict())
        return response
    else:
        release_details = get_release(release_id=release_id, release_type_cd=rls_type_cd.infrastructure.release_type_cd)
        infra_impacted_systems_list = list()
        environment_name_list = list()
        if len(release_details) > 0:
            rls = release_details[0]
            release_plan = release_plan_handler.get_release_plan(release_plan_id=rls.get('release_plan_id'))[0]
            test_folder_name=release_plan.get('release_plan_name')+'_'+str(release_plan.get('release_dt').strftime("%Y-%m-%d"))

            if rls.get('release_type_cd') == rls_type_cd.infrastructure.release_type_cd:

                impacted_systems = list()
                for platform_iter in rls.get('platform'):
                    platform = get_platform(platform_iter.get('platform_id'))[0].get('name')
                    impacted_systems.extend(get_infra_impacted_systems_for_platform(platform=platform))

                for impacted_system in impacted_systems:
                    impacted_system['release_id'] = release_id
                    impacted_system['test_folder_name'] = test_folder_name

                    infra_impacted_systems_list.append(
                        db_api.create_infra_release_impacted_application(args=impacted_system))

                    env_name = impacted_system.get('platform') + '_' + impacted_system.get('environment')
                    if env_name not in environment_name_list:
                        environment_name_list.append(env_name)

                if create_environment and len(environment_name_list) > 0:
                    for env in environment_name_list:
                        env_type_cd = stts_helper.get_env_type(env_type_description=env.rsplit('_')[1]).env_type_cd
                        create_env(env_name=env, env_type_cd=env_type_cd, release_id=release_id)

        return infra_impacted_systems_list

def get_impacted_systems_vnf(release_id):
    release_details = get_release(release_id=release_id, release_type_cd=rls_type_cd.vnf.release_type_cd)
    if len(release_details) > 0:
        rls = release_details[0]
        if rls.get('Release').get('release_type_cd') == rls_type_cd.vnf.release_type_cd:
          vnf_node = get_vnf_nodes(rls.get('VnfRelease').get('vnf_node_id'))[0].get('name')
          vnf_site = get_vnf_sites(rls.get('VnfRelease').get('vnf_site_id'))[0].get('name')
          print(vnf_node, vnf_site)

          impacted_systems = get_impacted_systems_for_node_site(vnf_node,vnf_site)
          final_impacted_systems_list = list()

          for k,v in impacted_systems.items():
                  env_type_cd = stts_helper.get_env_type(env_type_description=k).env_type_cd
                  env = create_env(env_name=k, env_type_cd=env_type_cd, release_id=release_id)
                  env['impactedSystems'] = v
                  final_impacted_systems_list.append(env)

        #print('final {}'.format(final_impacted_systems_list))
        return final_impacted_systems_list



def create_env(env_name, env_type_cd, release_id):
    from matilda_release.api.v2.handler import environment_handler
    environments = environment_handler.get_environment(release_id=release_id, env_name=env_name)
    # print('env {}'.format(environments))
    is_create_environment = False

    env_default = {
        "env_id": 0,
        "name": "string",
        "type": "string",
        "create_dt": "",
        "start_dt": "",
        "end_dt": "",
        "status": "string",
        "release_id": 0,
        "release": "string"
    }
    if environments != None and len(environments)!=0:
        match_found = False
        for  environment in environments:
            if environment.get('name') == env_name:
                match_found = True
                log.debug('{}:environment already created'.format(env_type_cd))
                return environment

        if not match_found:
            is_create_environment = True
    else:
        is_create_environment = True

    if is_create_environment:
        env_temp = env_default.copy()
        env_temp['name'] = env_name
        env_temp['env_type_cd'] = env_type_cd
        env_temp['status'] = 'Defined'
        env_temp['release_id'] = release_id
        env_temp['create_dt'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        env_temp['start_dt'] = None
        #env_temp['start_dt'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return environment_handler.create_environment(release_id, env_temp)

def get_release_name_list():
    releases = db_api.get_release_details()
    final_list = list()
    resp = dict()
    print('releases{}'.format(releases))
    for rls in releases:
        final_list.append(rls.get('name'))
    print('final_list{}'.format(final_list))
    resp['release_names'] = final_list
    return resp

def get_release_metrics(release_id=None):
    jsn={}
    rel_data=db_api.get_release(release_id=release_id)
    rel_type=rel_data[0].get('release_type_cd')
    if (rel_type != rls_type_cd.infrastructure.release_type_cd) and (rel_type != rls_type_cd.application.release_type_cd):
        return jsn
    jsn['Release status']=rel_data[0].get('status_cd')
    
    release_plan_from_db = db_api.get_release_plan(release_plan_id=rel_data[0].get('release_plan_id'))[0]._asdict().get('ReleasePlan')
    #print(release_plan_from_db[0])
    jsn['owner']=release_plan_from_db.get('release_owner')
    if release_plan_from_db.get('release_dt') is not None:
        jsn['start_date']=datetime.strftime(release_plan_from_db.get('release_dt'),'%m/%d/%Y')
    platform_array=[]
    if rel_type==rls_type_cd.infrastructure.release_type_cd:
        jsn['test_status'] ={}
        out_app=get_infra_release_impacted_application(release_id)
        resp=[]
        for app in out_app:
            #temp_subcomp = app.to_dict()
            resp.append(app)
        s = set()
        for dic in resp:
            s.add(dic['application_name'])
        jsn['app_count']=len(s)
        platform=db_api.get_release_details(release_id=release_id,release_type_cd=rel_type)
        for plat in platform:
            platform_array.append(plat.get('platform_name'))

        jsn['impacted_platforms']=platform_array
        test=mdh.get_test_status()
        status=[]
        entity=test['entities']
        for ent in entity:
            field = ent['Fields']
            for array in field:
                if array['Name']=='exec-status':
                    status.append(array['values'])
        jsn['test_status']['No Run']=len(status) +random.randint(1,101)
        jsn['test_status']['Failed'] =0
        jsn['test_status']['Passed'] = 0
        jsn['test_status']['Not Completed'] = 0
        '''jsn['test_status']['Passed']=sum(1 for item in status if item[0]['value'] == 'Passed')
        jsn['test_status']['Failed']=sum(1 for item in status if item[0]['value'] == 'Failed')
        jsn['test_status']['No Run']=sum(1 for item in status if item[0]['value'] == 'No Run')
        jsn['test_status']['Not Completed']=sum(1 for item in status if item[0]['value'] == 'Not Completed')'''
    elif rel_type==rls_type_cd.application.release_type_cd:
        out_app=db_api.get_application_details(release_id=release_id)
        s = set()
        for dic in out_app:
            s.add(dic['application_id'])
        jsn['app_count']=len(s)
        jsn['application_type']=None
        jsn['test_status']=None
    out_env=env.get_environments(release_id=release_id, extended=True)
    print(out_env)
    for en in out_env:
        wf=en.get('workflows')
        if wf:
            for out_wf in wf:
                wf_id=out_wf.get('wf_id')
                tsk=db_api.get_task(wf_id=wf_id)
                count_tsk = sum(1 for item in tsk if item['status_cd'] == stts_dfn.success.status_cd)
                jsn['Task_completed']=count_tsk
                jsn['Total_Task']=len(tsk)
        else:
            jsn['Total_Task']=0

    return jsn
