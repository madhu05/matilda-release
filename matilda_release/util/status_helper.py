import collections


class StatusDefinition(object):
    status_list = list()

    status = collections.namedtuple('Status', 'status_cd status_description status_order')
    defined = status(status_cd=1, status_description='Defined', status_order=1)
    configured = status(status_cd=2, status_description='Configured', status_order=2)
    inProgress = status(status_cd=3, status_description='InProgress', status_order=3)
    success = status(status_cd=4, status_description='Success', status_order=4)
    failed = status(status_cd=5, status_description='Failed', status_order=5)

    status_list.append(defined)
    status_list.append(configured)
    status_list.append(inProgress)
    status_list.append(success)
    status_list.append(failed)


def get_status(status_cd=None):
    for status in StatusDefinition.status_list:
        # print(type(status))
        if status.status_cd == status_cd:
            return status

class FrequencyDefinition(object):
    frequency_list = list()
    frequency = collections.namedtuple('Frequency', 'frequency_cd frequency_description')
    once = frequency(frequency_cd=1, frequency_description='once')
    hourly = frequency(frequency_cd=2, frequency_description='hourly')
    daily = frequency(frequency_cd=3, frequency_description='daily')
    weekly = frequency(frequency_cd=4, frequency_description='weekly')
    monthly = frequency(frequency_cd=5, frequency_description='monthly')
    yearly = frequency(frequency_cd=6, frequency_description='yearly')

    frequency_list.append(once)
    frequency_list.append(hourly)
    frequency_list.append(daily)
    frequency_list.append(weekly)
    frequency_list.append(monthly)
    frequency_list.append(yearly)

def get_frequency(frequency_cd = None):
    for frequency in FrequencyDefinition.frequency_list:
        # print(type(frequency))
        if frequency.frequency_cd == frequency_cd:
            return frequency

class EnvTypeDefinition(object):
    env_type_list = list()
    env_type = collections.namedtuple('EnvType', 'env_type_cd env_type_description')
    development = env_type(env_type_cd=1, env_type_description='Development')
    system_test = env_type(env_type_cd=2, env_type_description='System Test')
    production = env_type(env_type_cd=3, env_type_description='Production')
    integrated_test = env_type(env_type_cd=4, env_type_description='Integrated Test')

    env_type_list.append(development)
    env_type_list.append(system_test)
    env_type_list.append(production)
    env_type_list.append(integrated_test)


def get_env_type(env_type_cd = None, env_type_description = None):
    for env_type in EnvTypeDefinition.env_type_list:
        # print(type(frequency))
        if env_type.env_type_cd == env_type_cd:
            return env_type
        if env_type.env_type_description == env_type_description:
            return  env_type


class ReleaseTypeCdDefinition(object):

    release_type = collections.namedtuple('Release_Type', 'release_type_cd release_type_description')
    application = release_type(release_type_cd=1, release_type_description='Application')
    infrastructure = release_type(release_type_cd=2, release_type_description='Infrastructure')
    vnf = release_type(release_type_cd=3, release_type_description='VNF')

'''class ChartIdCdDefinition(object):

    chart_type = collections.namedtuple('ChartId_Type', 'chart_type_cd, chart_type_description')
    Released_Metrics = chart_type(chart_type_cd=1, chart_type_description='Released_Metrics')
    Release_Churn= chart_type(chart_type_cd=2, chart_type_description='Release_Churn')
    YTD_Normal_Changes= chart_type(chart_type_cd=3, chart_type_description='YTD_Normal_Changes_for_ERM&E MMWs')
    Change_Induced_Incidents= chart_type(chart_type_cd=4, chart_type_description='Change_Induced_Incidents')'''

class Metrics_table_Definition(object):

    metrics_table = collections.namedtuple('metrics_table', 'metrics_col sheet_col')
    YTD_Changes = metrics_table(metrics_col='YTD_Changes', sheet_col='# YTD Normal Changes')
    YTD_Changes_managed_release = metrics_table(metrics_col='YTD_Changes_managed_release', sheet_col='% YTD Normal Changes deployed as part of a managed release')
    YTD_Changes_ERME_MMW = metrics_table(metrics_col='YTD_Changes_ERME_MMW', sheet_col='# YTD Normal Changes for ERM&E MMW')
    YTD_ALL_Changes = metrics_table(metrics_col='YTD_ALL_Changes', sheet_col='# YTD All Changes')
    YTD_ALL_Changes_ERME_MMW = metrics_table(metrics_col='YTD_ALL_Changes_ERME_MMW', sheet_col='# YTD All Changes for ERM&E MMW')
    YTD_ALL_Changes_managed_release = metrics_table(metrics_col='YTD_ALL_Changes_managed_release', sheet_col='% YTD All Changes deployed as part of a managed release')
    Release_Churn_Planned = metrics_table(metrics_col='Release_Churn_Planned', sheet_col='Release Churn -- Number of Changes Planned')
    Release_Churn_Deployed = metrics_table(metrics_col='Release_Churn_Deployed', sheet_col='Release Churn -- Number of Changes Deployed')
    MMW_Statistics_Deployed_Success = metrics_table(metrics_col='MMW_Statistics_Deployed_Success', sheet_col='MMW Statistics -- Changes Deployed Successfully')
    MMW_Statistics_Deployed_Issues = metrics_table(metrics_col='MMW_Statistics_Deployed_Issues', sheet_col='MMW Statistics -- Changes Deployed with Issues')
    MMW_Statistics_Cancelled = metrics_table(metrics_col='MMW_Statistics_Cancelled', sheet_col='MMW Statistics -- Changes Backed Out / Cancelled')
    MMW_Statistics_Incidents = metrics_table(metrics_col='MMW_Statistics_Incidents', sheet_col='MMW Statistics -- Number of Change-Induced Incidents')
    YTD_Plan_Line = metrics_table(metrics_col='YTD_Plan_Line', sheet_col='% YTD Plan (Trend) Line')

class Appcat_table_Definition(object):

    app_cat_table = collections.namedtuple('app_cat_table', 'metrics_col sheet_col')
    Planned_Changes = app_cat_table(metrics_col='Planned_Changes', sheet_col='Planned Changes')
    Successful_Changes = app_cat_table(metrics_col='Successful_Changes', sheet_col='Successful Changes')
    Changes_with_Issues = app_cat_table(metrics_col='Changes_with_Issues', sheet_col='Changes with Issues')
    Changes_Rolled_Back = app_cat_table(metrics_col='Changes_Rolled_Back', sheet_col='Changes Rolled Back')
    SonarQube_Blocker = app_cat_table(metrics_col='SonarQube_Blocker', sheet_col='SonarQube Code Quality - Blocker')
    SonarQube_Critical = app_cat_table(metrics_col='SonarQube_Critical', sheet_col='SonarQube Code Quality - Critical')
    SonarQube_Major = app_cat_table(metrics_col='SonarQube_Major', sheet_col='SonarQube Code Quality - Major')


class Appsubcomp_table_Definition(object):

    app_subcomp_table = collections.namedtuple('app_subcomp_table', 'metrics_col sheet_col')
    eSign_Access = app_subcomp_table(metrics_col='eSign_Access', sheet_col='eSign & Access')
    Underwriting = app_subcomp_table(metrics_col='Underwriting', sheet_col='Underwriting')

'''['eSign & Access' 'Underwriting']
Claims,Salesforce, [STE,Core Ops,Salesforce]'''
