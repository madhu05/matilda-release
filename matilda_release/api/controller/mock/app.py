import json
import os
import jinja2
import jsonify
import random

from matilda_release.api.controller.mock import flow_mock

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_oslolog import OsloLog

from matilda_release.api.controller import api_handler

app = Flask(__name__)
CORS(app)
LOG = OsloLog(app).logger


@app.route('/api/release/artifact/types', methods=['GET'])
def get_artifact_types():
    data = {'artifact_types': ['Features', 'Test Suites', 'Wiki Links', 'Design Documents', 'Other']}
    return jsonify(data)

@app.route('/api/release/artifacts/<project>/<application>/<artifact_type>', methods=['GET'])
def get_artifacts(project, application, artifact_type):
    resp = api_handler.get_artifacts(artifact_type)
    return jsonify(resp)

@app.route('/api/release/<type>', methods=['POST'])
def create_release(type='app'):
    req_data = json.loads(request.data)
    print ('create release {}'.format(req_data))
    resp = api_handler.create_release(args=req_data, type=type)
    with open('release_list.json') as f:
        rls_data = json.load(f)
    print (rls_data)
    data = {
    "id": "154451" + str(random.randint(1,30)),
    "releasename": req_data.get('releasename'),
    "description": req_data.get('description'),
    "application": req_data.get('application'),
    "releaseversion": req_data.get('releaseversion'),
    "project": req_data.get('project'),
    "releaseschedule": req_data.get('releaseschedule'),
    "status": "Scheduled"
    }
    rls_data.append(data)
    with open('release_list.json', 'w') as f:
        f.write(json.dumps(rls_data))
    return jsonify(resp)

@app.route('/api/release/<type>', methods=['GET'])
@app.route('/api/release/<type>/<release_id>', methods=['GET'])
def get_releases(type='app', release_id=None):
    resp = api_handler.get_release(type, release_id)
    return jsonify(resp)

@app.route('/api/release/features/<project_id>/<app_id>/<version>', methods=['GET'])
def get_features(project_id, app_id, version):
    pass

@app.route('/api/release/testfacts/<project_id>/<app_id>/<version>', methods=['GET'])
def get_test_suites(project_id, app_id, tool):
    pass

@app.route('/api/release/<release_id>/<type>/artifacts', methods=['POST'])
def link_artifacts(release_id, type):
    artifact_data = json.loads(request.data)
    resp = api_handler.link_artifacts(release_id, type, artifact_data)
    return jsonify(resp)

@app.route('/api/release/<release_id>/<type>/env', methods=['POST'])
def create_environment(release_id, type):
    env_data = json.loads(request.data)
    resp = api_handler.create_environment(release_id, type, env_data)
    return jsonify(resp)

@app.route('/api/release/<release_id>/<type>/env', methods=['GET'])
def get_environments(release_id, type, extended=True):
    resp = api_handler.get_environments(release_id=release_id)
    return jsonify(resp)

@app.route('/api/release/<release_id>/<env>/wf', methods=['POST'])
def create_workflow(release_id, env):
    env_data = json.loads(request.data)
    resp = api_handler.create_workflow(release_id, env, env_data)
    print ('final response {}'.format(jsonify(resp)) )
    return jsonify(resp)

@app.route('/api/release/<release_id>/<env>/wf/<workflow_id>', methods=['GET'])
def get_workflow(release_id, env, workflow_id):
    resp = api_handler.get_full_workflow(release_id)
    return jsonify(resp)

@app.route('/api/release/infra/impacted_systems', methods=['GET'])
def get_systems():
    with open('impacted_systems.json') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/api/release/infra/impacted_apps', methods=['GET'])
def get_apps():
    with open('impacted_apps.json') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/api/release/summary', methods=['GET'])
def get_rls_summary():
    with open('release_list.json') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/api/release/view', methods=['GET'])
def get_rls_view():
    with open('rls_data.json') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/api/release/<release_id>/launch', methods=['POST'])
def launch_release(release_id):
    flow_mock.launch_release()
    with open('rls_data.json') as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6002, debug=True)


