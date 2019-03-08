import json
import datetime
import re
import requests

from matilda_release.api.v2.handler import release_handler as rh


class HPALMClient():

    TP_FIELDS = {
        'TEST_TYPES': 'user-07',
        'OWNER': 'owner',
        'STATUS': 'status',
        'EXEC_STATUS': 'exec-status',
        'NAME': 'name',
        'EXEC_TYPE': 'subtype-id',
        'TS_NAME': 'user-01',
        'PARENT_ID': 'parent-id',
        'PLATFORM': 'user-03'
    }

    TEST_TYPES = {
        'INTTST': 'Integration Testing',
        'SYSTST': 'System Testing',
        '5:00 AM': 'PROD 05AM',
        '10:00 AM': 'PROD 10AM',
        'Monday': 'PROD Monday'
    }

    BASE_FOLDER = {
        "name": "2019",
        "id": "0",
        "children": [
            {
                "name": "DERIVED_NAME",
                "id": "0",
                "children":
                    [

                        {
                            "name": "Linux INTTST Validation",
                            "id": "0",
                            "children": [

                            ]
                        },
                        {
                            "name": "Linux SYSTST Validation",
                            "id": "0",
                            "children": [

                            ]
                        },
                        {
                            "name": "PROD 05AM Validation",
                            "id": "0",
                            "children": [

                            ]
                        },
                        {
                            "name": "PROD 10AM Validation",
                            "id": "0",
                            "children": [

                            ]
                        },
                        {
                            "name": "PROD Monday Validation",
                            "id": "0",
                            "children": [

                            ]
                        },
                        {
                            "name": "Windows INTTST Validation",
                            "id": "0",
                            "children": [

                            ]
                        },
                        {
                            "name": "Windows SYSTST Validation",
                            "id": "0",
                            "children": [

                            ]
                        }

                    ]
                }
            ]
        }


    def __init__(self, release_name='20190228_Matilda_POC', impacted_apps=None):
        self.base_url = 'http://TLMTLDA001:8080/matilda/alm'
        self.user = None
        self.password = None
        self.impacted_apps = impacted_apps
        self.release_name = release_name

    def post(self, url, data, user=None, password=None):
        url = self.base_url + url
        headers = {'Content-Type': 'application/json', 'Accepts': '*/*'}
        print ('Data to post {}'.format(data))
        resp = requests.post(url, data=data, headers=headers)
        if resp.status_code != requests.codes.ok:
            print(str(resp.status_code) + '---' + str(resp.content))
            #raise Exception('Failed to create ', resp.status_code, resp.content)
        #print ('Response JSON {}'.format(resp.json()))
        try:
            return resp.json()
        except:
            return resp.content

    def get(self, url, user=None, password=None):
        url = self.base_url + url
        headers = {'Content-Type': 'application/json'}
        resp = requests.get(url, headers=headers)
        if resp.status_code != requests.codes.ok:
            raise Exception('Failed to get ', resp.content)
        print ('Response JSON from GET {}'.format(resp.json()))
        return resp.json()

    def get_impacted_systems(self, release_id):
        return rh.get_infra_release_impacted_application(release_id)

    def get_or_create_folder(self, folderList):
        url = '/CreateUpdateTestSetFolders'
        try:
            response = self.post(url, folderList)
            return response
        except Exception as e:
            print(e)

    def create_app_test_suites(self, data):
        for app in data:
            app_hierarchical_id = self.get_app_hierarchical_path(app['application_name'])
            app_test_cases = self.get_app_test_cases(app_hierarchical_id)

    def get_app_hierarchical_path(self, appName):
        url = '/fetchTestFolderInfo/{}'.format(appName)
        try:
            response = self.get(url)
            app_fields = response['entities']['fields']
            for item in app_fields:
                if item['Name'] == 'hierarchical-path':
                    return item['values'][0]['value']
        except Exception as e:
            print (e)

    def get_app_test_cases(self, appName):
        url = '/fetchTestCases/{}'.format(self.get_app_hierarchical_path(appName))
        try:
            response = self.get(url)
            hpalm_data = self._filter_app_test_case_from_hp_alm(response)
        except Exception as e:
            print (e)

    def create_base_folder(self):
        self.BASE_FOLDER['children'][0]['name'] = self.release_name
        print ('Folder path {}'.format(self.BASE_FOLDER))
        self.folder_ids = self.get_or_create_folder(str(self.BASE_FOLDER))

    def _filter_app_test_case_from_hp_alm(self, data):
        test_cases = data['entities']
        resp = []
        for test_case in test_cases:
            field_data = test_case['Fields']
            test_case_data = {}
            test_types = []
            platforms = []
            ts_name = None
            name = None
            exec_type = None
            for field in field_data:
                if field['Name'] == self.TP_FIELDS['TS_NAME']:
                    ts_name = field['values'][0]['value']
                if field['Name'] == self.TP_FIELDS['NAME']:
                    name = field['values'][0]['value']
                if field['Name'] == self.TP_FIELDS['EXEC_TYPE']:
                    exec_type = field['values'][0]['value']
                if field['Name'] == self.TP_FIELDS['TEST_TYPES']:
                    for value in field['values']:
                        test_types.append(value['value'])
                if field['Name'] == self.TP_FIELDS['PLATFORM']:
                    for value in field['values']:
                        platforms.append(value['value'])
            test_case_data['exec_type'] = exec_type
            test_case_data['ts_name'] = ts_name
            test_case_data['name'] = name
            test_case_data['platforms'] = platforms
            test_case_data['test_types'] = test_types
            resp.append(test_case_data)
        return resp

    def _create_folder_structure(self, impacted_apps, hpalm_data):
        resp = []
        for app in impacted_apps:
            #hpalm_data = self.get_app_test_cases(app['application_name'])
            if hpalm_data is not None:
                prod_test_types = app['test_type_prod'].split(',')
                for ptt in prod_test_types:
                    for hpitem in hpalm_data:
                        if self.TEST_TYPES[ptt] in hpitem['test_types']:
                            folder_name = ' '.join([self.TEST_TYPES[ptt], 'Validation'])
                            target_folder_id = self.folder_ids[folder_name]
                            # TODO: Create TS
                            resp.append({app['application_name']: {target_folder_id: folder_name}})
                non_prod_test_types = app['test_type_non_prod'].split(',')
                for nptt in non_prod_test_types:
                    for hpitem in hpalm_data:
                        if self.TEST_TYPES[nptt] in hpalm_data['test_types']:
                            folder_name = ' '.join([app['platform'], nptt, 'Validation'])
                            target_folder_id = self.folder_ids[folder_name]
                            # TODO: Create TS
                            resp.append({app['application_name']: {target_folder_id: folder_name}})
        return resp

    def create_target_testset(self):
        self.create_base_folder()
        resp = []
        for app in self.impacted_apps:
            #hpalm_data = self.get_app_test_cases(app['application_name'])
            if 'test_type_prod' in app.keys():
                prod_test_types = re.split(', |;', app['test_type_prod'])
                for ptt in prod_test_types:
                    if ptt not in ('Opt-Out', 'Not Applicable'):
                        folder_name = ' '.join([self.TEST_TYPES[ptt], 'Validation'])
                        print ('Folder name {}'.format(folder_name))
                        target_folder_id = self.folder_ids[folder_name]
                        #subTypeId = hpalm_data[0]['exec_type']
                        self._create_test_set(app['application_name'], target_folder_id, None)
            if 'test_type_non_prod' in app.keys():
                non_prod_test_types = re.split(', |;', app['test_type_non_prod'])
                for nptt in non_prod_test_types:
                    if nptt not in ('Opt-Out', 'Not Applicable'):
                        folder_name = ' '.join([app['platform'], nptt.strip(), 'Validation'])
                        target_folder_id = self.folder_ids[folder_name]
                        #subTypeId = hpalm_data[0]['exec_type']
                        self._create_test_set(app['application_name'], target_folder_id, None)
        return resp


    def _create_test_set(self, name, target_id, subTypeId):
        t = datetime.datetime.now()
        data = {
            'testSetName': str(name),
            'parentId': str(target_id),
            'subTypeId': 'hp.qc.test-set.default',
            'openDate': t.strftime('%Y-%m-%d'),
            'description': str(name),
            'status': 'Open'
        }
        url = '/CreateUpdateTestSets'
        print ('Data for TS {}'.format(data))
        resp = self.post(url=url, data=str(data))
        return resp

