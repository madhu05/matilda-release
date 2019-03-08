from matilda_plugin.plugins.jira_plugin import jira_plugin

def get_features(project=None):
    jira = jira_plugin.JiraPlugin()
    epics = jira.get_issues(issue_type='Epic')['issues']
    resp = []
    for epic in epics:
        data = epic['fields']
        ec = {}
        ec['id'] = epic['key']
        ec['progress'] = data['aggregateprogress'].get('progress', 0)
        ec['total'] = data['aggregateprogress'].get('total', 0)
        ec['status'] = data['status']['statusCategory']['name']
        ec['summary'] = data['summary']
        resp.append(ec)
    return resp
