from matilda_release.db import api as db_api;
from matilda_release.util import json_helper
from datetime import datetime
from werkzeug.exceptions import BadRequest
from matilda_release.util.status_helper import StatusDefinition
from matilda_release.util import encoder
import datetime as dl


enc = encoder.AESCipher()

def check_and_update_task(task_id=None, dag_task_name=None, data=None):
    resp = list()
    if task_id is None and dag_task_name is None:
        raise BadRequest('update task needs a task id or dag_task_name')
    else:
        tasks_from_db = db_api.get_task(task_id=task_id, dag_task_name = dag_task_name)
        for task in tasks_from_db:
            if task.get('input') is None:
                task['status_cd'] = StatusDefinition.defined.status_cd
            else:
                task['status_cd'] = StatusDefinition.configured.status_cd
                if data is not None:
                    task_status_cd_from_data = data.get('status_cd')
                    task['output'] = enc.encrypt(json_helper.create_dict_from_json_string(data))
                    task['status_cd'] = task_status_cd_from_data
                    if task_status_cd_from_data == StatusDefinition.inProgress.status_cd:
                        task['actual_start_dt'] = datetime.now()
                    elif task_status_cd_from_data in [StatusDefinition.success.status_cd, StatusDefinition.failed.status_cd]:
                        task['actual_end_dt'] = datetime.now()
                        duration = (task['actual_end_dt'] - task['actual_start_dt']).total_seconds()
                        task['duration'] = str(dl.timedelta(seconds=duration))
                resp.append(db_api.update_task(task_id=task_id, dag_task_name=dag_task_name,  data=task))
                check_and_update_stage(stage_id=task.get('stage_id'))
    return resp



def check_and_update_stage(stage_id=None, wf_id=None):
    resp = list()
    if stage_id is None and wf_id is None:
        raise BadRequest('update stage needs a stage id or workflow id')
    else:
        stages_from_db = db_api.get_stage(wf_id=wf_id, stage_id=stage_id)
        for stage in stages_from_db:
            count_dict = {'configured': 0, 'success': 0}
            tasks_for_stage = db_api.get_task(stage_id=stage.get('stage_id'))
            print(type(tasks_for_stage))
            total_tasks = len(tasks_for_stage)
            for task in tasks_for_stage:
                task_status_cd = task.get('status_cd')
                if task_status_cd == StatusDefinition.defined.status_cd:
                    stage['status_cd'] = StatusDefinition.defined.status_cd
                    break;
                elif task_status_cd == StatusDefinition.configured.status_cd:
                    count_dict['configured']+=1
                elif task_status_cd == StatusDefinition.inProgress.status_cd:
                    stage['status_cd'] = StatusDefinition.inProgress.status_cd
                    break;
                elif task_status_cd == StatusDefinition.failed.status_cd:
                    stage['status_cd'] = StatusDefinition.failed.status_cd
                    break;
                elif task_status_cd == StatusDefinition.success.status_cd:
                    count_dict['success'] += 1

            if count_dict['configured'] == total_tasks:
                stage['status_cd'] = StatusDefinition.configured.status_cd
            elif count_dict['success'] == total_tasks:
                stage['status_cd'] = StatusDefinition.success.status_cd
            print('stage:{}'.format(stage))
            resp.append(db_api.update_stage(stage.get('stage_id'), stage))
            check_and_update_workflow(wf_id=stage.get('wf_id'))
    return resp


def check_and_update_workflow(wf_id=None):
    resp = None
    if wf_id is None:
        raise BadRequest('update stage needs a workflow id')
    else:
        workflow_from_db = db_api.get_workflow(wf_id=wf_id)
        count_dict = {'configured':0, 'success':0}
        for workflow in workflow_from_db:
            intial_workflow_status_cd = workflow.get('status_cd')

            stages_for_workflow = db_api.get_stage(wf_id=wf_id)
            total_stages = len(stages_for_workflow)
            for stage in stages_for_workflow:
                stage_status_cd = stage.get('status_cd')
                if stage_status_cd == StatusDefinition.defined.status_cd:
                    workflow['status_cd'] = StatusDefinition.defined.status_cd
                    break;
                elif stage_status_cd == StatusDefinition.configured.status_cd:
                    count_dict['configured']+=1
                elif stage_status_cd == StatusDefinition.inProgress.status_cd:
                    workflow['status_cd'] = StatusDefinition.inProgress.status_cd
                    break;
                elif stage_status_cd == StatusDefinition.failed.status_cd:
                    workflow['status_cd'] = StatusDefinition.failed.status_cd
                    break;
                elif stage_status_cd == StatusDefinition.success.status_cd:
                    count_dict['success'] += 1

            if count_dict['configured'] == total_stages:
                if intial_workflow_status_cd == StatusDefinition.inProgress.status_cd:
                    workflow['status_cd'] = intial_workflow_status_cd
                else:
                    workflow['status_cd'] = StatusDefinition.configured.status_cd
            elif count_dict['success'] == total_stages:
                workflow['status_cd'] = StatusDefinition.success.status_cd
            resp = db_api.update_workflow(wf_id, workflow)
            check_and_update_environment(env_id=workflow.get('env_id'))
    return resp

def check_and_update_environment(env_id=None):
    resp = None
    if env_id is None:
        raise BadRequest('update environment needs a environment id')
    else:
        environment_from_db = db_api.get_environment(env_id=env_id)
        for environment in environment_from_db:
            workflow_for_environment = db_api.get_workflow(env_id=env_id)
            total_workflow_for_env = len(workflow_for_environment)
            if total_workflow_for_env > 1:
                print('More than one workflow present for the environment')
            elif total_workflow_for_env ==1:
                for workflow in workflow_for_environment:
                    environment['status_cd'] = workflow.get('status_cd')

            resp = db_api.update_environment(env_id, environment)
            check_and_update_release(release_id=environment.get('release_id'))
    return resp

def check_and_update_release(release_id=None):
    resp = None
    if release_id is None:
        raise BadRequest('update release needs a release id')
    else:
        release_from_db = db_api.get_release(release_id=release_id)
        count_dict = {'configured':0, 'success':0}
        total_env = 0
        for release in release_from_db:
            env_for_release = db_api.get_environment(release_id=release_id)
            total_env = len(env_for_release)
            for env in env_for_release:
                env_status_cd = env.get('status_cd')
                if env_status_cd == StatusDefinition.defined.status_cd:
                    release['status_cd'] = StatusDefinition.defined.status_cd
                    break;
                elif env_status_cd == StatusDefinition.configured.status_cd:
                    count_dict['configured']+=1
                elif env_status_cd == StatusDefinition.inProgress.status_cd:
                    release['status_cd'] = StatusDefinition.inProgress.status_cd
                    break;
                elif env_status_cd == StatusDefinition.failed.status_cd:
                    release['status_cd'] = StatusDefinition.failed.status_cd
                    break;
                elif env_status_cd == StatusDefinition.success.status_cd:
                    count_dict['success'] += 1

            if count_dict['configured'] == total_env:
                release['status_cd'] = StatusDefinition.configured.status_cd
            elif count_dict['success'] == total_env:
                release['status_cd'] = StatusDefinition.success.status_cd
            resp = db_api.update_release(release_id, release)
    return resp