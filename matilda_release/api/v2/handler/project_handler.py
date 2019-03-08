from matilda_release.db import api as db_api
from matilda_release.db.sqlalchemy import models
from matilda_release.api.v2.model.model import project

from datetime import datetime

def create_project(args):
    pj = models.Project()
    pj.project_id = args.get('project_id')
    pj.name = args.get('name')
    pj.owner = args.get('owner')
    pj.create_dt = datetime.now()
    pj.status = args.get('status')
    resp = db_api.create_project(pj)
    return resp

def get_projects(project_id=None):
    from matilda_release.api.v2.handler import application_handler as ah
    pj_list = db_api.get_projects(project_id)
    print ('project list {}'.format(pj_list))
    resp = []
    for item in pj_list:
        item = item.to_dict()
        applications = ah.get_applications(project_id=item.get('project_id'))
        for key in project:
            if key not in item.keys():
                item[key] = None
        item['applications'] = applications
        resp.append(item)
    return resp