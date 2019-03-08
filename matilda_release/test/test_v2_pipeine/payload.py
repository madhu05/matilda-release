import json,datetime


def project_payload():
    project_data = {
        "project_id": "global",
        "name": "global",
        "owner": "global",
        "create_dt": "2019-02-14T16:51:47.704Z",
        "status": "Non-Active"}
    return project_data


def application_payload():
    application_data = {"app_id": "global",
                        "owner": "global",
                        "create_dt":"2019-02-14T16:51:47.704Z",
                        "status": "Active",
                        "name": "global",
                        "project_id": "global"}
    return application_data


def release_plan():
    release_plan_data = { "release_plan_id": 1,
                          "release_type_cd": 1,
                          "color_pref": "#32c5e9",
                          "release_plan_name": "global",
                          "release_plan_description": "string",
                          "release_owner": "Rajesh",
                          "create_dt": "2019-02-14T16:51:47.702Z",
                          "release_dt": "2019-02-14T22:51:04.702Z"}
    return release_plan_data


def release_payload():
    release_data = {
        "release_id": 1,
        "name": "global",
        "release_dt": "2019-02-13T19:44:30.221Z",
        "project_id": "global",
        "project_name": "global",
        "application_id": "global",
        "application_name": "global",
        "os_id": 1,
        "os_name": "string",
        "platform_id": 1,
        "platform_name": "string",
        "vnf_site": "string",
        "vnf_node": "string",
        "release_type_cd": 1,
        "release_type_description": "string",
        "status_cd": 1,
        "status_description": "string",
        "duration": "string",
        "description": "string",
        "release_plan_id": 1,
        "release_plan_name": "global"}
    return release_data


def env_payload():
    env_data = {"env_id": 1,
                "name": "global",
                "env_type_cd": 1,
                "env_type_description": "Development",
                "create_dt": "2019-01-31T01:11:10.200Z",
                "start_dt": "2019-01-31T01:11:10.200Z",
                "end_dt": "2019-01-31T01:11:10.200Z",
                "status_cd": 1,
                "status_description": "Defined",
                "release_id": 1,
                "release": "global"}
    return env_data


def workflow_payload():
    workflow_data = {
        "name": "global",
        "env_id": 1,
        "description": "",
        "environment_name": "global",
        "create_dt": "2019-02-14T16:51:47.704Z",
        "template": "",
        "wf_id": 1,
        "release": "global",
        "schedule_dt": "2019-02-14T16:51:47.704Z",
        "release_id": 1,
        "overall_progress": 1,
        "status_cd": 1,
        "status_description": "",
        "frequency_cd": 1,
        "frequency_description": "once",
        "duration": "long",
        "stages": [
            {
                "stage_ui_id": "global",
                "name": "global",
                "actual_start_dt": "2019-02-14T16:51:47.704Z",
                "description": "posting",
                "planned_start_dt": "2019-02-14T16:51:47.704Z",
                "workflow_id": 1,
                "create_dt": "2019-02-14T16:51:47.704Z",
                "status_description": "",
                "status_cd": 1,
                "planned_end_dt": "2019-02-14T16:51:47.704Z",
                "actual_end_dt": "2019-02-14T16:51:47.704Z",
                "stage_id": 1,
                "duration": "long",
                "tasks": [
                    {
                        "task_ui_id": "global",
                        "name": "global",
                        "actual_start_dt": "2019-02-14T16:51:47.704Z",
                        "task_id": 1,
                        "stage_id": 1,
                        "service_name": "JMETER",
                        "action_name": "Load Test",
                        "service_id": "sv12",
                        "action_id": "sv12_ac1",
                        "dag_task_name": "",
                        "input": {
                            "file_path": "testpath"
                        },
                        "status_description": "",
                        "status_cd": 1,
                        "actual_end_dt": "2019-02-14T16:51:47.704Z",
                        "duration": "",
                        "planned_start_dt": "2019-02-14T16:51:47.704Z",
                        "planned_end_dt": "2019-02-14T16:51:47.704Z"
                    }
                ]
            }
        ]
    }



    return workflow_data


def stage_payload():
    stage_data = {"stage_id": 1,
                  "stage_ui_id": "Hack",
                  "name": "DemoHack",
                  "description": "testing",
                  "create_dt": "2018-12-03T20:02:06.842Z",
                  "planned_start_dt": "2018-12-03T20:02:06.842Z",
                  "planned_end_dt": "2018-12-03T20:02:06.842Z",
                  "actual_start_dt": "2018-12-03T20:02:06.842Z",
                  "actual_end_dt": "2018-12-03T20:02:06.842Z",
                  "status_cd": 1,
                  "owner": "Hack",
                  "order": 0,
                  "workflow_id": 1}
    return stage_data


def task_payload():
    task_data = {
                        "task_ui_id": "JMETERload1_test43389xs4pe9",
                        "name": "Test_tsk",
                        "actual_start_dt": "2019-02-14T16:51:47.704Z",
                        "task_id": 1,
                        "stage_id": 1,
                        "service_name": "JMETER",
                        "action_name": "Load Test",
                        "service_id": "sv12",
                        "action_id": "sv12_ac1",
                        "dag_task_name": "",
                        "input": {
                            "file_path": "testpath"
                        },
                        "status_description": "",
                        "status_cd": 1,
                        "actual_end_dt": "2019-02-14T16:51:47.704Z",
                        "duration": "",
                        "planned_start_dt": "2019-02-14T16:51:47.704Z",
                        "planned_end_dt": "2019-02-14T16:51:47.704Z"
               }
    return task_data
