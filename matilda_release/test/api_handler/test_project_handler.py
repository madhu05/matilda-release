from matilda_release.api.v2.handler import project_handler

def get_projects():
    print(project_handler.get_projects())

get_projects()
