# coding: utf-8
import datetime
import sqlite3
from sqlite3 import Date

import sqlalchemy
from sqlalchemy import ForeignKey, Index, Table, text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func

from oslo_config import cfg
from oslo_db.sqlalchemy import models
from sqlalchemy import (Column, String)
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import orm
from sqlalchemy import DateTime, Integer, Text, JSON, Date

CONF = cfg.CONF
BASE = declarative_base()


def MediumText():
    return Text().with_variant(MEDIUMTEXT(), 'mysql')


class MatildaRlsBase(models.ModelBase):
    metadata = None

    def __copy__(self):
        session = orm.Session()

        copy = session.merge(self, load=False)
        session.expunge(copy)
        return copy

    def save(self, session=None):
        from matilda_release.db.sqlalchemy import api as db_api
        if session is None:
            session = db_api.get_session()

        super(MatildaRlsBase, self).save(session=session)

    def delete(self, session=None):
        from matilda_release.db.sqlalchemy import api as db_api
        if session is None:
            session = db_api.get_session()

        super(MatildaRlsBase, self).delete(session=session)

    def __repr__(self):
        items = ['%s=%r' % (col.name, getattr(self, col.name))
                 for col in self.__table__.columns]
        return "<%s.%s[object at %x] {%s}>" % (self.__class__.__module__,
                                               self.__class__.__name__,
                                               id(self), ','.join(items))

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ActionField(BASE, MatildaRlsBase):
    __tablename__ = 'action_fields'

    action_field_id = Column(Integer, primary_key=True)
    field = Column(String(45), nullable=False)
    type = Column(String(45), nullable=False)
    options = Column(Text, nullable=False)
    mandatory = Column(String(45), nullable=False)
    datatype_id = Column(ForeignKey('datatype.datatype_id'), nullable=False, index=True)
    action_id = Column(ForeignKey('actions.action_id'), nullable=False, index=True)

    action = relationship('Action')
    datatype = relationship('Datatype')


class Action(BASE, MatildaRlsBase):
    __tablename__ = 'actions'
    __table_args__ = (
        Index('actions_service_id_name_uindex', 'service_id', 'name', unique=True),
    )

    action_id = Column(String(20), primary_key=True)
    name = Column(String(45), nullable=False)
    description = Column(Text)
    service_id = Column(ForeignKey('service.service_id'), nullable=False, index=True)

    service = relationship('Service')


class AppReleaseInfo(BASE, MatildaRlsBase):
    __tablename__ = 'app_release_info'

    app_release_id = Column(Integer, primary_key=True)
    application = Column(String(45))
    project = Column(String(45))
    portfolio = Column(String(45))
    project_id = Column(ForeignKey('project.project_id'), nullable=False, index=True)
    application_id = Column(ForeignKey('application.app_id'), nullable=False, index=True)
    release_id = Column(ForeignKey('release.release_id'), nullable=False, index=True)

    application1 = relationship('Application')
    project1 = relationship('Project')
    release = relationship('Release')


class Application(BASE, MatildaRlsBase):
    __tablename__ = 'application'

    app_id = Column(String(45), primary_key=True)
    owner = Column(String(45), nullable=False)
    create_dt = Column(DateTime, nullable=False, default=datetime.datetime.now)
    status = Column(String(45), nullable=False)
    project_id = Column(ForeignKey('project.project_id'), nullable=False, index=True)

    project = relationship('Project')


class ConditionField(BASE, MatildaRlsBase):
    __tablename__ = 'condition_fields'

    cond_field_id = Column(Integer, primary_key=True)
    type = Column(String(45), nullable=False)
    field_name = Column(String(45), nullable=False)
    order = Column(Integer, nullable=False)


class Datatype(BASE, MatildaRlsBase):
    __tablename__ = 'datatype'

    datatype_id = Column(Integer, primary_key=True)
    datatype = Column(String(45), nullable=False)


class DocumentType(BASE, MatildaRlsBase):
    __tablename__ = 'document_types'

    doc_type_id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    type = Column(String(45), nullable=False)
    description = Column(Text)
    value = Column(Text)


class EnvActivity(BASE, MatildaRlsBase):
    __tablename__ = 'env_activity'

    env_activity_id = Column(Integer, primary_key=True)
    env_id = Column(ForeignKey('environment.env_id'), nullable=False, index=True)
    activity = Column(Text, nullable=False)
    create_dt = Column(DateTime, nullable=False, default=datetime.datetime.now)

    env = relationship('Environment')


class EnvCondition(BASE, MatildaRlsBase):
    __tablename__ = 'env_condition'

    env_condition_id = Column(Integer, primary_key=True)
    env_id = Column(ForeignKey('environment.env_id'), nullable=False, index=True)
    cond_field_id = Column(ForeignKey('condition_fields.cond_field_id'), nullable=False, index=True)
    parameter = Column(String(45), nullable=False)
    operator = Column(String(45), nullable=False)
    value = Column(String(45), nullable=False)
    ignore_failure = Column(String(45))
    importance = Column(Integer)
    status = Column(String(45), nullable=False)

    cond_field = relationship('ConditionField')
    env = relationship('Environment')


class EnvTypeCd(BASE, MatildaRlsBase):
    __tablename__ = 'env_type_cd'

    env_type_cd = Column(Integer, primary_key=True)
    env_type_description = Column(String(100), nullable=False, unique=True)


class Environment(BASE, MatildaRlsBase):
    __tablename__ = 'environment'
    __table_args__ = (
        Index('environment_release_id_name_uindex', 'release_id', 'name', unique=True),
    )

    env_id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    env_type_cd = Column(ForeignKey('env_type_cd.env_type_cd'), nullable=False, index=True, server_default=text("'1'"))
    start_dt = Column(DateTime)
    create_dt = Column(DateTime, default=datetime.datetime.now)
    end_dt = Column(DateTime)
    status_cd = Column(ForeignKey('status_cd.status_cd'), nullable=False, index=True, server_default=text("'1'"))
    release_id = Column(ForeignKey('release.release_id'), nullable=False, index=True)


    env_type_cd1 = relationship('EnvTypeCd')
    release = relationship('Release')
    status_cd1 = relationship('StatusCd')


class Frequency(BASE, MatildaRlsBase):
    __tablename__ = 'frequency'

    frequency_cd = Column(Integer, primary_key=True)
    frequency_description = Column(String(50), nullable=False, unique=True)
    dag_usage = Column(String(50), nullable=False)
    comments = Column(String(200))
    cron_expression = Column(String(50))


class InfraRelease(BASE, MatildaRlsBase):
    __tablename__ = 'infra_release'

    infra_release_id = Column(Integer, primary_key=True)
    os_id = Column(ForeignKey('operating_system.os_id'), nullable=False, index=True)
    platform_id = Column(ForeignKey('platform.platform_id'), nullable=False, index=True)
    release_id = Column(ForeignKey('release.release_id'), nullable=False, index=True)

    os = relationship('OperatingSystem')
    platform = relationship('Platform')
    release = relationship('Release')


class Milestone(BASE, MatildaRlsBase):
    __tablename__ = 'milestone'
    __table_args__ = (
        Index('milestone_release_id_milestone_description_uindex', 'release_id', 'milestone_description', unique=True),
    )

    milestone_id = Column(Integer, primary_key=True)
    milestone_description = Column(String(250), nullable=False)
    milestone_status_cd = Column(ForeignKey('milestone_status_cd.milestone_status_cd'), index=True)
    start_dt = Column(DateTime)
    end_dt = Column(DateTime)
    percent_complete = Column(Integer, server_default=text("'0'"))
    release_id = Column(ForeignKey('release.release_id'))

    milestone_status_cd1 = relationship('MilestoneStatusCd')
    release = relationship('Release')


class MilestoneStatusCd(BASE, MatildaRlsBase):
    __tablename__ = 'milestone_status_cd'

    milestone_status_cd = Column(Integer, primary_key=True)
    milestone_status_description = Column(String(45), nullable=False)


class MilestoneTypeCd(BASE, MatildaRlsBase):
    __tablename__ = 'milestone_type_cd'

    milestone_type_cd = Column(Integer, primary_key=True)
    milestone_type_description = Column(String(100), nullable=False, unique=True)
    release_type_cd = Column(ForeignKey('release_type_cd.release_type_cd'), index=True)

    release_type_cd1 = relationship('ReleaseTypeCd')


class NewTable(BASE, MatildaRlsBase):
    __tablename__ = 'new_table'

    event_id = Column(Integer, primary_key=True)
    event_type = Column(String(45))
    source = Column(String(45))
    source_id = Column(String(45))
    time = Column(String(45))
    message = Column(String(45))
    status = Column(String(45))
    output = Column(String)


class OperatingSystem(BASE, MatildaRlsBase):
    __tablename__ = 'operating_system'

    os_id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    version = Column(String(45), nullable=False)
    status = Column(String(45), nullable=False)
    platform_id = Column(ForeignKey('platform.platform_id'), index=True)

    platform = relationship('Platform')


class OutputField(BASE, MatildaRlsBase):
    __tablename__ = 'output_fields'

    output_field_id = Column(Integer, primary_key=True)
    service_id = Column(ForeignKey('service.service_id'), nullable=False, index=True)
    action_id = Column(ForeignKey('actions.action_id'), nullable=False, index=True)
    fields = Column(Text)

    action = relationship('Action')
    service = relationship('Service')


class Platform(BASE, MatildaRlsBase):
    __tablename__ = 'platform'

    platform_id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    status = Column(String(45))


class Project(BASE, MatildaRlsBase):
    __tablename__ = 'project'

    project_id = Column(String(45), primary_key=True)
    name = Column(String(45), nullable=False)
    owner = Column(String(45))
    create_dt = Column(DateTime, nullable=False, default=datetime.datetime.now)
    status = Column(String(45), nullable=False)


class Release(BASE, MatildaRlsBase):
    __tablename__ = 'release'

    release_id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False, unique=True)
    release_plan_id = Column(ForeignKey('release_plan.release_plan_id'), ForeignKey('release_plan.release_plan_id'), nullable=False, index=True)
    create_dt = Column(DateTime, nullable=False)
    start_dt = Column(DateTime)
    complete_dt = Column(DateTime)
    release_dt = Column(DateTime)
    description = Column(Text)
    status_cd = Column(ForeignKey('status_cd.status_cd'), nullable=False, index=True, server_default=text("'1'"))
    release_type_cd = Column(ForeignKey('release_type_cd.release_type_cd'), nullable=False, index=True, server_default=text("'1'"))

    release_plan = relationship('ReleasePlan', primaryjoin='Release.release_plan_id == ReleasePlan.release_plan_id')
    release_type_cd1 = relationship('ReleaseTypeCd')
    status_cd1 = relationship('StatusCd')


class ReleaseCondition(BASE, MatildaRlsBase):
    __tablename__ = 'release_condition'

    rls_condition_id = Column(Integer, primary_key=True)
    release_id = Column(ForeignKey('release.release_id'), nullable=False, index=True)
    cond_field_id = Column(ForeignKey('condition_fields.cond_field_id'), nullable=False, index=True)
    parameter = Column(String(45), nullable=False)
    operator = Column(String(45), nullable=False)
    value = Column(String(45), nullable=False)
    ignore_failure = Column(String(45))
    importance = Column(Integer)
    status = Column(String(45), nullable=False)

    cond_field = relationship('ConditionField')
    release = relationship('Release')


class ReleaseLinkItem(BASE, MatildaRlsBase):
    __tablename__ = 'release_link_items'

    release_link_item_id = Column(Integer, primary_key=True)
    data = Column(JSON)
    release_link_id = Column(ForeignKey('release_links.release_link_id'), nullable=False, index=True)

    release_link = relationship('ReleaseLink')


class ReleaseLink(BASE, MatildaRlsBase):
    __tablename__ = 'release_links'

    release_link_id = Column(Integer, primary_key=True)
    name = Column(Text)
    url = Column(Text)
    source = Column(Text)
    description = Column(Text)
    release_id = Column(ForeignKey('release.release_id'), nullable=False, index=True)

    release = relationship('Release')


class ReleaseMilestone(BASE, MatildaRlsBase):
    __tablename__ = 'release_milestone'

    release_milestone_id = Column(Integer, primary_key=True)
    start_dt = Column(DateTime, nullable=False)
    create_dt = Column(DateTime, nullable=False, default=datetime.datetime.now)
    end_dt = Column(DateTime, nullable=False)
    description = Column(Text)
    release_type = Column(String(45), nullable=False)
    status_cd = Column(ForeignKey('milestone_status_cd.milestone_status_cd'), nullable=False, index=True)
    release_id = Column(ForeignKey('release.release_id'), nullable=False, index=True)
    rls_plan_milestone_id = Column(ForeignKey('release_plan_milestone.rls_plan_milestone_id'), nullable=False, index=True)

    release = relationship('Release')
    rls_plan_milestone = relationship('ReleasePlanMilestone')
    milestone_status_cd = relationship('MilestoneStatusCd')


class ReleasePlan(BASE, MatildaRlsBase):
    __tablename__ = 'release_plan'

    release_plan_id = Column(Integer, primary_key=True)
    release_type_cd = Column(ForeignKey('release_type_cd.release_type_cd'), nullable=False, index=True)
    release_plan_name = Column(String(250), nullable=False, unique=True)
    release_plan_description = Column(Text)
    release_owner = Column(String(100))
    create_dt = Column(DateTime, nullable=False)
    release_dt = Column(DateTime, nullable=False)

    release_type_cd1 = relationship('ReleaseTypeCd')


class ReleasePlanDoc(BASE, MatildaRlsBase):
    __tablename__ = 'release_plan_docs'

    rls_art_id = Column(Integer, primary_key=True)
    release_plan_id = Column(ForeignKey('release_plan.release_plan_id'), nullable=False, index=True)
    source = Column(Text, nullable=False)
    value = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    doc_type_id = Column(ForeignKey('document_types.doc_type_id'), nullable=False, index=True)

    doc_type = relationship('DocumentType')
    release_plan = relationship('ReleasePlan')


class ReleasePlanHistory(BASE, MatildaRlsBase):
    __tablename__ = 'release_plan_history'

    rls_history_id = Column(Integer, primary_key=True)
    activity = Column(Text, nullable=False)
    description = Column(Text)
    start_dt = Column(DateTime)
    end_dt = Column(DateTime, nullable=False)
    release_plan_id = Column(ForeignKey('release_plan.release_plan_id'), nullable=False, index=True)

    release_plan = relationship('ReleasePlan')


class ReleasePlanMilestone(BASE, MatildaRlsBase):
    __tablename__ = 'release_plan_milestone'

    rls_plan_milestone_id = Column(Integer, primary_key=True)
    start_dt = Column(DateTime, nullable=False)
    end_dt = Column(DateTime, nullable=False)
    description = Column(Text, nullable=False)
    release_plan_id = Column(ForeignKey('release_plan.release_plan_id'), nullable=False, index=True)
    milestone_id = Column(ForeignKey('milestone.milestone_id'), nullable=False, index=True)

    milestone = relationship('Milestone')
    release_plan = relationship('ReleasePlan')


class ReleaseTypeCd(BASE, MatildaRlsBase):
    __tablename__ = 'release_type_cd'

    release_type_cd = Column(Integer, primary_key=True)
    release_type_description = Column(String(100), unique=True)
    color_pref = Column(String(20), server_default=text("'#ffffff'"))

class Service(BASE, MatildaRlsBase):
    __tablename__ = 'service'

    service_id = Column(String(20), primary_key=True)
    name = Column(String(45), nullable=False, unique=True)
    category = Column(String(45), nullable=False)
    comments = Column(Text)


class ServiceActionOutputField(BASE, MatildaRlsBase):
    __tablename__ = 'service_action_output_fields'
    __table_args__ = (
        Index('service_action_output_fields_action_id_output_field_name_uindex', 'action_id', 'output_field_name', unique=True),
    )

    output_field_id = Column(String(30), primary_key=True)
    service_id = Column(ForeignKey('service.service_id'), nullable=False, index=True)
    action_id = Column(ForeignKey('actions.action_id'), nullable=False, index=True)
    output_field_name = Column(String(50))

    action = relationship('Action')
    service = relationship('Service')


class ServiceFields(BASE, MatildaRlsBase):
    __tablename__ = 'service_fields'
    __table_args__ = (
        Index('service_fields_service_id_action_id_key_uindex', 'service_id', 'action_id', 'key', unique=True),
    )

    service_field_id = Column(String(20), primary_key=True)
    key = Column(String(45), nullable=False)
    label = Column(String(45), nullable=False)
    placeholder = Column(String(255))
    control_type = Column(String(45))
    required = Column(String(45))
    order = Column(Integer)
    options = Column(Text)
    field_type = Column(String(45))
    description = Column(Text)
    service_id = Column(ForeignKey('service.service_id'), nullable=False, index=True)
    action_id = Column(ForeignKey('actions.action_id'), nullable=False, index=True)

    action = relationship('Action')
    service = relationship('Service')


class StageCondition(BASE, MatildaRlsBase):
    __tablename__ = 'stage_condition'

    stage_condition_id = Column(Integer, primary_key=True)
    stage_id = Column(ForeignKey('stages.stage_id'), nullable=False, index=True)
    cond_field_id = Column(ForeignKey('condition_fields.cond_field_id'), nullable=False, index=True)
    parameter = Column(String(45), nullable=False)
    operator = Column(String(45), nullable=False)
    value = Column(String(45), nullable=False)
    ignore_failure = Column(String(45))
    status = Column(String(45), nullable=False)
    importance = Column(Integer)

    cond_field = relationship('ConditionField')
    stage = relationship('Stage')


class Stage(BASE, MatildaRlsBase):
    __tablename__ = 'stages'

    stage_id = Column(Integer, primary_key=True)
    wf_id = Column(ForeignKey('workflow.wf_id'), nullable=False, index=True)
    name = Column(String(45), nullable=False)
    create_dt = Column(DateTime, nullable=False, default=datetime.datetime.now)
    planned_start_dt = Column(DateTime)
    actual_start_dt = Column(DateTime)
    planned_end_dt = Column(DateTime)
    actual_end_dt = Column(DateTime)
    order = Column(Integer, nullable=False)
    owner = Column(String(45))
    status_cd = Column(ForeignKey('status_cd.status_cd'), nullable=False, index=True, server_default=text("'1'"))
    stage_ui_id = Column(String(50))
    tasks = relationship('Task', backref=backref('stages', cascade='delete,all'))

    status_cd1 = relationship('StatusCd')


class StatusCd(BASE, MatildaRlsBase):
    __tablename__ = 'status_cd'
    __table_args__ = (
        Index('status_cd_status_cd_status_type_cd_status_description_uindex', 'status_cd', 'status_type_cd', 'status_description', unique=True),
    )

    status_cd = Column(Integer, primary_key=True)
    status_type_cd = Column(ForeignKey('status_type_cd.status_type_cd'), nullable=False, index=True)
    status_description = Column(String(100), nullable=False)
    order = Column(Integer, nullable=False)

    status_type_cd1 = relationship('StatusTypeCd')


class StatusTypeCd(BASE, MatildaRlsBase):
    __tablename__ = 'status_type_cd'

    status_type_cd = Column(Integer, primary_key=True)
    status_type_description = Column(String(100), unique=True)


class Task(BASE, MatildaRlsBase):
    __tablename__ = 'task'
    __table_args__ = (
        Index('task_wf_id_name_uindex', 'wf_id', 'name', unique=True),
    )

    task_id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    dag_task_name = Column(String(200), unique=True)
    create_dt = Column(DateTime, nullable=False, default=datetime.datetime.now)
    planned_start_dt = Column(DateTime)
    planned_end_dt = Column(DateTime)
    actual_start_dt = Column(DateTime)
    actual_end_dt = Column(DateTime)
    status_cd = Column(ForeignKey('status_cd.status_cd'), nullable=False, index=True, server_default=text("'1'"))
    owner = Column(String(45))
    order = Column(Integer, nullable=False)
    ignore_failure = Column(String(45))
    stage_id = Column(ForeignKey('stages.stage_id'), index=True)
    wf_id = Column(ForeignKey('workflow.wf_id'), nullable=False)
    task_group_id = Column(ForeignKey('task_group.task_group_id'), index=True)
    duration = Column(String(45))
    service_id = Column(ForeignKey('service.service_id'), nullable=False, index=True)
    action_id = Column(ForeignKey('actions.action_id'), nullable=False, index=True)
    input = Column(Text)
    output = Column(Text)
    task_ui_id = Column(String(50))

    action = relationship('Action')
    service = relationship('Service')
    status_cd1 = relationship('StatusCd')
    task_group = relationship('TaskGroup')
    wf = relationship('Workflow')


class TaskCondition(BASE, MatildaRlsBase):
    __tablename__ = 'task_condition'

    task_condition_id = Column(Integer, primary_key=True)
    parameter = Column(String(45), nullable=False)
    operator = Column(String(45), nullable=False)
    value = Column(String(45), nullable=False)
    status = Column(String(45), nullable=False)
    task_id = Column(ForeignKey('task.task_id'), nullable=False, index=True)
    cond_field_id = Column(ForeignKey('condition_fields.cond_field_id'), nullable=False, index=True)

    cond_field = relationship('ConditionField')
    task = relationship('Task')


class TaskGroup(BASE, MatildaRlsBase):
    __tablename__ = 'task_group'

    task_group_id = Column(Integer, primary_key=True)
    stage_id = Column(ForeignKey('stages.stage_id'), nullable=False, index=True)
    name = Column(String(45), nullable=False)
    create_dt = Column(DateTime, nullable=False, default=datetime.datetime.now)
    planned_start_dt = Column(DateTime, nullable=False)
    planned_end_dt = Column(DateTime)
    actual_start_dt = Column(DateTime)
    actual_end_dt = Column(DateTime)
    status = Column(String(45), nullable=False)

    stage = relationship('Stage')


class Template(BASE, MatildaRlsBase):
    __tablename__ = 'template'
    __table_args__ = (
        Index('unique_index', 'template_name', 'template_version', unique=True),
    )

    template_id = Column(Integer, primary_key=True)
    template_name = Column(String(100), nullable=False)
    template_version = Column(Integer, nullable=False)
    template_json = Column(JSON, nullable=False)


class VnfNodeType(BASE, MatildaRlsBase):
    __tablename__ = 'vnf_node_type'

    vnf_node_id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    status = Column(String(45))


class VnfRelease(BASE, MatildaRlsBase):
    __tablename__ = 'vnf_release'

    vnf_release_id = Column(Integer, primary_key=True)
    vnf_node_id = Column(ForeignKey('vnf_node_type.vnf_node_id'), nullable=False, index=True)
    vnf_site_id = Column(ForeignKey('vnf_sites.vnf_site_id'), nullable=False, index=True)
    release_id = Column(ForeignKey('release.release_id'), nullable=False, index=True)

    release = relationship('Release')
    vnf_node = relationship('VnfNodeType')
    vnf_site = relationship('VnfSite')


class VnfSite(BASE, MatildaRlsBase):
    __tablename__ = 'vnf_sites'

    vnf_site_id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    status = Column(String(45), nullable=False)
    vnf_node_id = Column(ForeignKey('vnf_node_type.vnf_node_id'), index=True)

    vnf_node = relationship('VnfNodeType')


class Workflow(BASE, MatildaRlsBase):
    __tablename__ = 'workflow'

    wf_id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    create_dt = Column(DateTime, nullable=False, default=datetime.datetime.now)
    planned_start_dt = Column(DateTime)
    actual_start_dt = Column(DateTime)
    planned_end_dt = Column(DateTime)
    actual_end_dt = Column(DateTime)
    status_cd = Column(ForeignKey('status_cd.status_cd'), nullable=False, index=True, server_default=text("'1'"))
    owner = Column(String(45), nullable=False)
    order = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    ignore_failure = Column(String(45), nullable=False)
    template_id = Column(Integer)
    env_id = Column(ForeignKey('environment.env_id'), nullable=False, index=True)
    frequency_cd = Column(ForeignKey('frequency.frequency_cd'), index=True, server_default=text("'1'"))
    dag_name = Column(String(150), unique=True)
    stages = relationship('Stage', backref=backref('workflow', cascade='delete,all'))

    env = relationship('Environment')
    frequency = relationship('Frequency')
    status_cd1 = relationship('StatusCd')


class WorkflowCondition(BASE, MatildaRlsBase):
    __tablename__ = 'workflow_condition'

    wf_condition_id = Column(Integer, primary_key=True)
    wf_id = Column(ForeignKey('workflow.wf_id'), nullable=False, index=True)
    cond_field_id = Column(ForeignKey('condition_fields.cond_field_id'), nullable=False, index=True)
    parameter = Column(String(45), nullable=False)
    operator = Column(String(45), nullable=False)
    value = Column(String(45), nullable=False)
    ignore_failure = Column(String(45))
    importance = Column(Integer)
    status = Column(String(45), nullable=False)

    cond_field = relationship('ConditionField')
    wf = relationship('Workflow')

class InfraMetricsCategory(BASE, MatildaRlsBase):
    __tablename__ = 'infra_metrics_category'

    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(45), nullable=False)

class InfraMetricsComponent(BASE, MatildaRlsBase):
    __tablename__ = 'infra_metrics_component'

    component_id = Column(Integer, primary_key=True)
    component_name = Column(String(45), nullable=False)

class InfraMetricsSubComponent(BASE, MatildaRlsBase):
    __tablename__ = 'infra_metrics_subcomponent'

    subcomponent_id = Column(Integer, primary_key=True)
    subcomponent_name = Column(String(45), nullable=False)

class InfraMetrics(BASE, MatildaRlsBase):
    __tablename__ = 'infra_metrics'

    component_id = Column(ForeignKey('infra_metrics_component.component_id'), primary_key=True)
    category_id = Column(ForeignKey('infra_metrics_category.category_id'), primary_key=True)
    subcomponent_id = Column(ForeignKey('infra_metrics_subcomponent.subcomponent_id'), primary_key=True)
    date = Column(Date, primary_key=True)
    metrics = Column(Integer, nullable=False)
    category = relationship('InfraMetricsCategory')
    subcomponent = relationship('InfraMetricsSubComponent')
    component = relationship('InfraMetricsComponent')

class InfraReleaseImpactedApplications(BASE, MatildaRlsBase):
    __tablename__ = 'infra_release_impacted_applications'

    impacted_application_id = Column(Integer, primary_key=True)
    release_id = Column(ForeignKey('release.release_id'))
    computer_system_name = Column(String(250), nullable=False)
    application_name = Column(String(250), nullable=False)
    environment = Column(String(20), nullable=False)
    platform = Column(String(100), nullable=False)
    platform_from_excel = Column(String(250))
    operating_system = Column(String(100), nullable=False)
    test_type_prod = Column(String(150))
    test_type_non_prod = Column(String(150))
    app_owner_name = Column(String(100))
    tester_name = Column(String(100))
    test_folder_name = Column(String(250), nullable=False)
    test_set_or_folder = Column(String(100), nullable=False)
    opt_out = Column(Integer)
    release = relationship('Release')


class MasterApplications(BASE, MatildaRlsBase):
    __tablename__ = 'master_applications'

    master_application_id = Column(Integer, primary_key=True)
    computer_system_name = Column(String(250), nullable=False)
    application_name = Column(String(250), nullable=False)
    environment = Column(String(20), nullable=False)
    platform = Column(String(100), nullable=False)
    platform_from_excel = Column(String(250))
    operating_system = Column(String(100), nullable=False)
    test_type_prod = Column(String(150))
    test_type_non_prod = Column(String(150))
    app_owner_name = Column(String(100))
    tester_name = Column(String(100))
    test_set_or_folder = Column(String(100), nullable=False)