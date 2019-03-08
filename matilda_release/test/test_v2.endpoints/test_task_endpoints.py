import json,requests,pytest,sys
from flask import request
from flask_restplus import Resource

from matilda_release.api.v2.restplus import api
from matilda_release.api.v2.model.model import task, task_response
from matilda_release.api.v2.handler import task_handler




def test_get_taskCollection():
    url = 'http://localhost:5000/api/rls/release/1/environment/1/workflow/1/stage/1/tasks'
    response = requests.get(url)
    assert response.status_code == 200