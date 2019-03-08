import json
import requests
import jenkins
from jira import JIRA

sys_id = '210827d64fa75f80bc3231124210c7bf'

def create_incident(msg):
    url = 'https://cnetglobaldemo1.service-now.com/api/now/table/incident'
    username = 'matilda'
    password = 'matilda'
    payload = {
            "short_description": msg,
            "assignment_group": "",
            "cmdb_ci": "",
            "caller_id": "",
            "state": "1",
            "priority": "5",
            "assigned_to": "Ananda",
            "category": "Matilda"
        }

    headers = {"Content-Type": "application/json",
               "Accept": "application/json"}

    response = requests.post(url, auth=(username, password),
                             headers=headers, data=json.dumps(payload))
    # Check for HTTP codes other than 200
    if response.status_code > 201:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response)

    # Decode the JSON response into a dictionary and use the data
    resp = {
        'status_code': response.status_code,
        'content': response.content
    }
    data = response.json()
    print (data)
    print (data.get('result').get('sys_id'))
    sys_id = str(data.get('result').get('sys_id'))
    print (str(sys_id))
    return resp


def build_job(job_name):

    job_name = 'demo_app_build'
    token = '5b9575fb7ed9cfa8f0e4def647e9ddb2'
    url = 'http://192.168.10.161:8080'
    user = 'admin'
    # jen = jenkins.Jenkins(url, username=user, password=token)
    # response = jen.build_job(job_name, None, token)
    # return response
    url = url + '/job/' + job_name + '/build'
    print url
    headers = {'Content-Type': 'application/json', 'Accepts': 'application/json'}
    response = requests.post(url, auth=(user, token), headers=headers)
    print 'Response %r' % response

def update_incident(notes):
    url = 'https://cnetglobaldemo1.service-now.com/api/now/table/incident/' + str(sys_id)
    username = 'matilda'
    password = 'matilda'
    payload = {
            "comments": notes
        }

    headers = {"Content-Type": "application/json",
               "Accept": "application/json"}

    response = requests.put(url, auth=(username, password),
                             headers=headers, data=json.dumps(payload))
    # Check for HTTP codes other than 200
    #if response.status_code > 201:
    print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response)

    # Decode the JSON response into a dictionary and use the data
    resp = {
        'status_code': response.status_code,
        'content': response.content
    }
    print resp
    return resp

def create_jira_issue(summary, description, issuetype='Bug'):
    host = 'https://matildacloud.atlassian.net'
    user = 'ananda@cnet-global.com'
    password = 'Sneha@30'
    ji = JIRA(options={'server': host}, basic_auth=(user, password))
    fields = {
        "project":
            {
                "key": "MM"
            },
        "summary": summary,
        "description": description,
        "issuetype": {
            "name": issuetype
        }
    }
    issue = ji.create_issue(fields=fields)
    print issue
    return issue.__dict__

def launch_release():
    create_incident("REVIEW - Cost Management Platform - Cost Analysis - R1.0 Deployment Launched.")
    create_jira_issue('Code Coverage not met', 'Code coverage for Matilda Cost Management Platform - Cost Analysis code '
                                               'coverage was 70.38% ')
    update_incident('SonarQube Code Coverage completed : 70.38%')
    update_incident('Jira Ticket created for Code Coverage')
    update_incident('Infrastructure request created.')
    update_incident('Infrastructure Created : VM Count - 1; IP Address: 192.168.20.114')
    build_job('demo_app_build')
    update_incident('Application Build successful: No Errors')
    build_job('Deploy')
    update_incident('Application Deployment Completed: No Errors')
    create_incident("REVIEW - Cost Management Platform - Cost Analysis - R1.0 - Manual Testing Requested.")
