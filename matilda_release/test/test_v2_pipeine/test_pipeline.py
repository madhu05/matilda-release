import unittest

from sqlalchemy import create_engine
from matilda_release.api.v2.handler import environment_handler,project_handler,release_handler,stage_handler,workflow_handler,application_handler,release_plan_handler,task_handler
from matilda_release.db import migration
from matilda_release.test.test_v2_pipeine.Paths import path
from matilda_release.test.test_v2_pipeine.payload import release_payload, env_payload, workflow_payload, project_payload,application_payload, stage_payload, task_payload,release_plan


connection = "sqlite:///release_management.db"
print('connection:{}'.format(connection))
engine = create_engine(connection)
conn = engine.connect()
conn.isolation_level = None
migration.db_sync(database='matilda_release')
scripts = path()


class MatildaReleaseTest(unittest.TestCase):

    def setUp(self):
        super(MatildaReleaseTest, self).setUp()
        self.headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        self.project = project_payload()
        self.application = application_payload()
        self.release_plan=release_plan()
        self.release = release_payload()
        self.environment=env_payload()
        self.workflow=workflow_payload()
        self.stage=stage_payload()
        self.task=task_payload()

    def test_insert_data(self):
        scripts = path()
        response = False
        output = []
        for script in scripts:
            with open(script, 'r', encoding="utf8") as data:
                query = data.read()
                commad = query.split('\n')
                for command in commad:
                    if not command.startswith(("use", "commit", "#", "--")):
                        conn.execute(command)
                        response = True
                        output.append(response)
        assert (all(c == True for c in output)) == True

    def test_post_project(self):
        response = project_handler.create_project(self.project)
        self.assertEqual(response['project_id'], self.project['project_id'])
        self.assertEqual(response['name'], self.project['name'])
        self.assertEqual(response['owner'], self.project['owner'])
        self.assertEqual(response['status'], self.project['status'])

    def test_get_project(self):
        response = project_handler.get_projects()
        print(response)
        self.assertNotEqual(response, {})

    def test_post_application(self):
        response= application_handler.create_application(self.application)
        self.assertEqual(response['app_id'], self.application['app_id'])
        self.assertEqual(response['owner'], self.application['owner'])
        self.assertEqual(response['status'], self.application['status'])
        self.assertEqual(response['project_id'], self.application['project_id'])

    def test_get_application(self):
        response = application_handler.get_applications()
        self.assertNotEqual(response, {})

    def test_post_release_plan(self):
        release_plan_response = release_plan_handler.create_release_plan(self.release_plan)
        print(release_plan_response)

        self.assertEqual(release_plan_response[0]['release_plan_id'], self.release_plan['release_plan_id'])
        self.assertEqual(release_plan_response[0]['release_type_cd'], self.release_plan['release_type_cd'])
        self.assertEqual(release_plan_response[0]['color_pref'], self.release_plan['color_pref'])
        self.assertEqual(release_plan_response[0]['release_plan_name'], self.release_plan['release_plan_name'])
        self.assertEqual(release_plan_response[0]['release_plan_description'], self.release_plan['release_plan_description'])
        self.assertEqual(release_plan_response[0]['release_owner'], self.release_plan['release_owner'])

        def test_post_release(self):
            release_response = release_handler.create_release(self.release)
            print(release_response)
            self.assertEqual(release_response['release_id'], self.release['release_id'])
            self.assertEqual(release_response['name'], self.release['name'])
            self.assertEqual(release_response['project_id'], self.release['project_id'])
            self.assertEqual(release_response['project_name'], self.release['project_name'])
            self.assertEqual(release_response['application_id'], self.release['application_id'])
            self.assertEqual(release_response['application_name'], self.release['application_name'])
            self.assertEqual(release_response['os_id'], self.release['os_id'])
            self.assertEqual(release_response['os_name'], self.release['os_name'])
            self.assertEqual(release_response['platform_id'], self.release['platform_id'])
            self.assertEqual(release_response['platform_name'], self.release['platform_name'])
            self.assertEqual(release_response['vnf_site'], self.release['vnf_site'])
            self.assertEqual(release_response['vnf_node'], self.release['vnf_node'])
            self.assertEqual(release_response['release_type_cd'], self.release['release_type_cd'])
            self.assertEqual(release_response['release_type_description'], self.release['release_type_description'])
            self.assertEqual(release_response['status_cd'], self.release['status_cd'])
            self.assertEqual(release_response['status_description'], self.release['status_description'])
            self.assertEqual(release_response['duration'], self.release['duration'])
            self.assertEqual(release_response['description'], self.release['description'])
            self.assertEqual(release_response['release_plan_id'], self.release['release_plan_id'])
            self.assertEqual(release_response['release_plan_name'], self.release['release_plan_name'])

        def test_post_environment(self):
            response = environment_handler.create_environment('release_id=1', self.environment)
            self.assertEqual(response['env_id'], self.environment['env_id'])
            self.assertEqual(response['name'], self.environment['name'])
            self.assertEqual(response['env_type_cd'], self.environment['env_type_cd'])
            self.assertEqual(response['env_type_description'], self.environment['env_type_description'])
            self.assertEqual(response['status_cd'], self.environment['status_cd'])
            self.assertEqual(response['status_description'], self.environment['status_description'])

        def test_post_workflow(self):
            response = workflow_handler.create_workflow(1, 1, self.workflow, include_env='include_env')
            self.assertEqual(response['name'], self.workflow['name'])
            self.assertEqual(response['env_id'], self.workflow['env_id'])
            self.assertEqual(response['environment_name'], self.workflow['environment_name'])
            self.assertEqual(response['template'], self.workflow['template'])
            self.assertEqual(response['wf_id'], self.workflow['wf_id'])
            self.assertEqual(response['release'], self.workflow['release'])
            self.assertEqual(response['release_id'], self.workflow['release_id'])
            self.assertEqual(response['overall_progress'], self.workflow['overall_progress'])
            self.assertEqual(response['status_cd'], self.workflow['status_cd'])
            self.assertEqual(response['status_description'], self.workflow['status_description'])
            self.assertEqual(response['frequency_cd'], self.workflow['frequency_cd'])
            self.assertEqual(response['frequency_description'], self.workflow['frequency_description'])
            self.assertEqual(response['duration'], self.workflow['duration'])

    def test_get_release_plan(self):
        response = release_plan_handler.get_release_plan()
        self.assertNotEqual(response, {})

    def test_get_release(self):

        response = release_handler.get_release()
        self.assertNotEqual(response, {})

    def test_get_environment(self):
        response = environment_handler.get_environment_details(1, 1)
        self.assertNotEqual(response, {})

    def test_get_workflow(self):
        response = workflow_handler.get_workflow(wf_id=1)
        self.assertNotEqual(response, {})

    def test_post_stages(self):
        response = stage_handler.create_stage(2, self.stage)
        self.assertEqual(response[0]['stage_id'], self.stage['stage_id'])
        self.assertEqual(response[0]['stage_ui_id'], self.stage['stage_ui_id'])
        self.assertEqual(response[0]['name'], self.stage['name'])
        self.assertEqual(response[0]['status_cd'], self.stage['status_cd'])
        self.assertEqual(response[0]['owner'], self.stage['owner'])
        self.assertEqual(response[0]['order'], self.stage['order'])

    def test_get_stage(self):
        response = stage_handler.get_stage(1)
        self.assertNotEqual(response, {})

    def test_post_taskCollection(self):
        response = task_handler.create_task(1, self.task)
        self.assertEqual(response['task_ui_id'], self.task['task_ui_id'])
        self.assertEqual(response['name'], self.task['name'])
        self.assertEqual(response['task_id'], self.task['task_id'])
        self.assertEqual(response['stage_id'], self.task['stage_id'])
        self.assertEqual(response['service_id'], self.task['service_id'])
        self.assertEqual(response['action_id'], self.task['action_id'])

if __name__ == '__main__':
    unittest.main()

