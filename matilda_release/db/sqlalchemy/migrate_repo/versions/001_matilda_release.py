import datetime
import logging
import uuid

from sqlalchemy import Boolean, BigInteger, Column, DateTime, Enum, Float
from sqlalchemy import dialects, null
from sqlalchemy import Index, Integer, MetaData, VARCHAR, String, Table
from sqlalchemy import Text, ForeignKey, ForeignKeyConstraint
from sqlalchemy.types import NullType
from sqlalchemy.dialects.mysql import JSON

log = logging.getLogger(__name__)


def MediumText():
    return Text().with_variant(dialects.mysql.MEDIUMTEXT(), 'mysql')


def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine

    project = Table(
        'project', meta,
        Column('project_id', String(45), primary_key=True, nullable=False),
        Column('name', String(45), nullable=False),
        Column('owner', String(45)),
        Column('create_dt', DateTime, nullable=False),
        Column('status', String(45), nullable=False)
    )

    condition_fields = Table(
        'condition_fields', meta,
        Column('cond_field_id', Integer, primary_key=True, autoincrement=True),
        Column('type', String(50), nullable=False),
        Column('field_name', String(50), nullable=False),
        Column('order', Integer, nullable=False)
    )

    datatype = Table(
        'datatype', meta,
        Column('datatype_id', Integer, primary_key=True, autoincrement=True),
        Column('datatype', String(50), nullable=False),
    )

    document_types = Table(
        'document_types', meta,
        Column('doc_type_id', Integer, primary_key=True, autoincrement=True),
        Column('name', String(50), nullable=False),
        Column('type', String(50), nullable=False),
        Column('description', String(50)),
        Column('value', String(50)),
    )

    env_type_cd = Table(
        'env_type_cd', meta,
        Column('env_type_cd', Integer, primary_key=True, autoincrement=True),
        Column('env_type_description', String(50), nullable=False, unique=True),
    )

    frequency = Table(
        'frequency', meta,
        Column('frequency_cd', Integer, primary_key=True, autoincrement=True),
        Column('frequency_description', String(50), nullable=False, unique=True),
        Column('dag_usage', String(50), nullable=False),
        Column('comments', String(200)),
        Column('cron_expression', String(50)),
    )

    impacted_systems = Table(
        'impacted_systems', meta,
        Column('release_id', Integer, nullable=False, primary_key=True),
        Column('env_id', Integer, nullable=False, primary_key=True),
        Column('server_ip', String(50), nullable=False, primary_key=True),
        Column('platform_id', Integer),
        Column('os_id', Integer),
        Column('impacted_applications', Text),  # JSON
        Column('exclude_server', Integer, default=0),
    )

    milestone_status_cd = Table(
        'milestone_status_cd', meta,
        Column('milestone_status_cd', Integer, primary_key=True, autoincrement=True),
        Column('milestone_status_description', String(50), nullable=False),
    )

    new_table = Table(
        'new_table', meta,
        Column('event_id', Integer, primary_key=True, autoincrement=True),
        Column('event_type', String(50)),
        Column('source', String(50)),
        Column('source_id', String(50)),
        Column('time', String(50)),
        Column('message', String(50)),
        Column('status', String(50)),
        Column('output', String(50)),
    )

    platform = Table(
        'platform', meta,
        Column('platform_id', Integer, primary_key=True, autoincrement=True),
        Column('name', String(45), nullable=False),
        Column('status', String(45), nullable=False)
    )

    application = Table(
        'application', meta,
        Column('app_id', String(50), nullable=False),
        Column('owner', String(50), nullable=False),
        Column('create_dt', DateTime, nullable=False),
        Column('status', String(50), nullable=False),
        Column('project_id', String(50), ForeignKey('project.project_id'), nullable=False),
        Index('fkIdx_177', 'project_id')
    )

    status_type_cd = Table(
        'status_type_cd', meta,
        Column('status_type_cd', Integer, primary_key=True, autoincrement=True),
        Column('status_type_description', String(100), unique=True),
    )

    status_cd = Table(
        'status_cd', meta,
        Column('status_cd', Integer, primary_key=True, nullable=False, unique=True),
        Column('status_type_cd', Integer, ForeignKey('status_type_cd.status_type_cd'), nullable=False),
        Column('status_description', String(100), nullable=False),
        Column('order', Integer, nullable=False),
    )

    release_type_cd = Table(
        'release_type_cd', meta,
        Column('release_type_cd', Integer, primary_key=True),
        Column('release_type_description', String(100), unique=True),
        Column('color_pref', String(20), default='#ffffff')
    )

    release_plan = Table(
        'release_plan', meta,
        Column('release_plan_id', Integer, primary_key=True, autoincrement=True),
        Column('release_type_cd', Integer, ForeignKey('release_type_cd.release_type_cd'), nullable=False),
        Column('release_plan_name', String(250), nullable=False, unique=True),
        Column('release_plan_description', Text),
        Column('release_owner', String(100)),
        Column('create_dt', DateTime, nullable=False),
        Column('release_dt', DateTime, nullable=False),
    )

    release = Table(
        'release', meta,
        Column('release_id', Integer, primary_key=True, nullable=False, autoincrement=True),
        Column('name', String(50), nullable=False, unique=True),
        Column('version', String(50)),
        Column('create_dt', DateTime, nullable=False),
        Column('start_dt', DateTime),
        Column('complete_dt', DateTime),
        Column('release_dt', DateTime),
        Column('description', Text),
        Column('status_cd', Integer, ForeignKey('status_cd.status_cd'), nullable=False, default=1),
        Column('release_type_cd', Integer, ForeignKey('release_type_cd.release_type_cd'), nullable=False, default=1),
        Column('release_plan_id', Integer, ForeignKey('release_plan.release_plan_id')),
        Index('fkIdx_release', 'release_plan_id')
    )

    template = Table(
        'template', meta,
        Column('template_id', Integer, primary_key=True, autoincrement=True),
        Column('template_name', String(100), nullable=False, unique=True),
        Column('template_version', Integer, nullable=False, unique=True),
        Column('template_json', Text, nullable=False),  # JSON
    )

    service = Table(
        'service', meta,
        Column('service_id', String(20), primary_key=True, nullable=False),
        Column('name', String(50), nullable=False, unique=True),
        Column('category', String(50), nullable=False),
        Column('comments', Text)
    )

    actions = Table(
        'actions', meta,
        Column('action_id', String(20), primary_key=True, nullable=False),
        Column('name', String(50), nullable=False),
        Column('description', Text),
        Column('service_id', String(20), ForeignKey('service.service_id'), nullable=False, unique=True),
        Index('fkIdx_actions', 'service_id')
    )

    service_action_output_fields = Table(
        'service_action_output_fields', meta,
        Column('output_field_id', String(30), primary_key=True, nullable=False),
        Column('service_id', String(20), ForeignKey('service.service_id'), nullable=False),
        Column('action_id', String(20), ForeignKey('actions.action_id'), nullable=False, unique=True),
        Column('output_field_name', String(50), unique=True),
        Index('fkIdx_saof', 'service_id', 'action_id')
    )

    service_fields = Table(
        'service_fields', meta,
        Column('service_field_id', String(30), primary_key=True, nullable=False),
        Column('`key`', String(50), nullable=False, unique=True),
        Column('label', String(50), nullable=False),
        Column('placeholder', String(255)),
        Column('control_type', String(45)),
        Column('required', String(45)),
        Column('order', Integer),
        Column('options', Text),
        Column('field_type', String(50)),
        Column('description', Text),
        Column('service_id', String(20), ForeignKey('service.service_id'), nullable=False),
        Column('action_id', String(20), ForeignKey('actions.action_id'), nullable=False),
        Index('fkIdx_sf', 'service_id', 'action_id', unique=True)
    )

    output_fields = Table(
        'output_fields', meta,
        Column('output_field_id', Integer, primary_key=True, autoincrement=True),
        Column('service_id', String(20), ForeignKey('service.service_id'), nullable=False),
        Column('action_id', String(20), ForeignKey('actions.action_id'), nullable=False),
        Column('fields', Text),
        Index('fkIdx_of', 'service_id', 'action_id')
    )

    vnf_node_type = Table(
        'vnf_node_type', meta,
        Column('vnf_node_id', Integer, primary_key=True, autoincrement=True),
        Column('name', String(50), nullable=False),
        Column('status', String(50)),
    )

    vnf_sites = Table(
        'vnf_sites', meta,
        Column('vnf_site_id', Integer, primary_key=True, autoincrement=True),
        Column('name', String(50), nullable=False),
        Column('status', String(50), nullable=False),
        Column('vnf_node_id', Integer, ForeignKey('vnf_node_type.vnf_node_id'))
    )

    vnf_release = Table(
        'vnf_release', meta,
        Column('vnf_release_id', Integer, primary_key=True, autoincrement=True),
        Column('vnf_node_id', Integer, ForeignKey('vnf_node_type.vnf_node_id'), nullable=False, ),
        Column('vnf_site_id', Integer, ForeignKey('vnf_sites.vnf_site_id'), nullable=False, ),
        Column('release_id', Integer, ForeignKey('release.release_id'), nullable=False, ),
    )

    environment = Table(
        'environment', meta,
        Column('env_id', Integer, primary_key=True, nullable=False, autoincrement=True),
        Column('name', String(50), nullable=False, unique=True),
        Column('env_type_cd', Integer, ForeignKey('env_type_cd.env_type_cd'), nullable=False, default=1),
        Column('create_dt', DateTime),
        Column('start_dt', DateTime),
        Column('end_dt', DateTime),
        Column('status_cd', Integer, ForeignKey('status_cd.status_cd'), nullable=False, default=1),
        Column('release_id', Integer, ForeignKey('release.release_id'), nullable=False),
        Index('fkIdk_env', 'release_id', unique=True)
    )

    workflow = Table(
        'workflow', meta,
        Column('wf_id', Integer, primary_key=True, nullable=False, autoincrement=True),
        Column('name', String(50), nullable=False),
        Column('create_dt', DateTime, nullable=False),
        Column('planned_start_dt', DateTime),
        Column('actual_start_dt', DateTime),
        Column('planned_end_dt', DateTime),
        Column('actual_end_dt', DateTime),
        Column('status_cd', Integer, ForeignKey('status_cd.status_cd'), nullable=False, default=1),
        Column('owner', String(50), nullable=False),
        Column('order', Integer, nullable=False),
        Column('description', Text, nullable=False),
        Column('ignore_failure', String(50), nullable=False),
        Column('template_id', Integer),
        Column('env_id', Integer, ForeignKey('environment.env_id'), nullable=False),
        Column('frequency_cd', Integer, ForeignKey('frequency.frequency_cd'), default=1),
        Column('dag_name', String(50), unique=True),
        Index('fkIdx_workflow', 'env_id')
    )

    stages = Table(
        'stages', meta,
        Column('stage_id', Integer, primary_key=True, nullable=False, autoincrement=True),
        Column('wf_id', Integer, ForeignKey('workflow.wf_id'), nullable=False, index=True),
        Column('name', String(50), nullable=False),
        Column('create_dt', DateTime, nullable=False),
        Column('planned_start_dt', DateTime),
        Column('actual_start_dt', DateTime),
        Column('planned_end_dt', DateTime),
        Column('actual_end_dt', DateTime),
        Column('order', Integer, nullable=False),
        Column('owner', String(50)),
        Column('status_cd', Integer, ForeignKey('status_cd.status_cd'), nullable=False, default=1),
        Column('stage_ui_id', String(50)))


    operating_system = Table(
        'operating_system', meta,
        Column('os_id', Integer, primary_key=True, autoincrement=True),
        Column('name', String(50), nullable=False),
        Column('version', String(50), nullable=False),
        Column('status', String(50), nullable=False),
        Column('platform_id', Integer, ForeignKey('platform.platform_id')),
    )

    stage_condition = Table(
        'stage_condition', meta,
        Column('stage_condition_id', Integer, primary_key=True, autoincrement=True),
        Column('stage_id', Integer, ForeignKey('stages.stage_id'), nullable=False),
        Column('cond_field_id', Integer, ForeignKey('condition_fields.cond_field_id'), nullable=False, ),
        Column('parameter', String(50), nullable=False),
        Column('operator', String(50), nullable=False),
        Column('value', String(50), nullable=False),
        Column('ignore_failure', String(50)),
        Column('status', String(50), nullable=False),
        Column('importance', Integer),
        Index('fkIdx_sc', 'stage_id', 'cond_field_id')
    )

    task_group = Table(
        'task_group', meta,
        Column('task_group_id', Integer, primary_key=True, autoincrement=True),
        Column('stage_id', Integer, ForeignKey('stages.stage_id'), nullable=False),
        Column('name', String(50), nullable=False),
        Column('create_dt', DateTime, nullable=False),
        Column('planned_start_dt', DateTime, nullable=False),
        Column('actual_start_dt', DateTime),
        Column('planned_end_dt', DateTime),
        Column('actual_end_dt', DateTime),
        Column('status', String(50), nullable=False),
        Index('fkIdx_tg', 'stage_id')
    )

    workflow_condition = Table(
        'workflow_condition', meta,
        Column('wf_condition_id', Integer, primary_key=True, autoincrement=True),
        Column('wf_id', Integer, ForeignKey('workflow.wf_id'), nullable=False),
        Column('cond_field_id', Integer, ForeignKey('condition_fields.cond_field_id'), nullable=False),
        Column('parameter', String(45), nullable=False),
        Column('operator', String(45), nullable=False),
        Column('value', String(45), nullable=False),
        Column('ignore_failure', String(45)),
        Column('importance', Integer),
        Column('status', String(45), nullable=False),
        Index('fkIdx_wc', 'wf_id', 'cond_field_id')
    )

    master_servers = Table(
        'master_servers', meta,
        Column('host_name', String(150), unique=True),
        Column('os_id', Integer, ForeignKey('operating_system.os_id')),
        Column('platform_id', Integer, ForeignKey('platform.platform_id')),
        Column('computer_system_name', String(250), unique=True),
    )

    master_systems = Table(
        'master_systems', meta,
        Column('system_name', String(250), nullable=False, unique=True),
        Column('system_description', String(250), nullable=False),
        Column('system_code', String(25)),
        Column('system_owner', String(250)),
        Column('system_owner_email', String(100)),
        Column('relationship_type', String(250)),
        Column('computer_system_name', String(250), ForeignKey('master_servers.computer_system_name')),
    )

    release_plan_docs = Table(
        'release_plan_docs', meta,
        Column('rls_art_id', Integer, primary_key=True),
        Column('release_plan_id', Integer, ForeignKey('release_plan.release_plan_id'), nullable=False),
        Column('source', Text, nullable=False),
        Column('value', Text, nullable=False),
        Column('description', Text, nullable=False),
        Column('doc_type_id', Integer, ForeignKey('document_types.doc_type_id'), nullable=False),
        Index('fkIdx_rpd', 'release_plan_id', 'doc_type_id')
    )

    release_plan_history = Table(
        'release_plan_history', meta,
        Column('rls_history_id', Integer, primary_key=True, autoincrement=True),
        Column('activity', Text, nullable=False),
        Column('description', Text),
        Column('start_dt', DateTime),
        Column('end_dt', DateTime, nullable=False),
        Column('release_plan_id', Integer, ForeignKey('release_plan.release_plan_id'), nullable=False),
        Index('fkIdx_rph', 'release_plan_id')
    )

    milestone_type_cd = Table(
        'milestone_type_cd', meta,
        Column('milestone_type_cd', Integer, primary_key=True, autoincrement=True),
        Column('milestone_type_description', String(100), nullable=False, unique=True),
        Column('release_type_cd', Integer, ForeignKey('release_type_cd.release_type_cd')),
    )

    action_fields = Table(
        'action_fields', meta,
        Column('action_field_id', Integer, primary_key=True, autoincrement=True),
        Column('field', String(50), nullable=False),
        Column('type', String(50), nullable=False),
        Column('options', Text, nullable=False),
        Column('mandatory', String(50), nullable=False),
        Column('datatype_id', Integer, ForeignKey('datatype.datatype_id'), nullable=False),
        Column('action_id', String(20), ForeignKey('actions.action_id'), nullable=False),
        Index('fkIdx_af', 'datatype_id', 'action_id')
    )

    env_activity = Table(
        'env_activity', meta,
        Column('env_activity_id', Integer, primary_key=True, autoincrement=True),
        Column('env_id', Integer, ForeignKey('environment.env_id'), nullable=False),
        Column('activity', Text, nullable=False),
        Column('create_dt', DateTime, nullable=False),
        Index('fkIdx_ea', 'env_id')
    )

    env_condition = Table(
        'env_condition', meta,
        Column('env_condition_id', Integer, primary_key=True, autoincrement=True),
        Column('env_id', Integer, ForeignKey('environment.env_id'), nullable=False),
        Column('cond_field_id', Integer, ForeignKey('condition_fields.cond_field_id'), nullable=False),
        Column('parameter', String(50), nullable=False),
        Column('operator', String(50), nullable=False),
        Column('value', String(50), nullable=False),
        Column('ignore_failure', String(50)),
        Column('importance', Integer),
        Column('status', String(50), nullable=False),
        Index('fkIdx_ec', 'env_id', 'cond_field_id')
    )

    infra_release = Table(
        'infra_release', meta,
        Column('infra_release_id', Integer, primary_key=True, autoincrement=True),
        Column('os_id', Integer, ForeignKey('operating_system.os_id'), nullable=False),
        Column('platform_id', Integer, ForeignKey('platform.platform_id'), nullable=False),
        Column('release_id', Integer, ForeignKey('release.release_id'), nullable=False),
        Index('fkIdx_ir', 'os_id', 'platform_id', 'release_id')
    )

    infra_release_servers = Table(
        'infra_release_servers', meta,
        Column('infra_release_server_id', Integer, primary_key=True, autoincrement=True),
        Column('release_id', Integer, ForeignKey('release.release_id'), nullable=False, unique=True),
        Column('host_name', String(150), nullable=False, unique=True),
        Column('os_id', Integer, ForeignKey('operating_system.os_id'), nullable=False),
        Column('platform_id', Integer, ForeignKey('platform.platform_id'), nullable=False)
    )

    infra_release_applications = Table(
        'infra_release_applications', meta,
        Column('infra_release_server_id', Integer, ForeignKey('infra_release_servers.infra_release_server_id'),
               nullable=False, unique=True),
        Column('application_name', String(250), nullable=False, unique=True),
        Column('application_description', String(250), nullable=False),
        Column('application_owner', String(150)),
        Column('application_owner_email', String(150), nullable=False),
    )

    milestone = Table(
        'milestone', meta,
        Column('milestone_id', Integer, primary_key=True, autoincrement=True),
        Column('milestone_description', String(250), nullable=False, unique=True),
        Column('milestone_status_cd', Integer, ForeignKey('milestone_status_cd.milestone_status_cd')),
        Column('start_dt', DateTime),
        Column('end_dt', DateTime),
        Column('percent_complete', Integer, default=0),
        Column('release_id', Integer, ForeignKey('release.release_id'), unique=True),
    )

    release_condition = Table(
        'release_condition', meta,
        Column('rls_condition_id', Integer, primary_key=True,
               autoincrement=True),
        Column('release_id', Integer, ForeignKey('release.release_id'), nullable=False),
        Column('cond_field_id', Integer, ForeignKey('condition_fields.cond_field_id'), nullable=False),
        Column('parameter', String(50), nullable=False),
        Column('operator', String(50), nullable=False),
        Column('value', String(50), nullable=False),
        Column('ignore_failure', String(50)),
        Column('importance', Integer),
        Column('status', String(50), nullable=False),
        Index('fkIdx_rc', 'release_id', 'cond_field_id')
    )

    release_links = Table(
        'release_links', meta,
        Column('release_link_id', Integer, primary_key=True, autoincrement=True),
        Column('name', Text),
        Column('url', Text),
        Column('source', Text),
        Column('description', Text),
        Column('release_id', Integer, ForeignKey('release.release_id'), nullable=False),
        Index('fkIdx_rl', 'release_id')
    )

    release_link_items = Table(
        'release_link_items', meta,
        Column('release_link_item_id', Integer, primary_key=True, autoincrement=True),
        Column('data', Text),  # JSON
        Column('release_link_id', Integer, ForeignKey('release_links.release_link_id'), nullable=False),
        Index('fkIdx_rli', 'release_link_id')
    )

    release_plan_milestone = Table(
        'release_plan_milestone', meta,
        Column('rls_plan_milestone_id', Integer, primary_key=True, autoincrement=True),
        Column('start_dt', DateTime, nullable=False),
        Column('end_dt', DateTime, nullable=False),
        Column('description', Text, nullable=False),
        Column('release_plan_id', Integer, ForeignKey('release_plan.release_plan_id'), nullable=False),
        Column('milestone_id', Integer, ForeignKey('milestone.milestone_id'), nullable=False),
        Index('fkIdx_rpm', 'release_plan_id', 'milestone_id')
    )

    release_milestone = Table(
        'release_milestone', meta,
        Column('release_milestone_id', Integer, primary_key=True, autoincrement=True),
        Column('start_dt', DateTime, nullable=False),
        Column('create_dt', DateTime, nullable=False),
        Column('end_dt', DateTime, nullable=False),
        Column('description', Text),
        Column('release_type', String(50), nullable=False),
        Column('status_cd', Integer, ForeignKey('milestone_status_cd.milestone_status_cd'), nullable=False),
        Column('release_id', Integer, ForeignKey('release.release_id'), nullable=False),
        Column('rls_plan_milestone_id', Integer, ForeignKey('release_plan_milestone.rls_plan_milestone_id'),
               nullable=False),
        Index('fkIdx_rm', 'rls_plan_milestone_id', 'release_id', 'status_cd')
    )

    task = Table(
        'task', meta,
        Column('task_id', Integer, primary_key=True, autoincrement=True),
        Column('name', String(50), nullable=False),
        Column('dag_task_name', String(200), nullable=True),
        Column('create_dt', DateTime, nullable=False),
        Column('planned_start_dt', DateTime),
        Column('actual_start_dt', DateTime),
        Column('planned_end_dt', DateTime),
        Column('actual_end_dt', DateTime),
        Column('order', Integer, nullable=False),
        Column('owner', String(50)),
        Column('ignore_failure', String(50)),
        Column('status_cd', Integer, nullable=False, default=1),
        Column('input', Text),
        Column('output', Text),
        Column('task_ui_id', String(50)),
        Column('duration', String(50)),
        Column('wf_id', Integer, ForeignKey('workflow.wf_id')),
        Column('action_id', String(25), ForeignKey('actions.action_id'),nullable=False),
        Column('service_id', String(25), ForeignKey('service.service_id'),nullable=False),
        Column('stage_id', Integer, ForeignKey('stages.stage_id')),
        Column('task_group_id', Integer, ForeignKey('task_group.task_group_id')),
        Column('status_cd', Integer, ForeignKey('status_cd.status_cd')),
        Index('fkIdx_task', 'action_id', 'service_id', 'stage_id', 'task_group_id'))

    task_condition = Table(
        'task_condition', meta,
        Column('task_condition_id', Integer, primary_key=True, autoincrement=True),
        Column('parameter', String(45), nullable=False),
        Column('operator', String(45), nullable=False),
        Column('value', String(45), nullable=False),
        Column('status', String(45), nullable=False),
        Column('task_id', Integer, ForeignKey('task.task_id'), nullable=False),
        Column('cond_field_id', Integer, ForeignKey('condition_fields.cond_field_id'), nullable=False),
        Index('fkIdx_tc', 'task_id', 'cond_field_id')
    )

    app_release_info = Table(
        'app_release_info', meta,
        Column('app_release_id', Integer, primary_key=True, autoincrement=True),
        Column('application', String(50)),
        Column('project', String(50), ForeignKey('project.project_id')),
        Column('portfolio', String(50)),
        Column('project_id', String(50), nullable=False),
        Column('application_id', String(50), ForeignKey('application.app_id'), nullable=False),
        Column('release_id', Integer, ForeignKey('release.release_id'), nullable=False),
        Index('fkIdx_ari', 'project_id', 'application_id', 'release_id')
    )
    app_metrics_category = Table(
        'app_metrics_category', meta,
        Column('category_id', Integer, primary_key=True, autoincrement=True),
        Column('category_name', String(50),nullable=False))

    app_metrics_component = Table(
        'app_metrics_component', meta,
        Column('component_id', Integer, primary_key=True, autoincrement=True),
        Column('component_name', String(50), nullable=False))

    app_metrics_subcomponent = Table(
        'app_metrics_subcomponent', meta,
        Column('subcomponent_id', Integer, primary_key=True, autoincrement=True),
        Column('subcomponent_name', String(50), nullable=False))

    app_metrics = Table(
        'app_metrics', meta,
        Column('component_id', Integer,nullable=False),
        Column('subcomponent_id', Integer, nullable=False),
        Column('category_id', Integer, nullable=False),
        Column('date', DateTime, nullable=False),
        Column('metrics', Integer, nullable=False),
        Column('component_id', Integer, ForeignKey('app_metrics_component.component_id'), nullable=False),
        Column('subcomponent_id', Integer, ForeignKey('app_metrics_subcomponent.subcomponent_id'), nullable=False),
        Column('category_id', Integer, ForeignKey('app_metrics_category.category_id'), nullable=False)
    )

    infra_metrics_category = Table(
        'infra_metrics_category', meta,
        Column('category_id', Integer, primary_key=True, autoincrement=True),
        Column('category_name', String(50),nullable=False))

    infra_metrics_component = Table(
        'infra_metrics_component', meta,
        Column('component_id', Integer, primary_key=True, autoincrement=True),
        Column('component_name', String(50), nullable=False))

    infra_metrics_subcomponent = Table(
        'infra_metrics_subcomponent', meta,
        Column('subcomponent_id', Integer, primary_key=True, autoincrement=True),
        Column('subcomponent_name', String(50), nullable=False))

    infra_metrics = Table(
        'infra_metrics', meta,
        Column('component_id', Integer, nullable=False),
        Column('subcomponent_id', Integer, nullable=False),
        Column('category_id', Integer, nullable=False),
        Column('date', DateTime, nullable=False),
        Column('metrics', Integer, nullable=False),
        Column('component_id', Integer, ForeignKey('infra_metrics_component.component_id'), nullable=False),
        Column('subcomponent_id', Integer, ForeignKey('infra_metrics_subcomponent.subcomponent_id'), nullable=False),
        Column('category_id', Integer, ForeignKey('infra_metrics_category.category_id'), nullable=False)
    )



    master_applications = Table(
        'master_applications', meta,
        Column('master_application_id', Integer, primary_key=True, autoincrement=True),
        Column('computer_system_name', String(250), nullable=False),
        Column('application_name', String(250), nullable=True),
        Column('environment', String(20), nullable=False),
        Column('platform', String(250),nullable=False),
        Column('platform_from_excel', String(250)),
        Column('operating_system', String(250),nullable=False),
        Column('test_type_prod', String(150)),
        Column('test_type_non_prod', String(150)),
        Column('app_owner_name', String(100)),
        Column('tester_name', String(100)),
        Column('test_set_or_folder',String(100),nullable=False))


    tables = [project, condition_fields, datatype, document_types, env_type_cd, frequency, impacted_systems,
              milestone_status_cd, new_table, platform, application, status_type_cd, status_cd, release_type_cd,
              release_plan, release, template, service, actions, service_action_output_fields, service_fields,
              output_fields, vnf_node_type, vnf_sites, vnf_release, environment, workflow, stages, operating_system,
              stage_condition, task_group, workflow_condition, master_servers, master_systems, release_plan_docs,
              release_plan_history, milestone_type_cd, action_fields, env_activity, env_condition, infra_release,
              infra_release_servers, infra_release_applications, milestone, release_condition,
              release_links, release_link_items, release_plan_milestone, release_milestone,app_release_info,task,task_condition,
              app_metrics_category,app_metrics_component,app_metrics_subcomponent,app_metrics,master_applications,infra_metrics_category,
              infra_metrics_component,infra_metrics_subcomponent,infra_metrics]

    print(len(tables))

    for table in tables:
        try:
            print(table)
            table.create()
        except Exception:
            log.info(repr(table))
            log.exception('Exception while creating table')
            raise

    if migrate_engine.name == 'mysql':
        migrate_engine.execute(
            'ALTER TABLE migrate_version CONVERT TO CHARACTER SET utf8')
        migrate_engine.execute(
            'ALTER DATABASE %s DEFAULT CHARACTER SET utf8' %
            migrate_engine.url.database)


def downgrade(migrage_engine):
    raise NotImplementedError('Downgrade is not implemented')