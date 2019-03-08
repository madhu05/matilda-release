import json
import os
import jinja2
import jsonify

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_oslolog import OsloLog

from matilda_release.api.controller import api_handler

app = Flask(__name__)
CORS(app)
LOG = OsloLog(app).logger



@app.route('/api/release/<type>', methods=['POST'])
def create_release(type='app'):
    req_data = json.loads(request.data)
    resp = api_handler.create_release(args=req_data, type=type)
    return jsonify(resp)

@app.route('/api/release/<type>', methods=['GET'])
def get_releases(type='app'):
    resp = api_handler.get_release(type)
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6002, debug=True)


