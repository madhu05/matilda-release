use release_management;

create table app_metrics_category
(
  category_id   int auto_increment
    primary key,
  category_name varchar(45) not null
);

create table app_metrics_component
(
  component_id   int auto_increment
    primary key,
  component_name varchar(45) not null
);

create table app_metrics_subcomponent
(
  subcomponent_id   int auto_increment
    primary key,
  subcomponent_name varchar(45) not null
);

create table app_metrics
(
  component_id    int  not null,
  subcomponent_id int  not null,
  category_id     int  not null,
  date            date not null,
  metrics         int  not null,
  primary key (component_id, subcomponent_id, category_id, date),
  constraint fk_app_metrics_1
    foreign key (component_id) references app_metrics_component (component_id),
  constraint fk_app_metrics_2
    foreign key (subcomponent_id) references app_metrics_subcomponent (subcomponent_id),
  constraint fk_app_metrics_3
    foreign key (category_id) references app_metrics_category (category_id)
);

create index fk_app_metrics_2_idx
  on app_metrics (subcomponent_id);

create index fk_app_metrics_3_idx
  on app_metrics (category_id);

create table condition_fields
(
  cond_field_id int auto_increment
    primary key,
  type          varchar(45) not null,
  field_name    varchar(45) not null,release_plan_info
  `order`       int         not null
);

create table datatype
(
  datatype_id int auto_increment
    primary key,
  datatype    varchar(45) not null
);

create table document_types
(
  doc_type_id int auto_increment
    primary key,
  name        varchar(45) not null,
  type        varchar(45) not null,
  description text        null,
  value       text        null
);

create table env_type_cd
(
  env_type_cd          int auto_increment
    primary key,
  env_type_description varchar(100) not null,
  constraint env_type_cd_env_type_description_uindex
    unique (env_type_description)
);

create table frequency
(
  frequency_cd          int auto_increment
    primary key,
  frequency_description varchar(50)  not null,
  dag_usage             varchar(50)  not null,
  comments              varchar(200) null,
  cron_expression       varchar(50)  null,
  constraint frequency_description_uindex
    unique (frequency_description)
);

create table infra_metrics_category
(
  category_id   int auto_increment
    primary key,
  category_name varchar(45) not null
);

create table infra_metrics_component
(
  component_id   int auto_increment
    primary key,
  component_name varchar(45) not null
);

create table infra_metrics_subcomponent
(
  subcomponent_id   int auto_increment
    primary key,
  subcomponent_name varchar(45) not null
);

create table infra_metrics
(
  component_id    int  not null,
  subcomponent_id int  not null,
  category_id     int  not null,
  date            date not null,
  metrics         int  not null,
  primary key (component_id, subcomponent_id, category_id, date),
  constraint fk_infra_metrics_1
    foreign key (component_id) references infra_metrics_component (component_id),
  constraint fk_infra_metrics_2
    foreign key (subcomponent_id) references infra_metrics_subcomponent (subcomponent_id),
  constraint fk_infra_metrics_3
    foreign key (category_id) references infra_metrics_category (category_id)
);

create index fk_infra_metrics_2_idx
  on infra_metrics (subcomponent_id);

create index fk_infra_metrics_3_idx
  on infra_metrics (category_id);

create table master_applications
(
  master_application_id int auto_increment
    primary key,
  computer_system_name  varchar(250) not null,
  application_name      varchar(250) not null,
  environment           varchar(20)  not null,
  platform              varchar(100) not null,
  platform_from_excel   varchar(250) null,
  operating_system      varchar(100) not null,
  test_type_prod        varchar(150) null,
  test_type_non_prod    varchar(150) null,
  app_owner_name        varchar(100) null,
  tester_name           varchar(100) null,
  test_set_or_folder    varchar(100) not null
);

create table milestone_status_cd
(
  milestone_status_cd          int auto_increment
    primary key,
  milestone_status_description varchar(45) not null
);

create table new_table
(
  event_id   int auto_increment
    primary key,
  event_type varchar(45) null,
  source     varchar(45) null,
  source_id  varchar(45) null,
  time       varchar(45) null,
  message    varchar(45) null,
  status     varchar(45) null,
  output     mediumtext  null
);

create table platform
(
  platform_id int auto_increment
    primary key,
  name        varchar(45) not null,
  status      varchar(45) null
);

create table operating_system
(
  os_id       int auto_increment
    primary key,
  name        varchar(45) not null,
  version     varchar(45) not null,
  status      varchar(45) not null,
  platform_id int         null,
  constraint operating_system_fk
    foreign key (platform_id) references platform (platform_id)
);

create table project
(
  project_id varchar(45) not null
    primary key,
  name       varchar(45) not null,
  owner      varchar(45) null,
  create_dt  datetime    not null,
  status     varchar(45) not null
);

create table application
(
  app_id     varchar(45) not null
    primary key,
  owner      varchar(45) not null,
  create_dt  datetime    not null,
  status     varchar(45) not null,
  project_id varchar(45) not null,
  constraint FK_177
    foreign key (project_id) references project (project_id)
);

create index fkIdx_177
  on application (project_id);

create table release_type_cd
(
  release_type_cd          int                           not null
    primary key,
  release_type_description varchar(100)                  null,
  color_pref               varchar(20) default '#ffffff' null,
  constraint release_type_cd_release_type_description_uindex
    unique (release_type_description)
);

create table milestone_type_cd
(
  milestone_type_cd          int auto_increment
    primary key,
  milestone_type_description varchar(100) not null,
  release_type_cd            int          null,
  constraint milestone_type_milestone_type_description_uindex
    unique (milestone_type_description),
  constraint milestone_type_release_type_cd_release_type_cd_fk
    foreign key (release_type_cd) references release_type_cd (release_type_cd)
);

create table release_plan
(
  release_plan_id          int auto_increment
    primary key,
  release_type_cd          int          not null,
  release_plan_name        varchar(250) not null,
  release_plan_description text         null,
  release_owner            varchar(100) null,
  create_dt                datetime     not null,
  release_dt               datetime     not null,
  constraint release_plan_release_plan_name_uindex
    unique (release_plan_name),
  constraint release_plan_release_type_cd_release_type_cd_fk
    foreign key (release_type_cd) references release_type_cd (release_type_cd)
);

create table release_plan_docs
(
  rls_art_id      int  not null
    primary key,
  release_plan_id int  not null,
  source          text not null,
  value           text not null,
  description     text not null,
  doc_type_id     int  not null,
  constraint FK_40
    foreign key (release_plan_id) references release_plan (release_plan_id),
  constraint FK_57
    foreign key (doc_type_id) references document_types (doc_type_id)
);

create index fkIdx_40
  on release_plan_docs (release_plan_id);

create index fkIdx_57
  on release_plan_docs (doc_type_id);

create table release_plan_history
(
  rls_history_id  int auto_increment
    primary key,
  activity        text     not null,
  description     text     null,
  start_dt        datetime null,
  end_dt          datetime not null,
  release_plan_id int      not null,
  constraint FK_45
    foreign key (release_plan_id) references release_plan (release_plan_id)
);

create index fkIdx_45
  on release_plan_history (release_plan_id);

create table service
(
  service_id varchar(20) not null
    primary key,
  name       varchar(45) not null,
  category   varchar(45) not null,
  comments   text        null,
  constraint service_name_uindex
    unique (name)
);

create table actions
(
  action_id   varchar(20) not null
    primary key,
  name        varchar(45) not null,
  description text        null,
  service_id  varchar(20) not null,
  constraint actions_service_id_name_uindex
    unique (service_id, name),
  constraint FK_491
    foreign key (service_id) references service (service_id)
);

create table action_fields
(
  action_field_id int auto_increment
    primary key,
  field           varchar(45) not null,
  type            varchar(45) not null,
  options         text        not null,
  mandatory       varchar(45) not null,
  datatype_id     int         not null,
  action_id       varchar(20) not null,
  constraint FK_508
    foreign key (datatype_id) references datatype (datatype_id),
  constraint FK_512
    foreign key (action_id) references actions (action_id)
);

create index fkIdx_508
  on action_fields (datatype_id);

create index fkIdx_512
  on action_fields (action_id);

create index fkIdx_491
  on actions (service_id);

create table output_fields
(
  output_field_id int auto_increment
    primary key,
  service_id      varchar(20) not null,
  action_id       varchar(20) not null,
  fields          text        null,
  constraint FK_514a
    foreign key (service_id) references service (service_id),
  constraint FK_517a
    foreign key (action_id) references actions (action_id)
);

create index fkIdx_514a
  on output_fields (service_id);

create index fkIdx_517a
  on output_fields (action_id);

create table service_action_output_fields
(
  output_field_id   varchar(30) not null
    primary key,
  service_id        varchar(20) not null,
  action_id         varchar(20) not null,
  output_field_name varchar(50) null,
  constraint service_action_output_fields_action_id_output_field_name_uindex
    unique (action_id, output_field_name),
  constraint FK_483a
    foreign key (service_id) references service (service_id),
  constraint FK_487a
    foreign key (action_id) references actions (action_id)
);

create index fkIdx_483a
  on service_action_output_fields (service_id);

create index fkIdx_487a
  on service_action_output_fields (action_id);

create table service_fields
(
  service_field_id varchar(20)  not null
    primary key,
  `key`            varchar(45)  not null,
  label            varchar(45)  not null,
  placeholder      varchar(255) null,
  control_type     varchar(45)  null,
  required         varchar(45)  null,
  `order`          int          null,
  options          text         null,
  field_type       varchar(45)  null,
  description      text         null,
  service_id       varchar(20)  not null,
  action_id        varchar(20)  not null,
  constraint service_fields_service_id_action_id_key_uindex
    unique (service_id, action_id, `key`),
  constraint FK_93a
    foreign key (service_id) references service (service_id),
  constraint FK_97a
    foreign key (action_id) references actions (action_id)
);

create index fkIdx_93a
  on service_fields (service_id);

create index fkIdx_97a
  on service_fields (action_id);

create table status_type_cd
(
  status_type_cd          int auto_increment
    primary key,
  status_type_description varchar(100) null,
  constraint status_type_cd_status_type_description_uindex
    unique (status_type_description)
);

create table status_cd
(
  status_cd          int          not null
    primary key,
  status_type_cd     int          not null,
  status_description varchar(100) not null,
  `order`            int          not null,
  constraint status_cd_status_cd_status_type_cd_status_description_uindex
    unique (status_cd, status_type_cd, status_description),
  constraint status_cd_status_type_cd_status_type_cd_fk
    foreign key (status_type_cd) references status_type_cd (status_type_cd)
);

create table `release`
(
  release_id      integer auto_increment primary key,
  name            varchar(45)   not null,
  release_plan_id int           not null,
  create_dt       datetime      not null,
  start_dt        datetime      null,
  complete_dt     datetime      null,
  release_dt      datetime      null,
  description     text          null,
  status_cd       int default 1 not null,
  release_type_cd int default 1 not null,
  constraint release_name_uindex
    unique (name),
  constraint FK_274
    foreign key (release_plan_id) references release_plan (release_plan_id),
  constraint release_release_type_cd_release_type_cd_fk
    foreign key (release_type_cd) references release_type_cd (release_type_cd),
  constraint release_status_cd_status_cd_fk
    foreign key (status_cd) references status_cd (status_cd)
);

create table app_release_info
(
  app_release_id int auto_increment
    primary key,
  application    varchar(45) null,
  project        varchar(45) null,
  portfolio      varchar(45) null,
  project_id     varchar(45) not null,
  application_id varchar(45) not null,
  release_id     int         not null,
  constraint FK_181
    foreign key (project_id) references project (project_id),
  constraint FK_185
    foreign key (application_id) references application (app_id),
  constraint FK_280
    foreign key (release_id) references `release` (release_id)
);

create index fkIdx_181
  on app_release_info (project_id);

create index fkIdx_185
  on app_release_info (application_id);

create index fkIdx_280
  on app_release_info (release_id);

create table environment
(
  env_id      Int PRIMARY KEY AUTOINCREMENT,
  name        varchar(45)   not null,
  env_type_cd int default 1 not null,
  start_dt    datetime      null,
  create_dt   datetime      null,
  end_dt      datetime      null,
  status_cd   int default 1 not null,
  release_id  int           not null,
  constraint environment_release_id_name_uindex
    unique (release_id, name),
  constraint FK_324
    foreign key (release_id) references `release` (release_id),
  constraint environment_env_type_cd_env_type_cd_fk
    foreign key (env_type_cd) references env_type_cd (env_type_cd),
  constraint environment_status_cd_status_cd_fk
    foreign key (status_cd) references status_cd (status_cd)
);

create table env_activity
(
  env_activity_id int auto_increment
    primary key,
  env_id          int      not null,
  activity        text     not null,
  create_dt       datetime not null,
  constraint FK_349
    foreign key (env_id) references environment (env_id)
);

create index fkIdx_349
  on env_activity (env_id);

create table env_condition
(
  env_condition_id int auto_increment
    primary key,
  env_id           int         not null,
  cond_field_id    int         not null,
  parameter        varchar(45) not null,
  operator         varchar(45) not null,
  value            varchar(45) not null,
  ignore_failure   varchar(45) null,
  importance       int         null,
  status           varchar(45) not null,
  constraint FK_332
    foreign key (env_id) references environment (env_id),
  constraint FK_336
    foreign key (cond_field_id) references condition_fields (cond_field_id)
);

create index fkIdx_332
  on env_condition (env_id);

create index fkIdx_336
  on env_condition (cond_field_id);

create index fkIdx_324
  on environment (release_id);

create table infra_release
(
  infra_release_id int auto_increment
    primary key,
  os_id            int null,
  platform_id      int not null,
  release_id       int not null,
  constraint FK_141
    foreign key (os_id) references operating_system (os_id),
  constraint FK_149
    foreign key (platform_id) references platform (platform_id),
  constraint FK_284
    foreign key (release_id) references `release` (release_id)
);

create index fkIdx_141
  on infra_release (os_id);

create index fkIdx_149
  on infra_release (platform_id);

create index fkIdx_284
  on infra_release (release_id);

create table infra_release_impacted_applications
(
  impacted_application_id int auto_increment
    primary key,
  release_id              int                  not null,
  computer_system_name    varchar(250)         not null,
  application_name        varchar(250)         not null,
  environment             varchar(20)          not null,
  platform                varchar(100)         not null,
  platform_from_excel     varchar(250)         null,
  operating_system        varchar(100)         not null,
  test_type_prod          varchar(150)         null,
  test_type_non_prod      varchar(150)         null,
  app_owner_name          varchar(100)         null,
  tester_name             varchar(100)         null,
  test_folder_name        varchar(250)         not null,
  test_set_or_folder      varchar(100)         not null,
  opt_out                 tinyint(1) default 0 null,
  constraint infra_release_impacted_applications_release_release_id_fk
    foreign key (release_id) references `release` (release_id)
);

create table milestone
(
  milestone_id          int auto_increment
    primary key,
  milestone_description varchar(250)             not null,
  milestone_status_cd   int                      null,
  start_dt              datetime                 null,
  end_dt                datetime                 null,
  percent_complete      float(3, 2) default 0.00 null,
  release_id            int                      null,
  constraint milestone_release_id_milestone_description_uindex
    unique (release_id, milestone_description),
  constraint milestone_milestone_status_cd_status_cd_fk
    foreign key (milestone_status_cd) references milestone_status_cd (milestone_status_cd),
  constraint milestone_release_release_id_fk
    foreign key (release_id) references `release` (release_id)
);

create index fkIdx_274
  on `release` (release_plan_id);

create table release_condition
(
  rls_condition_id int auto_increment
    primary key,
  release_id       int         not null,
  cond_field_id    int         not null,
  parameter        varchar(45) not null,
  operator         varchar(45) not null,
  value            varchar(45) not null,
  ignore_failure   varchar(45) null,
  importance       int         null,
  status           varchar(45) not null,
  constraint FK_297
    foreign key (release_id) references `release` (release_id),
  constraint FK_301
    foreign key (cond_field_id) references condition_fields (cond_field_id)
);

create index fkIdx_297
  on release_condition (release_id);

create index fkIdx_301
  on release_condition (cond_field_id);

create table release_links
(
  release_link_id int auto_increment
    primary key,
  name            text null,
  url             text null,
  source          text null,
  description     text null,
  release_id      int  not null,
  constraint FK_288
    foreign key (release_id) references `release` (release_id)
);

create table release_link_items
(
  release_link_item_id int auto_increment
    primary key,
  data                 json null,
  release_link_id      int  not null,
  constraint FK_288a
    foreign key (release_link_id) references release_links (release_link_id)
);

create index fkIdx_288a
  on release_link_items (release_link_id);

create index fkIdx_288
  on release_links (release_id);

create table release_plan_milestone
(
  rls_plan_milestone_id int auto_increment
    primary key,
  start_dt              datetime not null,
  end_dt                datetime not null,
  description           text     not null,
  release_plan_id       int      not null,
  milestone_id          int      not null,
  constraint FK_93
    foreign key (release_plan_id) references release_plan (release_plan_id),
  constraint FK_97
    foreign key (milestone_id) references milestone (milestone_id)
);

create table release_milestone
(
  release_milestone_id  int auto_increment
    primary key,
  start_dt              datetime    not null,
  create_dt             datetime    not null,
  end_dt                datetime    not null,
  description           text        null,
  release_type          varchar(45) not null,
  status_cd             int         not null,
  release_id            int         not null,
  rls_plan_milestone_id int         not null,
  constraint FK_223
    foreign key (rls_plan_milestone_id) references release_plan_milestone (rls_plan_milestone_id),
  constraint FK_246
    foreign key (status_cd) references milestone_status_cd (milestone_status_cd),
  constraint FK_292
    foreign key (release_id) references `release` (release_id)
);

create index fkIdx_223
  on release_milestone (rls_plan_milestone_id);

create index fkIdx_246
  on release_milestone (status_cd);

create index fkIdx_292
  on release_milestone (release_id);

create index fkIdx_93
  on release_plan_milestone (release_plan_id);

create index fkIdx_97
  on release_plan_milestone (milestone_id);

create table template
(
  template_id      int auto_increment
    primary key,
  template_name    varchar(100) not null,
  template_version int          not null,
  template_json    json         not null,
  constraint unique_index
    unique (template_name, template_version)
);

create table vnf_node_type
(
  vnf_node_id int auto_increment
    primary key,
  name        varchar(45) not null,
  status      varchar(45) null
);

create table vnf_sites
(
  vnf_site_id int auto_increment
    primary key,
  name        varchar(45) not null,
  status      varchar(45) not null,
  vnf_node_id int         null,
  constraint vnf_site_fk
    foreign key (vnf_node_id) references vnf_node_type (vnf_node_id)
);

create table vnf_release
(
  vnf_release_id int auto_increment
    primary key,
  vnf_node_id    int not null,
  vnf_site_id    int not null,
  release_id     int not null,
  constraint release_fk
    foreign key (release_id) references `release` (release_id),
  constraint vnf_node_fk
    foreign key (vnf_node_id) references vnf_node_type (vnf_node_id),
  constraint vnf_sites_fk
    foreign key (vnf_site_id) references vnf_sites (vnf_site_id)
);

create table workflow
(
  wf_id            int auto_increment
    primary key,
  name             varchar(45)   not null,
  create_dt        datetime      not null,
  planned_start_dt datetime      null,
  actual_start_dt  datetime      null,
  planned_end_dt   datetime      null,
  actual_end_dt    datetime      null,
  status_cd        int default 1 not null,
  owner            varchar(45)   not null,
  `order`          int           not null,
  description      text          not null,
  ignore_failure   varchar(45)   not null,
  template_id      int           null,
  env_id           int           not null,
  frequency_cd     int default 1 null,
  dag_name         varchar(150)  null,
  constraint workflow_dag_name_uindex
    unique (dag_name),
  constraint FK_371
    foreign key (env_id) references environment (env_id),
  constraint workflow_frequency_frequency_cd_fk
    foreign key (frequency_cd) references frequency (frequency_cd),
  constraint workflow_status_cd_status_cd_fk
    foreign key (status_cd) references status_cd (status_cd)
);

create table stages
(
  stage_id         int auto_increment
    primary key,
  wf_id            int           not null,
  name             varchar(45)   not null,
  create_dt        datetime      not null,
  planned_start_dt datetime      null,
  actual_start_dt  datetime      null,
  planned_end_dt   datetime      null,
  actual_end_dt    datetime      null,
  `order`          int           not null,
  owner            varchar(45)   null,
  status_cd        int default 1 not null,
  stage_ui_id      varchar(50)   null,
  constraint FK_396
    foreign key (wf_id) references workflow (wf_id),
  constraint stages_status_cd_status_cd_fk
    foreign key (status_cd) references status_cd (status_cd)
);

create table stage_condition
(
  stage_condition_id int auto_increment
    primary key,
  stage_id           int         not null,
  cond_field_id      int         not null,
  parameter          varchar(45) not null,
  operator           varchar(45) not null,
  value              varchar(45) not null,
  ignore_failure     varchar(45) null,
  status             varchar(45) not null,
  importance         int         null,
  constraint FK_413
    foreign key (stage_id) references stages (stage_id),
  constraint FK_417
    foreign key (cond_field_id) references condition_fields (cond_field_id)
);

create index fkIdx_413
  on stage_condition (stage_id);

create index fkIdx_417
  on stage_condition (cond_field_id);

create index fkIdx_396
  on stages (wf_id);

create table task_group
(
  task_group_id    int auto_increment
    primary key,
  stage_id         int         not null,
  name             varchar(45) not null,
  create_dt        datetime    not null,
  planned_start_dt datetime    not null,
  planned_end_dt   datetime    null,
  actual_start_dt  datetime    null,
  actual_end_dt    datetime    null,
  status           varchar(45) not null,
  constraint FK_434
    foreign key (stage_id) references stages (stage_id)
);

create table task
(
  task_id          int auto_increment
    primary key,
  name             varchar(45)   not null,
  dag_task_name    varchar(200)  null,
  create_dt        datetime      not null,
  planned_start_dt datetime      null,
  planned_end_dt   datetime      null,
  actual_start_dt  datetime      null,
  actual_end_dt    datetime      null,
  status_cd        int default 1 not null,
  owner            varchar(45)   null,
  `order`          int           not null,
  ignore_failure   varchar(45)   null,
  stage_id         int           null,
  wf_id            int           not null,
  task_group_id    int           null,
  duration         varchar(45)   null,
  service_id       varchar(20)   not null,
  action_id        varchar(20)   not null,
  input            text          null,
  output           text          null,
  task_ui_id       varchar(50)   null,
  constraint task_dag_task_name_uindex
    unique (dag_task_name),
  constraint task_wf_id_name_uindex
    unique (wf_id, name),
  constraint FK_462
    foreign key (stage_id) references stages (stage_id),
  constraint FK_466
    foreign key (task_group_id) references task_group (task_group_id),
  constraint FK_483
    foreign key (service_id) references service (service_id),
  constraint FK_487
    foreign key (action_id) references actions (action_id),
  constraint task_status_cd_status_cd_fk
    foreign key (status_cd) references status_cd (status_cd),
  constraint task_workflow_wf_id_fk
    foreign key (wf_id) references workflow (wf_id)
);

create index fkIdx_462
  on task (stage_id);

create index fkIdx_466
  on task (task_group_id);

create index fkIdx_483
  on task (service_id);

create index fkIdx_487
  on task (action_id);

create table task_condition
(
  task_condition_id int auto_increment
    primary key,
  parameter         varchar(45) not null,
  operator          varchar(45) not null,
  value             varchar(45) not null,
  status            varchar(45) not null,
  task_id           int         not null,
  cond_field_id     int         not null,
  constraint FK_526
    foreign key (task_id) references task (task_id),
  constraint FK_530
    foreign key (cond_field_id) references condition_fields (cond_field_id)
);

create index fkIdx_526
  on task_condition (task_id);

create index fkIdx_530
  on task_condition (cond_field_id);

create index fkIdx_434
  on task_group (stage_id);

create index fkIdx_371
  on workflow (env_id);

create table workflow_condition
(
  wf_condition_id int auto_increment
    primary key,
  wf_id           int         not null,
  cond_field_id   int         not null,
  parameter       varchar(45) not null,
  operator        varchar(45) not null,
  value           varchar(45) not null,
  ignore_failure  varchar(45) null,
  importance      int         null,
  status          varchar(45) not null,
  constraint FK_379
    foreign key (wf_id) references workflow (wf_id),
  constraint FK_383
    foreign key (cond_field_id) references condition_fields (cond_field_id)
);

create index fkIdx_379
  on workflow_condition (wf_id);

create index fkIdx_383
  on workflow_condition (cond_field_id);

