import datetime
import sys
import threading

from oslo_config import cfg
from oslo_db import options as oslo_db_options
from oslo_db.sqlalchemy import session as db_session
from oslo_db.sqlalchemy import utils as sqlalchemyutils
from oslo_log import log as logging
from six import iteritems
from sqlalchemy import func

from matilda_release.db.sqlalchemy import models
from matilda_release.util.status_helper import ReleaseTypeCdDefinition as rls_type_cd

data = str(datetime.datetime.now())
chop = len(data.split()[-1]) - 8
now = datetime.datetime.now()

api_db_opts = [
    cfg.StrOpt('db_connection',
               secret=True,
               #default='mysql://matilda:M@3ilDa@35.162.247.245/release_management'
               #default='mysql://root:root@localhost/release_management'
                default="sqlite:///release_management.db"
                )
]

CONF = cfg.CONF

opt_group = cfg.OptGroup(name='database')
CONF.register_group(opt_group)
CONF.register_opts(oslo_db_options.database_opts, opt_group)
CONF.register_opts(api_db_opts, opt_group)

LOG = logging.getLogger(__name__)

_ENGINE_FACADE = {'matilda_release': None}
_CSS_FACADE = 'matilda_release'
_LOCK = threading.Lock()


def _create_facade(conf_group):
    return db_session.EngineFacade(
        sql_connection=conf_group.db_connection,
        autocommit=True,
        expire_on_commit=False,
        mysql_sql_mode=conf_group.mysql_sql_mode,
        idle_timeout=conf_group.idle_timeout,
        connection_debug=conf_group.connection_debug,
        max_pool_size=conf_group.max_pool_size,
        max_overflow=conf_group.max_overflow,
        pool_timeout=conf_group.pool_timeout,
        sqlite_synchronous=conf_group.sqlite_synchronous,
        connection_trace=conf_group.connection_trace,
        max_retries=conf_group.max_retries,
        retry_interval=conf_group.retry_interval)


def _create_facade_lazily(facade, conf_group):
    global _LOCK, _ENGINE_FACADE
    if _ENGINE_FACADE[facade] is None:
        with _LOCK:
            if _ENGINE_FACADE[facade] is None:
                _ENGINE_FACADE[facade] = _create_facade(conf_group)
    return _ENGINE_FACADE[facade]


def get_engine(use_slave=False):
    conf_group = CONF.database
    facade = _create_facade_lazily(_CSS_FACADE, conf_group)
    return facade.get_engine(use_slave=use_slave)


def get_session(use_slave=False, **kwargs):
    conf_group = CONF.database
    facade = _create_facade_lazily(_CSS_FACADE, conf_group)
    return facade.get_session(use_slave=use_slave, **kwargs)


def get_backend():
    """The backend is this module itself."""
    return sys.modules[__name__]


def model_query(model,
                args=None,
                session=None):
    if session is None:
        session = get_session()

    query = sqlalchemyutils.model_query(model, session, args)
    return query


def create_release(args):
    session = get_session()
    with session.begin():
        req_data = models.Release()
        req_data.update(args)
        req_data.save(session=session)
    return req_data.to_dict()


def create_project(args):
    session = get_session()
    with session.begin():
        req_data = models.Project()
        req_data.update(args)
        req_data.save(session=session)
    return req_data.to_dict()


def create_application(args):
    session = get_session()
    with session.begin():
        req_data = models.Application()
        req_data.update(args)
        req_data.save(session=session)
    return req_data.to_dict()


def create_app_release(args):
    session = get_session()
    with session.begin():
        req_data = models.AppReleaseInfo()
        req_data.update(args)
        req_data.save(session=session)
    return req_data.to_dict()


def create_infra_release(args):
    print('sqlalchemy args', args)
    session = get_session()
    with session.begin():
        req_data =       models.InfraRelease()
        req_data.update(args)
        req_data.save(session=session)
    return req_data.to_dict()


def create_vnf_release(args):
    print('sqlalchemy args', args)
    session = get_session()
    with session.begin():
        req_data = models.VnfRelease()
        req_data.update(args)
        req_data.save(session=session)
    return req_data.to_dict()


def add_link_to_release(args):
    session = get_session()
    with session.begin():
        req_data = models.ReleaseLink()
        req_data.update(args)
        req_data.save(session=session)
    return req_data.to_dict()


def add_link_items(args):
    session = get_session()
    with session.begin():
        req_data = models.ReleaseLinkItem()
        req_data.update(args)
        req_data.save(session=session)
    return req_data.to_dict()


def add_env_to_release(args):
    session = get_session()
    with session.begin():
        req_data = models.Environment()
        req_data.update(args)
        req_data.save(session=session)
    return req_data.to_dict()


def add_release_conditions(args):
    session = get_session()
    with session.begin():
        req_data = models.ReleaseCondition()
        req_data.update(args)
        req_data.save(session=session)
    return req_data.to_dict()


def add_release_execution_stats(args):
    session = get_session()
    with session.begin():
        req_data = models.ReleaseExecutionStatus()
        req_data.update(data)
        req_data.save(session=session)
    return req_data.to_dict()


def get_release(release_id=None, name=None, filters=None):
    session = get_session()
    with session.begin():
        print('Filters %r' % filters)
        print('name %r' % release_id, models.Release)
        query = session.query(models.Release)
        if release_id is not None:
            query = query.filter(models.Release.release_id == release_id)
        if name is not None:
            query = query.filter(models.Release.name == name)
        if filters is not None:
            for k, v in iteritems(filters):
                query = query.filter_by(k=v)

        print(query)
        resp = query.all()
        return resp


def get_base_release_details(release_id=None, name=None, filters=None):
    session = get_session()
    with session.begin():
        print('Filters %r' % filters)
        print('name %r' % release_id, models.Release)
        query = session.query(
            models.Release,
            models.ReleaseTypeCd,
            models.StatusCd)
        query = query.join(
            models.ReleaseTypeCd,
            models.Release.release_type_cd == models.ReleaseTypeCd.release_type_cd)
        query = query.join(
            models.StatusCd,
            models.Release.status_cd == models.StatusCd.status_cd)

        if release_id is not None:
            query = query.filter(models.Release.release_id == release_id)
        if name is not None:
            query = query.filter(models.Release.name == name)
        if filters is not None:
            for k, v in iteritems(filters):
                query = query.filter_by(k=v)

        print(query)
        resp = query.all()
        return resp


def get_application_release_Details(release_id=None, name=None, filters=None):
    session = get_session()
    with session.begin():
        print('Filters %r' % filters)
        print('name %r' % release_id, models.Release)
        query = session.query(
            models.Release,
            models.AppReleaseInfo,
            models.Project.name.label('project_name'),
            models.Application.app_id.label('application_name'),
            models.Application.app_id.label('application_id'),
            models.StatusCd,
            models.ReleaseTypeCd,
            models.ReleasePlan
        )
        query = query.filter_by(
            release_type_cd=rls_type_cd.application.release_type_cd)
        query = query.join(
            models.AppReleaseInfo,
            models.Release.release_id == models.AppReleaseInfo.release_id)
        query = query.join(
            models.Project,
            models.AppReleaseInfo.project_id == models.Project.project_id)
        query = query.join(
            models.Application,
            models.AppReleaseInfo.application_id == models.Application.app_id)
        query = query.join(
            models.ReleaseTypeCd,
            models.Release.release_type_cd == models.ReleaseTypeCd.release_type_cd)
        query = query.join(
            models.StatusCd,
            models.Release.status_cd == models.StatusCd.status_cd)
        query = query.join(
            models.ReleasePlan,
            models.ReleasePlan.release_plan_id == models.Release.release_plan_id)

        if release_id is not None:
            query = query.filter(models.Release.release_id == release_id)
        if name is not None:
            query = query.filter(models.Release.name == name)
        if filters is not None:
            for k, v in iteritems(filters):
                query = query.filter_by(k=v)

        print(query)
        resp = query.all()
        return resp

def get_application_details(
        release_id=None,app_release_id=None,
        project_id=None,application_id=None,filters=None):
    session = get_session()
    with session.begin():
        print('Filters %r' % filters)
        print('name %r' % release_id, models.AppReleaseInfo)
        query = session.query(models.AppReleaseInfo)
        if release_id is not None:
            query = query.filter(models.AppReleaseInfo.release_id == release_id)
        if app_release_id is not None:
            query = query.filter(models.AppReleaseInfo.app_release_id == app_release_id)
        if project_id is not None:
            query = query.filter(models.AppReleaseInfo.project_id == project_id)
        if application_id is not None:
            query = query.filter(models.AppReleaseInfo.application_id == application_id)
        if filters is not None:
            for k, v in iteritems(filters):
                query = query.filter_by(k=v)

        print(query)
        resp = query.all()
        return resp

def get_infrastructure_release_Details(
        release_id=None, name=None, filters=None):
    session = get_session()
    with session.begin():
        print('Filters %r' % filters)
        print('name %r' % release_id, models.Release)
        query = session.query(
            models.Release,
            models.InfraRelease,
            models.Platform,
            models.ReleasePlan)
        query = query.filter_by(
            release_type_cd=rls_type_cd.infrastructure.release_type_cd)
        query = query.join(
            models.InfraRelease,
            models.Release.release_id == models.InfraRelease.release_id)
        query = query.join(
            models.Platform,
            models.InfraRelease.platform_id == models.Platform.platform_id)
        query = query.join(
            models.ReleaseTypeCd,
            models.Release.release_type_cd == models.ReleaseTypeCd.release_type_cd)
        query = query.join(
            models.StatusCd,
            models.Release.status_cd == models.StatusCd.status_cd)
        query = query.join(
            models.ReleasePlan,
            models.ReleasePlan.release_plan_id == models.Release.release_plan_id)

        if release_id is not None:
            query = query.filter(models.Release.release_id == release_id)
        if name is not None:
            query = query.filter(models.Release.name == name)
        if filters is not None:
            for k, v in iteritems(filters):
                query = query.filter_by(k=v)

        print(query)
        print(query.all())
        resp = query.all()
        return resp


def get_vnf_release_Details(release_id=None, name=None, filters=None):
    session = get_session()
    with session.begin():
        print('Filters %r' % filters)
        print('name %r' % release_id, models.Release)
        query = session.query(
            models.Release,
            models.VnfRelease,
            models.VnfNodeType.name.label('vnf_node'),
            models.VnfSite.name.label('vnf_site'),
            models.ReleasePlan
        )
        query = query.filter_by(
            release_type_cd=rls_type_cd.vnf.release_type_cd)
        query = query.join(
            models.VnfRelease,
            models.Release.release_id == models.VnfRelease.release_id)
        query = query.join(
            models.VnfNodeType,
            models.VnfRelease.vnf_node_id == models.VnfNodeType.vnf_node_id)
        query = query.join(
            models.VnfSite,
            models.VnfRelease.vnf_site_id == models.VnfSite.vnf_site_id)
        query = query.join(
            models.ReleaseTypeCd,
            models.Release.release_type_cd == models.ReleaseTypeCd.release_type_cd)
        query = query.join(
            models.StatusCd,
            models.Release.status_cd == models.StatusCd.status_cd)
        query = query.join(
            models.ReleasePlan,
            models.ReleasePlan.release_plan_id == models.Release.release_plan_id)

        if release_id is not None:
            query = query.filter(models.Release.release_id == release_id)
        if name is not None:
            query = query.filter(models.Release.name == name)
        if filters is not None:
            for k, v in iteritems(filters):
                query = query.filter_by(k=v)

        print(query)
        print(query.all())
        resp = query.all()
        return resp


def get_release_type_cd(
        release_type_cd=None,
        release_type_description=None,
        filters=None):
    session = get_session()
    with session.begin():
        print('Filters %r' % filters)
        print('name %r' % release_type_cd)
        query = session.query(models.ReleaseTypeCd)
        if release_type_cd is not None:
            query = query.filter_by(release_type_cd=release_type_cd)
        if release_type_description is not None:
            query = query.filter_by(
                release_type_description=release_type_description)
            print(filters)
        if filters is not None:
            for k, v in iteritems(filters):
                print(k, v)
                query = query.filter_by(k=v)
        print(query)
        return query.all()


def get_release_conditions(release_id, release_env_id, filters=None):
    session = get_session()
    with session.begin():
        print('Filters %r' % filters)
        print('name %r' % release_id)
        query = session.query(models.ReleaseCondition)
        if release_id is not None:
            query = query.filter(release_id=release_id)
        if release_env_id is not None:
            query = query.filter(release_env_id=release_env_id)
        for k, v in iteritems():
            query = query.filter_by(k=v)
        print(query)
        return query.all()



def get_environment(release_id=None, env_id=None, name=None, filters=None, env_type_cd=None):
    session = get_session()
    with session.begin():
        query = session.query(models.Environment)
        if release_id is not None and release_id != 0:
            query = query.filter_by(release_id=release_id)
        if env_id is not None:
            query = query.filter_by(env_id=env_id)
        if name is not None:
            query = query.filter_by(name=name)
        if env_type_cd is not None:
            query = query.filter_by(env_type_cd=env_type_cd)
        if filters is not None and type(filters) is dict:
            for k, v in filters.items():
                query = query.filter_by(k=v)
        response = query.all()
        resp = []
        for env in response:
            resp.append(env.to_dict())
        return resp



def get_release_environment_execution_stats(
        release_environment_id, filters={}):
    session = get_session()
    with session.begin():
        print('Filters %r' % filters)
        print('name %r' % release_environment_id)
        query = session.query(models.ReleaseExecutionStat)
        if release_environment_id is not None:
            query = query.filter_by(
                release_environment_id=release_environment_id)
        for k, v in iteritems(filters):
            query = query.filter_by(k=v)
        print(query)
        return query.all()


def save_req_data(data):
    session = get_session()
    with session.begin():
        req_data = models.ReleaseReqData()
        print(data)
        req_data.update(data)
        req_data.save(session=session)
    return req_data.to_dict()


def get_req_data(release_id, filters=None):
    session = get_session()
    with session.begin():
        print('Filters %r' % filters)
        print('name %r' % release_id)
        query = session.query(models.ReleaseReqData)
        if release_id is not None:
            query = query.filter_by(req_id=release_id)
        print(query)
        resp = query.all()
        for item in resp:
            if release_id == item.get('req_id'):
                return item
        print(len(resp))
        if len(resp) > 0:
            return resp[0]


def create_release_link(args):
    session = get_session()
    with session.begin():
        req_data = models.ReleaseLink()
        req_data.update(args)
        req_data.save(session=session)
    return req_data.to_dict()


def create_release_link_item(args):
    session = get_session()
    with session.begin():
        req_data = models.ReleaseLinkItem()
        req_data.update(args)
        req_data.save(session=session)
    return req_data.to_dict()


def get_release_links(release_id, link_id=None, filters=None):
    session = get_session()
    with session.begin():
        print('Filters %r' % filters)
        print('name %r' % release_id)
        query = session.query(models.ReleaseLink)
        if release_id is not None:
            query = query.filter_by(release_id=release_id)
        if link_id is not None:
            query = query.filter_by(release_link_id=link_id)
        if filters is not None:
            for k, v in iteritems(filters):
                query = query.filter_by(k=v)
        print(query)
        return query.all()


def get_release_link_items(release_link_id, link_item_id, filters=None):
    session = get_session()
    with session.begin():
        print('Filters %r' % filters)
        print('name %r' % release_link_id)
        query = session.query(models.ReleaseLinkItem)
        if release_link_id is not None:
            query = query.filter_by(release_link_id=release_link_id)
        if link_item_id is not None:
            query = query.filter_by(release_link_item_id=link_item_id)
        if filters is not None:
            for k, v in iteritems(filters):
                query = query.filter_by(k=v)
        print(query)
        return query.all()


def create_workflow(args):
    session = get_session()
    with session.begin():
        req_data = models.Workflow()
        req_data.update(args)
        req_data.save(session=session)
    return req_data.to_dict()


def get_workflow(env_id=None, wf_id=None, filters=None):
    session = get_session()
    with session.begin():
        print('Filters %r' % filters)
        print('name %r' % get_session)
        query = session.query(models.Workflow)
        # query = session.query(models.Workflow, models.StatusCd, models.Frequency)
        if env_id is not None:
            query = query.filter_by(env_id=env_id)
        if wf_id is not None:
            query = query.filter_by(wf_id=wf_id)
        if filters is not None:
            for k, v in iteritems(filters):
                query = query.filter_by(k=v)
        # query = query.join(models.StatusCd, models.Workflow.status_cd == models.StatusCd.status_cd)
        # query = query.join(models.Frequency, models.Workflow.frequency_cd == models.Frequency.frequency_cd)
        print(query)
        return query.all()


def create_stage(args):
    session = get_session()
    with session.begin():
        req_data = models.Stage()
        req_data.update(args)
        req_data.save(session=session)
    return req_data.to_dict()


def get_stage(wf_id=None, stage_id=None, filters=None):
    session = get_session()
    with session.begin():
        print('Filters %r' % filters)
        print('name %r' % get_session)
        query = session.query(models.Stage)
        # query = session.query(models.Stage, models.StatusCd)
        if wf_id is not None:
            query = query.filter_by(wf_id=wf_id)
        if stage_id is not None:
            query = query.filter_by(stage_id=stage_id)
        if filters is not None:
            for k, v in iteritems(filters):
                query = query.filter_by(k=v)
        # query = query.join(models.StatusCd, models.Stage.status_cd == models.StatusCd.status_cd)
        print(query)
        return query.all()


def create_task(args):
    session = get_session()
    with session.begin():
        req_data = models.Task()
        req_data.update(args)
        req_data.save(session=session)
    return req_data.to_dict()


def delete_task(task_id=None, stage_id=None):
    if stage_id is None and task_id is None:
        return "Cannot Delete All Tasks in DB"
    session = get_session()
    with session.begin():
        query = session.query(models.Task)
        if stage_id is not None:
            query = query.filter_by(stage_id=stage_id)
        if task_id is not None:
            query = query.filter_by(task_id=task_id)
        print(query)
        return query.delete()


def delete_stage(stage_id=None, wf_id=None):
    if stage_id is None and wf_id is None:
        return "Cannot Delete All Stages in DB"
    session = get_session()
    with session.begin():
        query = session.query(models.Stage)
        if wf_id is not None:
            query = query.filter_by(wf_id=wf_id)
        if stage_id is not None:
            query = query.filter_by(stage_id=stage_id)
        print(query)
        return query.delete()


def delete_workflow(env_id=None, wf_id=None):
    if env_id is None and wf_id is None:
        return "Cannot Delete All Workflows in DB"
    session = get_session()
    with session.begin():
        query = session.query(models.Workflow)
        if env_id is not None:
            query = query.filter_by(env_id=env_id)
        if wf_id is not None:
            query = query.filter_by(wf_id=wf_id)
        print(query)
        return query.delete()


def get_task(
        task_id=None,
        dag_task_name=None,
        stage_id=None,
        wf_id=None,
        name=None,
        filters=None):
    session = get_session()
    with session.begin():
        print('Filters %r' % filters)
        print('name %r' % get_session)
        query = session.query(models.Task)
        # query = session.query(models.Task, models.StatusCd)
        if task_id is not None:
            query = query.filter_by(task_id=task_id)
        if dag_task_name is not None:
            query = query.filter_by(dag_task_name=dag_task_name)
        if stage_id is not None:
            query = query.filter_by(stage_id=stage_id)
        if wf_id is not None:
            query = query.filter_by(wf_id=wf_id)
        if name is not None:
            query = query.filter_by(name=name)
        if filters is not None:
            for k, v in iteritems(filters):
                query = query.filter_by(k=v)
        # query = query.join(models.StatusCd, models.Task.status_cd == models.StatusCd.status_cd)
        print(query)
        # print(query.all())
        return query.all()


def create_service(args):
    session = get_session()
    with session.begin():
        req_data = models.Service()
        req_data.update(args)
        req_data.save(session=session)
    return req_data.to_dict()


def update_service(service_id, data):
    session = get_session()
    with session.begin():
        query = session.query(models.Service)
        query = query.filter_by(service_id=service_id)
        rows = query.update(data)
        if not rows:
            print('Nothing to update in Service')
    return rows


def get_service(
        service_id=None,
        name=None,
        category=None,
        comments=None,
        filters=None):
    session = get_session()
    with session.begin():
        print('Filters %r' % filters)
        print('name %r' % get_session)
        query = session.query(models.Service)
        if service_id is not None:
            query = query.filter_by(service_id=service_id)
        if name is not None:
            query = query.filter_by(name=name)
        if category is not None:
            query = query.filter_by(category=category)
        if comments is not None:
            query = query.filter_by(comments=comments)
        if filters is not None:
            for k, v in iteritems(filters):
                query = query.filter_by(k=v)
        print(query)
        return query.all()


def get_projects(project_id=None, filters=None):
    session = get_session()
    with session.begin():
        print('Filters %r' % filters)
        print('name %r' % get_session)
        query = session.query(models.Project)
        if project_id is not None:
            query = query.filter_by(project_id=project_id)
        if filters is not None:
            for k, v in iteritems(filters):
                query = query.filter_by(k=v)
        print(query)
        return query.all()


def get_applications(application_id=None, project_id=None, filters=None):
    session = get_session()
    with session.begin():
        print('Filters %r' % filters)
        print('name %r' % get_session)
        query = session.query(models.Application)
        if application_id is not None:
            query = query.filter_by(app_id=application_id)
        if project_id is not None:
            query = query.filter_by(project_id=project_id)
        if filters is not None:
            for k, v in iteritems(filters):
                query = query.filter_by(k=v)
        print(query)
        return query.all()


def create_action(args):
    session = get_session()
    with session.begin():
        req_data = models.Action()
        req_data.update(args)
        req_data.save(session=session)
    return req_data.to_dict()


def update_action(action_id, data):
    session = get_session()
    with session.begin():
        query = session.query(models.Action)
        query = query.filter_by(action_id=action_id)
        rows = query.update(data)
        if not rows:
            print('Nothing to update in Action')
    return rows


def get_action(
        action_id=None,
        service_id=None,
        name=None,
        description=None,
        filters=None):
    session = get_session()
    with session.begin():
        print('Filters %r' % filters)
        print('name %r' % get_session)
        query = session.query(models.Action)
        if service_id is not None:
            query = query.filter_by(service_id=service_id)
        if action_id is not None:
            query = query.filter_by(action_id=action_id)
        if name is not None:
            query = query.filter_by(name=name)
        if description is not None:
            query = query.filter_by(description=description)
        if filters is not None:
            for k, v in iteritems(filters):
                query = query.filter_by(k=v)
        print(query)
        return query.all()


def get_platform(platform_id, name, filters={}):
    session = get_session()
    with session.begin():
        print('Filters %r' % filters)
        print('name %r' % platform_id)
        query = session.query(models.Platform)
        if platform_id is not None:
            query = query.filter_by(platform_id=platform_id)
        if name is not None:
            query = query.filter_by(name=name)
        for k, v in iteritems(filters):
            print(k, v)
            query = query.filter_by(k=v)
        print(query)
        return query.all()


def get_operating_system(os_id, name, platform_id, filters={}):
    session = get_session()
    with session.begin():
        print('Filters %r' % filters)
        print('name %r' % os_id)
        query = session.query(models.OperatingSystem)
        if os_id is not None:
            query = query.filter_by(os_id=os_id)
        if name is not None:
            query = query.filter_by(name=name)
        if platform_id is not None:
            query = query.filter_by(platform_id=platform_id)
        for k, v in iteritems(filters):
            print(k, v)
            query = query.filter_by(k=v)
        print(query)
        return query.all()


def create_milestone(args):
    session = get_session()
    with session.begin():
        req_data = models.Milestone()
        req_data.update(args)
        req_data.save(session=session)
    return req_data.to_dict()

def update_milestone(milestone_id, data):
    session = get_session()
    with session.begin():
        query = session.query(models.Milestone)
        query = query.filter_by(milestone_id=milestone_id)
        rows = query.update(data)
        if not rows:
            print('Nothing to update in Action')
    return rows

def get_milestone(milestone_id=None, release_id=None,filters=None):
    if milestone_id is None and release_id is None:
        print('please specify milestone_id or release id to get the milestones')
    session = get_session()
    with session.begin():
        print ('Filters %r'% filters)
        print ('name %r' % get_session)
        query = session.query(models.Milestone)
        if milestone_id is not None:
            query = query.filter_by(milestone_id=milestone_id)
        if release_id is not None:
            query = query.filter_by(release_id=release_id)
        if filters is not None:
            for k, v in iteritems(filters):
                query = query.filter_by(k=v)
        print (query)
        return query.all()

def create_milestone_status(args):
    session = get_session()
    with session.begin():
        req_data = models.MilestoneStatusCd()
        req_data.update(args)
        req_data.save(session=session)
    return req_data.to_dict()

def update_milestone_status(milestone_status_cd, data):
    session = get_session()
    with session.begin():
        query = session.query(models.MilestoneStatusCd)
        query = query.filter_by(milestone_status_cd=milestone_status_cd)
        rows = query.update(data)
        if not rows:
            print('Nothing to update in Action')
    return rows

def get_milestone_status(milestone_status_cd=None, filters=None):
    session = get_session()
    with session.begin():
        query = session.query(models.MilestoneStatusCd)
        if milestone_status_cd != None:
            query = query.filter_by(milestone_status_cd=milestone_status_cd)
        if filters is not None:
            for k, v in iteritems(filters):
                query = query.filter_by(k=v)
        print (query)
        return query.all()

def create_milestone_type(args):
    session = get_session()
    with session.begin():
        req_data = models.MilestoneTypeCd()
        req_data.update(args)
        req_data.save(session=session)
    return req_data.to_dict()

def update_milestone_type(milestone_type_cd, data):
    session = get_session()
    with session.begin():
        query = session.query(models.MilestoneTypeCd)
        query = query.filter_by(milestone_type_cd=milestone_type_cd)
        rows = query.update(data)
        if not rows:
            print('Nothing to update in Action')
    return rows


def get_milestone_type(milestone_type_cd=None, release_type_cd=None, filters=None):
    session = get_session()
    with session.begin():
        print('Filters %r' % filters)
        print('name %r' % get_session)
        query = session.query(models.MilestoneTypeCd)
        if milestone_type_cd != None:
            query = query.filter_by(milestone_type_cd=milestone_type_cd)
        if release_type_cd != None:
            query = query.filter_by(release_type_cd=release_type_cd)
        if filters is not None:
            for k, v in iteritems(filters):
                query = query.filter_by(k=v)
        print(query)
        return query.all()


def get_vnf_nodes(vnf_node_id, name, filters={}):
    session = get_session()
    with session.begin():
        print('Filters %r' % filters)
        print('name %r' % vnf_node_id)
        query = session.query(models.VnfNodeType)
        if vnf_node_id is not None:
            query = query.filter_by(vnf_node_id=vnf_node_id)
        if name is not None:
            query = query.filter_by(name=name)
        for k, v in iteritems(filters):
            print(k, v)
            query = query.filter_by(k=v)
        print(query)
        return query.all()


def get_vnf_sites(vnf_site_id, name, vnf_node_id, filters={}):
    session = get_session()
    with session.begin():
        print('Filters %r' % filters)
        print('name %r' % vnf_site_id)
        query = session.query(models.VnfSite)
        if vnf_site_id is not None:
            query = query.filter_by(vnf_site_id=vnf_site_id)
        if name is not None:
            query = query.filter_by(name=name)
        if vnf_node_id is not None:
            query = query.filter_by(vnf_node_id=vnf_node_id)
        for k, v in iteritems(filters):
            print(k, v)
            query = query.filter_by(k=v)
        print(query)
        return query.all()


def create_service_fields(args):
    session = get_session()
    with session.begin():
        req_data = models.ServiceFields()
        req_data.update(args)
        req_data.save(session=session)
    return req_data.to_dict()


def update_service_fields(service_field_id, data):
    session = get_session()
    with session.begin():
        query = session.query(models.ServiceFields)
        query = query.filter_by(service_field_id=service_field_id)
        rows = query.update(data)
        if not rows:
            print('Nothing to update in Action')
    return rows


def get_service_fields(
        service_id=None,
        action_id=None,
        service_field_id=None,
        key=None,
        filters=None):
    if service_id is None and action_id is None and service_field_id is None and key is None:
        print('please specify service_id or action_id or service_field_id or key to get the service fields')
    session = get_session()
    with session.begin():
        print('Filters %r' % filters)
        print('name %r' % get_session)
        query = session.query(models.ServiceFields)
        if service_id is not None:
            query = query.filter_by(service_id=service_id)
        if action_id is not None:
            query = query.filter_by(action_id=action_id)
        if service_field_id is not None:
            query = query.filter_by(service_field_id=service_field_id)
        if key is not None:
            query = query.filter_by(key=key)
        if filters is not None:
            for k, v in iteritems(filters):
                query = query.filter_by(k=v)
        print(query)
        return query.all()


def get_output_fields(service_id=None, action_id=None,
                        output_field_id=None, filters=None):
    session = get_session()
    with session.begin():
        print('Filters %r' % filters)
        print('name %r' % get_session)
        query = session.query(models.ServiceActionOutputField)
        if service_id is not None:
            query = query.filter_by(service_id=service_id)
        if action_id is not None:
            query = query.filter_by(action_id=action_id)
        if output_field_id is not None:
            query = query.filter_by(output_field_id=output_field_id)
        if filters is not None:
            for k, v in iteritems(filters):
                query = query.filter_by(k=v)
        print(query)
        return query.all()


def update_environment(env_id, data):
    session = get_session()
    with session.begin():
        query = session.query(models.Environment)
        query = query.filter_by(env_id=env_id)
        rows = query.update(data)
        if not rows:
            print('Nothin to update in Environment')
    return rows


def update_stage(stage_id, data):
    print('data to be updated:{}'.format(data))
    session = get_session()
    with session.begin():
        query = session.query(models.Stage)
        query = query.filter_by(stage_id=stage_id)
        rows = query.update(data)
        if not rows:
            print('Nothing to update in stage')
    return rows


def update_workflow(wf_id, data):
    session = get_session()
    with session.begin():
        query = session.query(models.Workflow)
        query = query.filter_by(wf_id=wf_id)
        rows = query.update(data)
        if not rows:
            print('Nothing to update in workflow')
    return rows


def update_task(task_id=None, dag_task_name=None, data=None):
    session = get_session()
    with session.begin():
        query = session.query(models.Task)
        if task_id is not None:
            query = query.filter_by(task_id=task_id)
        if dag_task_name is not None:
            query = query.filter_by(dag_task_name=dag_task_name)
        rows = query.update(data)
        if not rows:
            print('Nothing to update in Task')
    return rows


def create_template(args):
    session = get_session()
    with session.begin():
        req_data = models.Template()
        req_data.update(args)
        req_data.save(session=session)
        print(req_data.to_dict())
    return req_data.to_dict()


def get_template(template_id=None, template_name=None, filters=None):
    session = get_session()
    with session.begin():
        print('Filters %r' % filters)
        print('name %r' % get_session)
        query = session.query(models.Template)
        if template_id is not None:
            query = query.filter_by(template_id=template_id)
        if template_name is not None:
            query = query.filter_by(template_name=template_name)
        if filters is not None:
            for k, v in iteritems(filters):
                query = query.filter_by(k=v)
        print(query)
        return query.all()


def get_frequency(frequency_cd=None, filters=None):
    session = get_session()
    with session.begin():
        query = session.query(models.Frequency)
        if frequency_cd is not None:
            query = query.filter_by(frequency_cd=frequency_cd)
        if filters is not None:
            for k, v in iteritems(filters):
                query = query.filter_by(k=v)
        print(query)
        return query.all()


def create_frequency(args):
    session = get_session()
    with session.begin():
        req_data = models.Frequency()
        req_data.update(args)
        req_data.save(session=session)
        print(req_data.to_dict())
    return req_data.to_dict()


def get_max_template_version(template_name=None):
    session = get_session()
    with session.begin():
        query = session.query(func.max(models.Template.template_version))
        if template_name is not None:
            query = query.filter_by(template_name=template_name)
        resp = query.all()
        resp = [value for (value,) in resp]
        if resp[0] is None:
            return 0
        return resp[0]


def get_release_name_env_name(env_id):
    session = get_session()
    with session.begin():
        query = session.query(
            models.Environment.name,
            models.Environment.env_id,
            models.Release.name,
            models.Release.release_id)
        if env_id is not None:
            query = query.filter_by(env_id=env_id)
        query = query.join(
            models.Release,
            models.Release.release_id == models.Environment.release_id)
        resp = query.all()
        for iter in resp:
            return (iter[2] + '_' + iter[0] + '_')


def update_release(release_id, data):
    session = get_session()
    with session.begin():
        query = session.query(models.Release)
        query = query.filter_by(release_id=release_id)
        rows = query.update(data)
        if not rows:
            print('Nothing to update in Release')
    return rows


def get_env_type_cd(env_type_cd=None):
    session = get_session()
    with session.begin():
        query = session.query(models.EnvTypeCd)
        if env_type_cd is not None:
            query = query.filter_by(env_type_cd=env_type_cd)
        print(query)
        return query.all()


def create_env_type_cd(args):
    session = get_session()
    with session.begin():
        req_data = models.EnvTypeCd()
        req_data.update(args)
        req_data.save(session=session)
        print(req_data.to_dict())
    return req_data.to_dict()


def delete_service_field(
        service_id=None,
        action_id=None,
        service_field_id=None):
    if service_id is None and action_id is None and service_field_id is None:
        return "Cannot Delete All Service Fields in DB"
    session = get_session()
    with session.begin():
        query = session.query(models.ServiceFields)
        if service_id is not None:
            query = query.filter_by(service_id=service_id)
        if action_id is not None:
            query = query.filter_by(action_id=action_id)
        if service_field_id is not None:
            query = query.filter_by(service_field_id=service_field_id)
        print(query)
        return query.delete()


def delete_action(service_id=None, action_id=None):
    if service_id is None and action_id is None:
        return "Cannot Delete All Actions in DB"
    session = get_session()
    with session.begin():
        query = session.query(models.Action)
        if service_id is not None:
            query = query.filter_by(service_id=service_id)
        if action_id is not None:
            query = query.filter_by(action_id=action_id)
        print(query)
        return query.delete()


def delete_service(service_id=None):
    if service_id is None:
        return "Cannot Delete All Services in DB"
    session = get_session()
    with session.begin():
        query = session.query(models.Service)
        if service_id is not None:
            query = query.filter_by(service_id=service_id)
        print(query)
        return query.delete()


def create_output_fields(args):
    session = get_session()
    with session.begin():
        req_data = models.ServiceActionOutputField()
        req_data.update(args)
        req_data.save(session=session)
    return req_data.to_dict()


def update_output_fields(output_field_id, data):
    session = get_session()
    with session.begin():
        query = session.query(models.ServiceActionOutputField)
        query = query.filter_by(output_field_id=output_field_id)
        rows = query.update(data)
        if not rows:
            print('Nothing to update in Action')
    return rows

def delete_output_field(
        service_id=None,
        action_id=None,
        output_field_id=None):
    if service_id is None and action_id is None and output_field_id is None:
        return "Cannot Delete All Output Fields in DB"
    session = get_session()
    with session.begin():
        query = session.query(models.ServiceActionOutputField)
        if service_id is not None:
            query = query.filter_by(service_id=service_id)
        if action_id is not None:
            query = query.filter_by(action_id=action_id)
        if output_field_id is not None:
            query = query.filter_by(output_field_id=output_field_id)
        print(query)
        return query.delete()

def delete_milestone(
        release_id=None,
        milestone_id=None):
    if release_id is None and milestone_id is None:
        return "Cannot Delete All Milestones in DB"
    session = get_session()
    with session.begin():
        query = session.query(models.Milestone)
        if release_id is not None:
            query = query.filter_by(release_id=release_id)
        if milestone_id is not None:
            query = query.filter_by(milestone_id=milestone_id)
        print(query)
        return query.delete()


def delete_milestone_type(
        release_type_cd=None,
        milestone_type_cd=None):
    if release_type_cd is None and milestone_type_cd is None:
        return "Cannot Delete All Milestone Types in DB"
    session = get_session()
    with session.begin():
        query = session.query(models.MilestoneTypeCd)
        if release_type_cd is not None:
            query = query.filter_by(release_type_cd=release_type_cd)
        if milestone_type_cd is not None:
            query = query.filter_by(milestone_type_cd=milestone_type_cd)
        print(query)
        return query.delete()


def create_release_plan(args):
    session = get_session()
    with session.begin():
        req_data = models.ReleasePlan()
        req_data.update(args)
        req_data.save(session=session)
    return req_data.to_dict()


def update_release_plan(release_plan_id, args):
    session = get_session()
    with session.begin():
        query = session.query(models.ReleasePlan)
        query = query.filter_by(release_plan_id=release_plan_id)
        rows = query.update(args)
        if not rows:
            print('Nothing to update in Action')
    return rows

def delete_release_plan(
        release_plan_id):
    if release_plan_id is None or release_plan_id == 0:
        return "Deleting release plan needs release plan id"
    session = get_session()
    with session.begin():
        query = session.query(models.ReleasePlan)
        if release_plan_id is not None:
            query = query.filter_by(release_plan_id=release_plan_id)
        return query.delete()

def get_release_plan(release_plan_id=None, release_type_cd=None, filters=None):
    session = get_session()
    with session.begin():
        query = session.query(models.ReleasePlan, models.ReleaseTypeCd.color_pref.label('color_pref'))
        query = query.join(
            models.ReleaseTypeCd,
            models.ReleasePlan.release_type_cd == models.ReleaseTypeCd.release_type_cd)
        if release_plan_id is not None:
            query = query.filter(models.ReleasePlan.release_plan_id == release_plan_id)
        if release_type_cd is not None:
            query = query.filter(models.ReleasePlan.release_type_cd == release_type_cd)
        if filters is not None:
            for k, v in iteritems(filters):
                query = query.filter_by(k=v)

        print(query)
        return query.all()

def create_infra_category(args):
    session = get_session()
    with session.begin():
        req_data = models.InfraMetricsCategory()
        req_data.update(args)
        req_data.save(session=session)
        print(req_data.to_dict())
    return req_data.to_dict()

def get_infra_category(
        category_id=None,
        category_name=None,
        filters=None):
    session = get_session()
    with session.begin():
        print('Filters %r' % filters)
        print('name %r' % get_session)
        query = session.query(models.InfraMetricsCategory)
        # query = session.query(models.Task, models.StatusCd)
        if category_id is not None:
            query = query.filter_by(category_id=category_id)
        if category_name is not None:
            query = query.filter_by(category_name=category_name)
        if filters is not None:
            for k, v in iteritems(filters):
                query = query.filter_by(k=v)
        # query = query.join(models.StatusCd, models.Task.status_cd == models.StatusCd.status_cd)
        print(query)
        # print(query.all())
        return query.all()

def create_infra_subcomponent(args):
    session = get_session()
    with session.begin():
        req_data = models.InfraMetricsSubComponent()
        req_data.update(args)
        req_data.save(session=session)
        print(req_data.to_dict())
    return req_data.to_dict()


def get_infra_subcomponent(
        subcomponent_id=None,
        subcomponent_name=None,
        filters=None):
    session = get_session()
    with session.begin():
        print('Filters %r' % filters)
        print('name %r' % get_session)
        query = session.query(models.InfraMetricsSubComponent)
        # query = session.query(models.Task, models.StatusCd)
        if subcomponent_id is not None:
            query = query.filter_by(subcomponent_id=subcomponent_id)
        if subcomponent_name is not None:
            query = query.filter_by(subcomponent_name=subcomponent_name)
        if filters is not None:
            for k, v in iteritems(filters):
                query = query.filter_by(k=v)
        # query = query.join(models.StatusCd, models.Task.status_cd == models.StatusCd.status_cd)
        print(query)
        return query.all()
        # print(query.all())

def create_infra_component(args):
    session = get_session()
    with session.begin():
        req_data = models.InfraMetricsComponent()
        req_data.update(args)
        req_data.save(session=session)
        print(req_data.to_dict())
    return req_data.to_dict()


def get_infra_component(
        component_id=None,
        component_name=None,
        filters=None):
    session = get_session()
    with session.begin():
        print('Filters %r' % filters)
        print('name %r' % get_session)
        query = session.query(models.InfraMetricsComponent)
        # query = session.query(models.Task, models.StatusCd)
        if component_id is not None:
            query = query.filter_by(component_id=component_id)
        if component_name is not None:
            query = query.filter_by(component_name=component_name)
        if filters is not None:
            for k, v in iteritems(filters):
                query = query.filter_by(k=v)
        # query = query.join(models.StatusCd, models.Task.status_cd == models.StatusCd.status_cd)
        print(query)
        return query.all()

def create_infra_metrics(args):
    session = get_session()
    with session.begin():
        req_data = models.InfraMetrics()
        req_data.update(args)
        req_data.save(session=session)
        print(req_data.to_dict())
    return req_data.to_dict()

def get_infra_metrics(
        component_id=None,
        subcomponent_id=None,
        category_id=None,
        start_date=None,
        end_date=None,
        filters=None):
    session = get_session()
    with session.begin():
        print('Filters %r' % filters)
        print('name %r' % get_session)
        query = session.query(models.InfraMetrics)
        # query = session.query(models.Task, models.StatusCd)
        if component_id is not None:
            query = query.filter_by(component_id=component_id)
        if subcomponent_id is not None:
            query = query.filter_by(subcomponent_id=subcomponent_id)
        if category_id is not None:
            query = query.filter_by(category_id=category_id)
        if start_date is not None:
            query = query.filter(models.InfraMetrics.date >= start_date)
        if end_date is not None:
            query= query.filter(models.InfraMetrics.date <= end_date )
        if filters is not None:
            for k, v in iteritems(filters):
                query = query.filter_by(k=v)
        # query = query.join(models.StatusCd, models.Task.status_cd == models.StatusCd.status_cd)
        print(query)
        return query.all()

def create_app_category(args):
    session = get_session()
    with session.begin():
        req_data = models.AppMetricsCategory()
        req_data.update(args)
        req_data.save(session=session)
        print(req_data.to_dict())
    return req_data.to_dict()

def get_app_category(
        category_id=None,
        category_name=None,
        filters=None):
    session = get_session()
    with session.begin():
        print('Filters %r' % filters)
        print('name %r' % get_session)
        query = session.query(models.AppMetricsCategory)
        # query = session.query(models.Task, models.StatusCd)
        if category_id is not None:
            query = query.filter_by(category_id=category_id)
        if category_name is not None:
            query = query.filter_by(category_name=category_name)
        if filters is not None:
            for k, v in iteritems(filters):
                query = query.filter_by(k=v)
        # query = query.join(models.StatusCd, models.Task.status_cd == models.StatusCd.status_cd)
        print(query)
        # print(query.all())
        return query.all()

def create_app_subcomponent(args):
    session = get_session()
    with session.begin():
        req_data = models.AppMetricsSubComponent()
        req_data.update(args)
        req_data.save(session=session)
        print(req_data.to_dict())
    return req_data.to_dict()


def get_app_subcomponent(
        subcomponent_id=None,
        subcomponent_name=None,
        filters=None):
    session = get_session()
    with session.begin():
        print('Filters %r' % filters)
        print('name %r' % get_session)
        query = session.query(models.AppMetricsSubComponent)
        # query = session.query(models.Task, models.StatusCd)
        if subcomponent_id is not None:
            query = query.filter_by(subcomponent_id=subcomponent_id)
        if subcomponent_name is not None:
            query = query.filter_by(subcomponent_name=subcomponent_name)
        if filters is not None:
            for k, v in iteritems(filters):
                query = query.filter_by(k=v)
        # query = query.join(models.StatusCd, models.Task.status_cd == models.StatusCd.status_cd)
        print(query)
        return query.all()
        # print(query.all())

def create_app_component(args):
    session = get_session()
    with session.begin():
        req_data = models.AppMetricsComponent()
        req_data.update(args)
        req_data.save(session=session)
        print(req_data.to_dict())
    return req_data.to_dict()


def get_app_component(
        component_id=None,
        component_name=None,
        filters=None):
    session = get_session()
    with session.begin():
        print('Filters %r' % filters)
        print('name %r' % get_session)
        query = session.query(models.AppMetricsComponent)
        # query = session.query(models.Task, models.StatusCd)
        if component_id is not None:
            query = query.filter_by(component_id=component_id)
        if component_name is not None:
            query = query.filter_by(component_name=component_name)
        if filters is not None:
            for k, v in iteritems(filters):
                query = query.filter_by(k=v)
        # query = query.join(models.StatusCd, models.Task.status_cd == models.StatusCd.status_cd)
        print(query)
        return query.all()

def create_app_metrics(args):
    session = get_session()
    with session.begin():
        req_data = models.AppMetrics()
        req_data.update(args)
        req_data.save(session=session)
        print(req_data.to_dict())
    return req_data.to_dict()

def get_app_metrics(
        component_id=None,
        subcomponent_id=None,
        category_id=None,
        start_date=None,
        end_date=None,
        filters=None):
    session = get_session()
    with session.begin():
        print('Filters %r' % filters)
        print('name %r' % get_session)
        query = session.query(models.AppMetrics)
        # query = session.query(models.Task, models.StatusCd)
        if component_id is not None:
            query = query.filter_by(component_id=component_id)
        if subcomponent_id is not None:
            query = query.filter_by(subcomponent_id=subcomponent_id)
        if category_id is not None:
            query = query.filter_by(category_id=category_id)
        if start_date is not None:
            query = query.filter(models.AppMetrics.date >= start_date)
        if end_date is not None:
            query= query.filter(models.AppMetrics.date <= end_date )
        if filters is not None:
            for k, v in iteritems(filters):
                query = query.filter_by(k=v)
        # query = query.join(models.StatusCd, models.Task.status_cd == models.StatusCd.status_cd)
        print(query)
        return query.all()

def create_master_application(args):
    session = get_session()
    with session.begin():
        req_data = models.MasterApplications()
        req_data.update(args)
        req_data.save(session=session)
    return req_data.to_dict()

def delete_master_application():
    # master_applications will be loaded freshly everytime, thats why we are enabling delte of entire table
    session = get_session()
    with session.begin():
        query = session.query(models.MasterApplications)
        return query.delete()

def get_master_application(computer_system_name=None, platform=None, operating_system=None, filters=None):
    session = get_session()
    with session.begin():
        query = session.query(models.MasterApplications)
        if computer_system_name is not None:
            query = query.filter_by(computer_system_name=computer_system_name)
        if operating_system is not None:
            query = query.filter_by(operating_system=operating_system)
        if platform is not None:
            query = query.filter_by(platform=platform)
        if filters is not None:
            for k, v in iteritems(filters):
                query = query.filter_by(k=v)
        print(query)
        return query.all()

def get_infra_release_impacted_application(release_id=None, computer_system_name=None, platform=None, operating_system=None, application_name=None, filters=None):
    session = get_session()
    with session.begin():
        query = session.query(models.InfraReleaseImpactedApplications)
        if release_id is not None:
            query = query.filter_by(release_id=release_id)
        if computer_system_name is not None:
            query = query.filter_by(computer_system_name=computer_system_name)
        if operating_system is not None:
            query = query.filter_by(operating_system=operating_system)
        if platform is not None:
            query = query.filter_by(platform=platform)
        if application_name is not None:
            query = query.filter_by(application_name=application_name)
        if filters is not None:
            for k, v in iteritems(filters):
                query = query.filter_by(k=v)
        print(query)
        return query.all()


def create_infra_release_impacted_application(args):
    session = get_session()
    with session.begin():
        req_data = models.InfraReleaseImpactedApplications()
        req_data.update(args)
        req_data.save(session=session)
    return req_data.to_dict()


def update_infra_release_impacted_application(impacted_application_id, data):
    session = get_session()
    with session.begin():
        query = session.query(models.InfraReleaseImpactedApplications)
        query = query.filter_by(impacted_application_id=impacted_application_id)
        rows = query.update(data)
        if not rows:
            print('Nothing to update in Action')
    return rows

def update_opt_out_for_application(release_id, application_name, opt_out):
    session = get_session()
    with session.begin():
        query = session.query(models.InfraReleaseImpactedApplications)
        query = query.filter_by(release_id=release_id)
        query = query.filter_by(application_name=application_name)
        rows = query.update({'opt_out': opt_out})
        if not rows:
            print('Nothing to update in Action')
    return rows


################################################################
#                        Delete functions                      #
################################################################

def delete_project(project_id):
    session = get_session()
    with session.begin():
        query = models.Project()
        query = query.filter_by(project_id=project_id).first()
        if not query:
            return {'message': 'No Project found'}
        query.delete(query)
        query.commit()
        return {'message': 'Project has been deleted'}