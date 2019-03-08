import logging
import uuid

from matilda_release.db.sqlalchemy.models import MasterApplications, InfraReleaseImpactedApplications
from matilda_release.api.v2.handler import release_handler

from matilda_release.db import api as db_api
from matilda_release.client import rpcapi

log = logging.getLogger(__name__)
debug = False

def get_master_application(computer_system_name=None, platform=None, operating_system=None, filters=None):
    return db_api.get_master_application(computer_system_name=computer_system_name, platform=platform, operating_system=operating_system, filters=filters)

def create_master_application(args=None):

    ms_info = MasterApplications()
    ms_info.computer_system_name = args.get('computer_system_name')
    ms_info.application_name = args.get('application_name')
    ms_info.environment = args.get('environment')
    ms_info.platform = args.get('platform')
    ms_info.platform_from_excel = args.get('platform_from_excel')
    ms_info.operating_system = args.get('operating_system')
    ms_info.test_type_prod = args.get('test_type_prod')
    ms_info.test_type_non_prod = args.get('test_type_non_prod')
    ms_info.app_owner_name = args.get('app_owner_name')
    ms_info.tester_name = args.get('tester_name')
    ms_info.test_set_or_folder = args.get('test_set_or_folder')

    resp_master_system = db_api.create_master_application(args=ms_info)
    return resp_master_system

def delete_master_applications():
    return db_api.delete_master_application()

def get_infra_release_impacted_application(release_id, computer_system_name=None, platform=None, operating_system=None, create_environment=False, filters=None):
    return release_handler.get_infra_release_impacted_application(release_id=release_id, computer_system_name=computer_system_name, platform=platform, operating_system=operating_system, create_environment=create_environment, filters=filters)

def create_infra_release_impacted_application(release_id, args=None):

    ms_info = InfraReleaseImpactedApplications()
    ms_info.release_id = release_id
    ms_info.computer_system_name = args.get('computer_system_name')
    ms_info.application_name = args.get('application_name')
    ms_info.environment = args.get('environment')
    ms_info.platform = args.get('platform')
    ms_info.platform_from_excel = args.get('platform_from_excel')
    ms_info.operating_system = args.get('operating_system')
    ms_info.test_type_prod = args.get('test_type_prod')
    ms_info.test_type_non_prod = args.get('test_type_non_prod')
    ms_info.app_owner_name = args.get('app_owner_name')
    ms_info.tester_name = args.get('tester_name')
    ms_info.test_folder_name = args.get('test_folder_name')
    ms_info.test_set_or_folder = args.get('test_set_or_folder')
    ms_info.opt_out = args.get('opt_out')

    resp_master_system = db_api.create_infra_release_impacted_application(args=ms_info)
    return resp_master_system


def update_infra_release_impacted_application(release_id=None, impacted_application_id=None, args=None):
    ms_info = InfraReleaseImpactedApplications()
    ms_info.impacted_application_id = impacted_application_id
    ms_info.release_id = release_id
    ms_info.computer_system_name = args.get('computer_system_name')
    ms_info.application_name = args.get('application_name')
    ms_info.environment = args.get('environment')
    ms_info.platform = args.get('platform')
    ms_info.platform_from_excel = args.get('platform_from_excel')
    ms_info.operating_system = args.get('operating_system')
    ms_info.test_type_prod = args.get('test_type_prod')
    ms_info.test_type_non_prod = args.get('test_type_non_prod')
    ms_info.app_owner_name = args.get('app_owner_name')
    ms_info.tester_name = args.get('tester_name')
    ms_info.test_folder_name = args.get('test_folder_name')
    ms_info.test_set_or_folder = args.get('test_set_or_folder')
    ms_info.opt_out = args.get('opt_out')
    db_api.update_infra_release_impacted_application(impacted_application_id=impacted_application_id, data=args)
    return ms_info

def create_test_suites(release_id):
    release_data = release_handler.get_release(release_id=release_id)
    cntx = {'req_id': str(uuid.uuid4())}
    payload = {
        'release_id': release_id,
        'release_name': release_data.get('name') or str(release_id)
    }
    rpc = rpcapi.RpcAPI()
    rpc.invoke_notifier(ctxt=cntx, payload=payload,
                        action='create_test_suites', component='infra')
    return cntx

def update_opt_out_for_application(release_id, application_name, opt_out):
    return db_api.update_opt_out_for_application(release_id=release_id, application_name=application_name, opt_out=opt_out)