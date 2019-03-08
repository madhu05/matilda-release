MOCK_PROJECT = {
  "owner": "mock_owner",
  "status": "Active",
  "project_id": "MOCK_P",
  "name": "Mock Project"
}

MOCK_APPLICATION = {
  "status": "Active",
  "name": "Mock Application",
  "app_id": "MOCK_A",
  "owner": "mock_owner",
  "project_id": "MOCK_P"
}

MOCK_SERVICE = {

}

MOCK_ACTION = {

}

MOCK_APP_RELEASE = {
  "release_type_description": "Mock Release",
  "project_id": "MOCK_P",
  "release_id": 0,
  "application_id": "MOCK_A",
  "application_name": "Mock Application",
  "status_cd": 0,
  "name": "Mock Release",
  "project_name": "Mock Project",
  "version": "1.0",
  "release_dt": "2019-01-27T14:35:29.300Z",
  "status_description": "Status",
  "platform_name": "string",
  "release_type_cd": 0,
  "description": "string"
}

MOCK_ENVIRONMENT1 = {
  "status_cd": 0,
  "release_id": 1,
  "name": "mock-dev1",
  "env_type_description": "string",
  "status_description": "string",
  "release": "string",
  "env_id": 0,
  "start_dt": "2019-01-27 14:48:37",
  "end_dt": "2019-01-27 14:48:37.823",
  "env_type_cd": 0
}

MOCK_WORKFLOW = {
    "wf_id": 0,
    "status_cd": 0,
    "dag_name": "string",
    "release_id": 0,
    "description": "string",
    "frequency_description": "string",
    "environment_name": "string",
    "frequency_cd": 0,
    "overall_progress": 0,
    "release": "string",
    "env_id": 0,
    "status_description": "string",
    "template_id": 0,
    "name": "string"
}

MOCK_STAGE = {
    "status_cd": 0,
    "description": "string",
    "stage_ui_id": "string",
    "actual_end_dt": "",
    "stage_id": 0,
    "workflow_id": 0,
    "planned_start_dt": "",
    "planned_end_dt": "",
    "owner": "string",
    "actual_start_dt": "",
    "status_description": "string",
    "order": 0,
    "name": "string"
  }

MOCK_TASK = {
    "service_name": "string",
    "actual_end_dt": "",
    "duration": "string",
    "owner": "string",
    "planned_end_dt": "",
    "task_ui_id": "string",
    "task_group_id": 0,
    "create_dt": "",
    "actual_start_dt": "",
    "action_id": "sv1_ac1",
    "action_name": "string",
    "planned_start_dt": "",
    "input": {},
    "status_description": "string",
    "wf_id": 0,
    "status_cd": 0,
    "stage_id": 0,
    "name": "string",
    "task_id": 0,
    "ignore_failure": "string",
    "dag_task_name": "string",
    "output": {},
    "service_id": "sv1"
  }

def get_project():
    return MOCK_PROJECT

def get_application():
    return MOCK_APPLICATION

def get_mock_release(rls_type='app'):
    if rls_type == 'app':
        return MOCK_APP_RELEASE

def get_mock_environment(release_id=1):
    if release_id != 1:
        MOCK_ENVIRONMENT1['release_id'] = release_id
    return MOCK_ENVIRONMENT1

def get_workflow(env_id=1):
    stage_list = []
    for i in range(2):
        stage = MOCK_STAGE
        stage['name'] = MOCK_STAGE['name'] + str(i)
        task_list = []
        for j in range(5):
            task = MOCK_TASK
            task['name'] = MOCK_TASK['name'] + + str(i) + str(j)
            task_list.append(task)
        stage['tasks'] = task_list
        stage_list.append(stage)
    wf = MOCK_WORKFLOW
    wf['stages'] = stage_list
    return wf
