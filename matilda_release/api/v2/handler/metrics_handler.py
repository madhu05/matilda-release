import logging


from matilda_release.util.status_helper import Metrics_table_Definition as metric
from matilda_release.util.status_helper import Appcat_table_Definition as appmetric
from datetime import datetime
from matilda_release.util.status_helper import Appsubcomp_table_Definition as subcomp

from collections import defaultdict
import calendar

from matilda_release.db import api as db_api

log = logging.getLogger(__name__)
debug = False

def create_json(second_string=None,data_lst=None):
    metric_totals={}
    for (index,snd) in zip(range(len(second_string)),second_string):
        if data_lst:
            metric_totals[snd]=data_lst[index]
        else:
            metric_totals[snd] ={}


    return metric_totals




def get_metrics_totals(start_date=None,end_date=None):
    ytd_total = {}
    chart1_first = "YTD_Normal_Changes_for_ERME_MMW"
    chart2_first = "Release_Metrics"
    chart3_first = "Change_Induced_Incidents"
    chart4_first = "Release_Churn"
    ytd_total[chart1_first] = {}
    ytd_total[chart2_first] = {}
    ytd_total[chart3_first] = {}
    date_cnt = {}
    met_val = get_infra_component_id()
    for i in range(len(met_val)):
        if met_val[i].get('component_name')=='Server':
            server_id= met_val[i].get('component_id')
        elif met_val[i].get('component_name')=='Middleware':
            middleware_id= met_val[i].get('component_id')
        elif met_val[i].get('component_name')=='Database':
            database_id= met_val[i].get('component_id')
        elif met_val[i].get('component_name')=='Mainframe':
            mainframe_id= met_val[i].get('component_id')
        elif met_val[i].get('component_name')=='Network':
            network_id= met_val[i].get('component_id')
    (server_tot,date_fmt) = get_metrics(component_id=server_id,start_date=start_date,end_date=end_date,json_flag=False)
    if not server_tot[chart1_first][metric.YTD_Changes.metrics_col]:
        return server_tot
    (middleware_tot,date_fmt) = get_metrics(component_id=middleware_id,start_date=start_date,end_date=end_date,json_flag=False)
    if not middleware_tot[chart1_first][metric.YTD_Changes.metrics_col]:
        return middleware_tot
    (database_tot,date_fmt) = get_metrics(component_id=database_id,start_date=start_date,end_date=end_date,json_flag=False)
    if not database_tot[chart1_first][metric.YTD_Changes.metrics_col]:
        return database_tot
    (mainframe_tot,date_fmt) = get_metrics(component_id=mainframe_id,start_date=start_date,end_date=end_date,json_flag=False)
    if not mainframe_tot[chart1_first][metric.YTD_Changes.metrics_col]:
        return mainframe_tot
    (network_tot,date_fmt) = get_metrics(component_id=network_id,start_date=start_date,end_date=end_date,json_flag=False)
    if not network_tot[chart1_first][metric.YTD_Changes.metrics_col]:
        return network_tot
    cat_array=[metric.YTD_Changes.metrics_col,metric.YTD_Changes_ERME_MMW.metrics_col,metric.YTD_Plan_Line.metrics_col]
    for cat in cat_array:
        ytd_total[chart1_first][cat]={}
        for fmt in date_fmt:
            date_cnt[fmt] =0
            ytd_total[chart1_first][cat][fmt] =(server_tot[chart1_first][cat].get(fmt) + middleware_tot[chart1_first][cat].get(fmt) + database_tot[chart1_first][cat].get(fmt) + mainframe_tot[chart1_first][cat].get(fmt) + network_tot[chart1_first][cat].get(fmt))
            if cat == metric.YTD_Plan_Line.metrics_col:
                if server_tot[chart1_first][cat].get(fmt) > 0:
                    date_cnt[fmt]+=1
                if middleware_tot[chart1_first][cat].get(fmt) > 0:
                    date_cnt[fmt]+=1
                if database_tot[chart1_first][cat].get(fmt) > 0:
                    date_cnt[fmt]+=1
                if mainframe_tot[chart1_first][cat].get(fmt) > 0:
                    date_cnt[fmt]+=1
                if network_tot[chart1_first][cat].get(fmt) > 0:
                    date_cnt[fmt]+=1
                if date_cnt[fmt] > 0:
                    ytd_total[chart1_first][cat][fmt] /=date_cnt[fmt]

    cat_array=[metric.Release_Churn_Planned.metrics_col,metric.Release_Churn_Deployed.metrics_col,metric.MMW_Statistics_Deployed_Success.metrics_col,metric.MMW_Statistics_Deployed_Issues.metrics_col,metric.MMW_Statistics_Cancelled.metrics_col]
    for cat in cat_array:
        ytd_total[chart2_first][cat]={}
        for fmt in date_fmt:
            ytd_total[chart2_first][cat][fmt] =(server_tot[chart2_first][cat].get(fmt) + middleware_tot[chart2_first][cat].get(fmt) + database_tot[chart2_first][cat].get(fmt) + mainframe_tot[chart2_first][cat].get(fmt) + network_tot[chart2_first][cat].get(fmt))
    for fmt in date_fmt:
        ytd_total[chart3_first][fmt] =(server_tot[chart3_first].get(fmt) + middleware_tot[chart3_first].get(fmt) + database_tot[chart3_first].get(fmt) + mainframe_tot[chart3_first].get(fmt) + network_tot[chart3_first].get(fmt))
    ytd_total[chart4_first]=server_tot[chart4_first]
    return ytd_total

def get_value_calculate_sum(component_id=None,category_array=None,start_date=None,end_date=None,release_type=2,subcomponent_id=0):
    s_date = datetime.strptime(start_date, "%m-%d-%Y")
    d_date = datetime.strptime(end_date, "%m-%d-%Y")
    start_date=datetime.strftime(s_date, "%m/%d/%Y")
    end_date=datetime.strftime(d_date, "%m/%d/%Y")
    st_date = datetime.strptime(start_date, '%m/%d/%Y').date()
    ed_date = datetime.strptime(end_date, '%m/%d/%Y').date()
    metric_array=[]
    percent_id=0
    for category in category_array:
        if release_type==1:
            temp_obj = db_api.get_app_category(category_name=category)
        else:
            temp_obj = db_api.get_infra_category(category_name=category)
        if category == metric.YTD_Plan_Line.metrics_col:
            percent_id = temp_obj[0].get('category_id')

        if release_type==1:
            if subcomponent_id !=0:
                metric_array.append(db_api.get_app_metrics(component_id=component_id,category_id=temp_obj[0].get('category_id'),subcomponent_id=subcomponent_id,start_date=st_date,end_date=ed_date))
            else:
                metric_array.append(db_api.get_app_metrics(component_id=component_id,category_id=temp_obj[0].get('category_id'),start_date=st_date,end_date=ed_date))
        else:
            metric_array.append(db_api.get_infra_metrics(component_id=component_id,category_id=temp_obj[0].get('category_id'),start_date=st_date,end_date=ed_date))


    sum_list=[]
    date_dict = defaultdict(set)
    for item in metric_array[0]:
        for key, value in item.items():
            date_dict[key].add(value)
    if not date_dict.get('date'):
        return (sum_list,date_dict)
    date_lst= list(date_dict.get('date'))
    if release_type==1:
        date_lst.sort(reverse=True)
        date_fmt=[calendar.month_abbr[dt.month] +'-'+ str(dt.year%2000) for dt in date_lst]
    else:
        date_lst.sort()
        date_fmt=[datetime.strftime(dt,'%m/%d/%Y')for dt in date_lst]
    for met in metric_array:
        sum_dict={}
        count_date={}
        for (fmt,dt) in zip(date_fmt,date_lst):
            sum_dict[fmt]=sum([item['metrics'] for item in met if item['date']==dt])
            if percent_id != 0:
                count_date[fmt] = sum(1 for item in met if item['date'] == dt and item['category_id']==percent_id)
                if count_date[fmt]>0:
                    sum_dict[fmt] /=count_date[fmt]


        sum_list.append(sum_dict)
    return (sum_list,date_fmt)

def get_metrics(component_id=None,start_date=None,end_date=None,json_flag=False):
    jsn={}
    cat_array=[metric.YTD_Changes.metrics_col,metric.YTD_Changes_ERME_MMW.metrics_col,metric.YTD_Plan_Line.metrics_col]
    (sum_list,date_fmt) = get_value_calculate_sum(component_id=component_id,category_array=cat_array,start_date=start_date,end_date=end_date)
    first_string = "YTD_Normal_Changes_for_ERME_MMW"
    second_string =cat_array
    jsn[first_string] =create_json(second_string=second_string,data_lst=sum_list)

    cat_array1=[metric.Release_Churn_Planned.metrics_col,metric.Release_Churn_Deployed.metrics_col,metric.MMW_Statistics_Deployed_Success.metrics_col,metric.MMW_Statistics_Deployed_Issues.metrics_col,metric.MMW_Statistics_Cancelled.metrics_col]
    (sum_list1,date_fmt) = get_value_calculate_sum(component_id=component_id,category_array=cat_array1,start_date=start_date,end_date=end_date)

    first_string = "Release_Metrics"
    second_string =cat_array1
    jsn[first_string] =create_json(second_string=second_string,data_lst=sum_list1)
    cat_array2=[metric.Release_Churn_Planned.metrics_col,metric.Release_Churn_Deployed.metrics_col]
    (sum_list2,date_fmt) = get_value_calculate_sum(component_id=component_id,category_array=cat_array2,start_date=start_date,end_date=end_date)

    first_string = "Release_Churn"
    if json_flag:
        second_string =cat_array2
    #if sum_list2:
        jsn[first_string] =create_json(second_string=second_string,data_lst=sum_list2)
    else:
        jsn[first_string] = {}
    #else:
     #   jsn[first_string]= {}

    cat_array3=[metric.MMW_Statistics_Incidents.metrics_col]
    (sum_list3,date_fmt) = get_value_calculate_sum(component_id=component_id,category_array=cat_array3,start_date=start_date,end_date=end_date)
    first_string = "Change_Induced_Incidents"
        #second_string =["Planned Changes","Changes Deployed"]
    if  sum_list3:
        jsn[first_string] = sum_list3[0] #create_json(second_string=second_string,data_lst=sum_list)
    else:
        jsn[first_string] = {}
    if json_flag:
        #jsn1=json.dumps(jsn)
        return jsn
    else:
        return (jsn,date_fmt)

def get_infra_component_id(component_name=None):
    return db_api.get_infra_component(component_name=component_name)

def get_app_component_id(component_name=None):
    return db_api.get_app_component(component_name=component_name)

def get_infra_metrics_data(component_id=None,start_date=None,end_date=None):
    val=get_infra_component_id(component_name='Overview')
    if component_id == val[0].get('component_id'):
        resp = get_metrics_totals(start_date, end_date)
    else:
        resp =get_metrics(component_id, start_date, end_date, json_flag=True)
    return resp

def get_app_metrics(component_id=None,start_date=None,end_date=None,component_name=None):
    resp=[]
    jsn = {}
    cat_array = [appmetric.Successful_Changes.metrics_col, appmetric.Changes_Rolled_Back.metrics_col,
                 appmetric.Changes_with_Issues.metrics_col, appmetric.Planned_Changes.metrics_col]
    (sum_list, date_fmt) = get_value_calculate_sum(component_id=component_id, category_array=cat_array,
                                                   start_date=start_date, end_date=end_date,release_type=1)
    second_string = cat_array
    if component_name == 'Core_Ops':
        first_string = "Core_Ops_Release_Metrics"
    elif component_name == 'Salesforce':
        first_string = "Salesforce_Release_Metrics"
    elif component_name == 'STE':
        first_string = "STE_Release_Metrics"
    jsn[first_string] = create_json(second_string=second_string, data_lst=sum_list)

    subcomp_name = [subcomp.eSign_Access.metrics_col, subcomp.Underwriting.metrics_col]
    if component_name == 'STE':
        sub_id=0
        for sub in subcomp_name:
            first_string = "STE_Release_Metrics"
            first_string = first_string + '_' +sub
            subcomp_id=db_api.get_app_subcomponent(subcomponent_name=sub)
            sub_id = subcomp_id[0]['subcomponent_id']
            (sum_list, date_fmt) = get_value_calculate_sum(component_id=component_id, category_array=cat_array,
                                                           start_date=start_date, end_date=end_date,release_type=1,subcomponent_id=sub_id)
            jsn[first_string] = create_json(second_string=second_string, data_lst=sum_list)
    else:
        for sub in subcomp_name:
            first_string = "STE_Release_Metrics"
            first_string = first_string + '_' + sub
            jsn[first_string] = {}
    cat_array = [appmetric.SonarQube_Major.metrics_col, appmetric.SonarQube_Critical.metrics_col,
                 appmetric.SonarQube_Blocker.metrics_col]
    (sum_list, date_fmt) = get_value_calculate_sum(component_id=component_id, category_array=cat_array,
                                                   start_date=start_date, end_date=end_date,release_type=1)


        
    second_string = cat_array
    if component_name == 'Core_Ops':
        first_string = "Core_Ops_Quality_Metrics"
    elif component_name == 'Salesforce':
        first_string = "Salesforce_Quality_Metrics"
    elif component_name == 'STE':
        first_string = "STE_Quality_Metrics"
    jsn[first_string] = create_json(second_string=second_string, data_lst=sum_list)
    if component_name == 'STE':
        sub_id=0
        for sub in subcomp_name:
            first_string = "STE_Quality_Metrics"
            first_string = first_string + '_' +sub
            subcomp_id=db_api.get_app_subcomponent(subcomponent_name=sub)
            sub_id = subcomp_id[0]['subcomponent_id']
            (sum_list, date_fmt) = get_value_calculate_sum(component_id=component_id, category_array=cat_array,
                                                           start_date=start_date, end_date=end_date,release_type=1,subcomponent_id=sub_id)
            jsn[first_string] = create_json(second_string=second_string, data_lst=sum_list)
    else:
        for sub in subcomp_name:
            first_string = "STE_Release_Metrics"
            first_string = first_string + '_' + sub
            jsn[first_string] = {}

    return jsn


def get_app_metrics_data(component_id=None,start_date=None,end_date=None):
    val=db_api.get_app_component(component_id=component_id)
    resp=get_app_metrics(component_id=component_id,start_date=start_date,end_date=end_date,component_name=val[0].get('component_name'))
        
    return resp