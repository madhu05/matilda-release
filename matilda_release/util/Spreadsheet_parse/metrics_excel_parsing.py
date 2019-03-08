import pandas as pd
import json,sys
import numpy as np
from matilda_release.db import api as db_api
from matilda_release.db.sqlalchemy import models
from datetime import datetime
from werkzeug.exceptions import BadRequest
from matilda_release.api.v2.handler import metrics_handler
from matilda_release.util.status_helper import Metrics_table_Definition as metric

def read_excel(excel_name=None,st_name=None,startrow=None,startcol=None,intrval=None):
    data=pd.read_excel(excel_name,sheet_name=st_name,header=startrow,index_col=None,interval=intrval)
    #data1=pd.read_excel('2019-Infrastructure_Overall-Summary.xlsx',sheet_name='Server'):
    #print(data.head())
    i =0
    cat_array=[]
    subcat_array=[]
    metrics_subcat = []
    print(len(data))
    print(len(data[intrval*i:intrval*(i+1)]))
    print('Headers',data.keys())
    for col in data['Sub-Category'][intrval * i:intrval * (i + 1)]:
        subcat_array.append(col)
    if st_name != 'Overall Infrastructure Metrics':
        while (intrval*i <len(data)):
            cat_val = data['Component'][(intrval)*i]
            metrics_subcat.append(cat_val)
            data['Component'][intrval*i:intrval*(i+1)]=data['Component'][intrval*i:intrval*(i+1)].replace(np.nan, cat_val)
            #data['Sub-Category'] = data['Sub-Category'].replace(metric.metrics_table.sheet_col,metric.metrics_table.metrics_col)
            #print(data['Component'])
            #print(data['Sub-Category'])
            #dt.append(data['Category'][intrval*i:intrval*(i+1)].fillna(data['Category'][intrval*i]))
            i+=1
        data.replace(np.nan, 0, inplace=True)
        if st_name == 'Server':
            cat_array = ['Server']
        elif st_name == 'Middleware':
            cat_array = ['Middleware']
            metrics_subcat.remove('Totals')
        elif st_name == 'Database':
            cat_array = ['Database']
            metrics_subcat.remove('Totals')
        elif st_name == 'Mainframe':
            cat_array = ['Mainframe']
            metrics_subcat.remove('Totals')
        elif st_name == 'Network':
            cat_array = ['Network']
            metrics_subcat.remove('Totals')

            #print('cat_array',cat_array)
        #print('data',data)
        #print('hello_world')
    else:
        #for col in data['Sub-Category'][intrval*i:intrval*(i+1)]:
        #    subcat_array.append(col)
        #subcat_array = data['Sub-Category'][intrval*i:intrval*(i+1)]
        print('sub-cat',subcat_array)
        while (intrval*i <len(data)):
            cat_val = data['Category'][(intrval)*i]
            cat_array.append(cat_val)
            data['Category'][intrval*i:intrval*(i+1)]=data['Category'][intrval*i:intrval*(i+1)].replace(np.nan, cat_val)
            #data['Sub-Category'] = data['Sub-Category'].replace(metric.metrics_table.sheet_col,metric.metrics_table.metrics_col)
            #print(data['Category'])
            #print(data['Sub-Category'])
            #dt.append(data['Category'][intrval*i:intrval*(i+1)].fillna(data['Category'][intrval*i]))
            i+=1
        data.replace(np.nan, 0, inplace=True)
        print('cat_array',cat_array)
        print('data',data)
        #metrics_subcat = []
        metrics_subcat =['Overview']
    return(cat_array,metrics_subcat,subcat_array,data)


def create_infra_category(datak):
    for i in range(len(datak)):
        sof = models.InfraMetricsCategory()
        sof.category_name = datak[i]
        db_api.create_infra_category(sof)


def create_infra_subcomponent(datak):
    for i in range(len(datak)):
        sof = models.InfraMetricsSubComponent()
        sof.subcomponent_name = datak[i]
        db_api.create_infra_subcomponent(sof)


def create_infra_component(datak):
    for i in range(len(datak)):
        sof = models.InfraMetricsComponent()
        sof.component_name = datak[i]
        db_api.create_infra_component(sof)

def category_lookup(category):
    category_db = []
    for i in range(len(category)):
        if metric.YTD_Changes.sheet_col == category[i]:
            category_db.append(metric.YTD_Changes.metrics_col)
        elif metric.YTD_Changes_ERME_MMW.sheet_col == category[i]:
            category_db.append(metric.YTD_Changes_ERME_MMW.metrics_col)
        elif metric.YTD_Changes_managed_release.sheet_col == category[i]:
            category_db.append(metric.YTD_Changes_managed_release.metrics_col)
        elif metric.YTD_ALL_Changes.sheet_col == category[i]:
            category_db.append(metric.YTD_ALL_Changes.metrics_col)
        elif metric.YTD_ALL_Changes_managed_release.sheet_col == category[i]:
            category_db.append(metric.YTD_ALL_Changes_managed_release.metrics_col)
        elif metric.YTD_ALL_Changes_ERME_MMW.sheet_col == category[i]:
            category_db.append(metric.YTD_ALL_Changes_ERME_MMW.metrics_col)
        elif metric.YTD_Plan_Line.sheet_col == category[i]:
            category_db.append(metric.YTD_Plan_Line.metrics_col)
        elif metric.Release_Churn_Deployed.sheet_col == category[i]:
            category_db.append(metric.Release_Churn_Deployed.metrics_col)
        elif metric.Release_Churn_Planned.sheet_col == category[i]:
            category_db.append(metric.Release_Churn_Planned.metrics_col)
        elif metric.MMW_Statistics_Deployed_Issues.sheet_col == category[i]:
            category_db.append(metric.MMW_Statistics_Deployed_Issues.metrics_col)
        elif metric.MMW_Statistics_Deployed_Success.sheet_col == category[i]:
            category_db.append(metric.MMW_Statistics_Deployed_Success.metrics_col)
        elif metric.MMW_Statistics_Cancelled.sheet_col == category[i]:
            category_db.append(metric.MMW_Statistics_Cancelled.metrics_col)
        elif metric.MMW_Statistics_Incidents.sheet_col == category[i]:
            category_db.append(metric.MMW_Statistics_Incidents.metrics_col)
        else:
            raise BadRequest('Unknown value in spreadsheet {}',format(metric.MMW_Statistics_Incidents.sheet_col ))

    return category_db

def create_infra_metrics(id,subid,date_val,index_val,datak):
    for i in range(len(datak)):
        sof = models.InfraMetrics()
        sof.component_id = id
        sof.subcomponent_id=subid
        sof.category_id=index_val[i]
        #a=datak[0]
        if sof.category_id==3 or sof.category_id==6 or sof.category_id==7:
            sof.metrics=datak[i]*100
        else:
            sof.metrics=datak[i]
        sof.date = datetime.strptime(date_val, '%m/%d/%Y')
        db_api.create_infra_metrics(sof)

def process_metrics(component=None,category=None,data=None,interval=None):
    keys = list(data.keys())
    index = 4
    index_id=[]
    comp = db_api.get_infra_component(component_name=component)
    comp_id = comp[0].get('component_id')
    cat_db = category_lookup(category)
    for l in range(len(cat_db)):
        temp_id=db_api.get_infra_category(category_name=cat_db[l])
        index_id.append(temp_id[0].get('category_id'))
    #update_array = []
    while index < len(keys):
        i =0
        while (interval*i <(len(data)-interval)):
            update_array=[]
            cat_val = data['Component'][(interval)*i]
            subcomponent = db_api.get_infra_subcomponent(subcomponent_name=cat_val)
            update_array[:interval]=data[keys[index]][interval*i:interval*(i+1)]
            print(len(update_array))
            date_val = keys[index]
            create_infra_metrics(comp_id,subcomponent[0].get('subcomponent_id'),date_val,index_id,update_array)
            i+=1
        index+=1

def main():
    for arg in sys.argv[1:]:
        '''if arg == 'create_comp':
            (component,subcomponent,dt) = read_excel(excel_name='2019-Infrastructure_Overall-Summary.xlsx',
                                       st_name='Overall Infrastructure Metrics',startrow=6,startcol=1,intrval=13)
            create_infra_component(component)'''
        if arg == 'create_supporttbl':

            (component,subcomponent,category,dt) = read_excel(excel_name='2019-Infrastructure_Overall-Summary.xlsx',
                                           st_name='Server',startrow=21,startcol=1,intrval=13)
            create_infra_component(component)
            create_infra_subcomponent(subcomponent)
            cat_db=category_lookup(category)
            create_infra_category(cat_db)
            process_metrics(component=component,category=category,data=dt, interval=13)
            (component,subcomponent,category,dt) = read_excel(excel_name='2019-Infrastructure_Overall-Summary.xlsx',
                                           st_name='Middleware',startrow=21,startcol=1,intrval=13)
            create_infra_component(component)
            create_infra_subcomponent(subcomponent)
            (component,subcomponent,category,dt) = read_excel(excel_name='2019-Infrastructure_Overall-Summary.xlsx',
                                           st_name='Database',startrow=21,startcol=1,intrval=13)
            create_infra_component(component)
            create_infra_subcomponent(subcomponent)
            (component,subcomponent,category,dt) = read_excel(excel_name='2019-Infrastructure_Overall-Summary.xlsx',
                                           st_name='Mainframe',startrow=21,startcol=1,intrval=13)
            create_infra_component(component)
            create_infra_subcomponent(subcomponent)
            (component,subcomponent,category,dt) = read_excel(excel_name='2019-Infrastructure_Overall-Summary.xlsx',
                                           st_name='Network',startrow=21,startcol=1,intrval=13)
            create_infra_component(component)
            create_infra_subcomponent(subcomponent)
        elif arg == 'create_tbl':
            (component,subcomponent,category,dt) = read_excel(excel_name='2019-Infrastructure_Overall-Summary.xlsx',
                                                             st_name='Server',startrow=21,startcol=1,intrval=13)
            process_metrics(component=component,category=category,data=dt, interval=13)
            (component,subcomponent,category,dt) = read_excel(excel_name='2019-Infrastructure_Overall-Summary.xlsx',
                                                              st_name='Middleware',startrow=21,startcol=1,intrval=13)
            process_metrics(component=component,category=category,data=dt, interval=13)
            (component,subcomponent,category,dt) = read_excel(excel_name='2019-Infrastructure_Overall-Summary.xlsx',
                                                              st_name='Database',startrow=21,startcol=1,intrval=13)
            process_metrics(component=component,category=category,data=dt, interval=13)
            (component,subcomponent,category,dt) = read_excel(excel_name='2019-Infrastructure_Overall-Summary.xlsx',
                                                              st_name='Mainframe',startrow=21,startcol=1,intrval=13)
            process_metrics(component=component,category=category,data=dt, interval=13)
            (component,subcomponent,category,dt) = read_excel(excel_name='2019-Infrastructure_Overall-Summary.xlsx',
                                                              st_name='Network',startrow=21,startcol=1,intrval=13)
            process_metrics(component=component,category=category,data=dt, interval=13)

if __name__=='__main__':
    #(category,subcategory,dt) = read_excel(excel_name='2019-Infrastructure_Overall-Summary.xlsx',
     #                                      st_name='Overall Infrastructure Metrics',startrow=6,startcol=1,intrval=13)
    #(category,subcategory,dt) = read_excel(excel_name='2019-Infrastructure_Overall-Summary.xlsx',
     #                                      st_name='Mainframe',startrow=21,startcol=1,intrval=13)
    #create_infra_subcategory(subcategory)
    main()
    #ret=db_api.get_infra_metrics(component_id=1, subcomponent_id=None, category_id=1, start_date=datetime.strptime('1/1/2018', '%m/%d/%Y'), end_date=datetime.strptime('12/31/2018', '%m/%d/%Y'))
    #ret=db_api.get_infra_metrics(component_id=1, subcomponent_id=None, category_id=1, start_date=datetime.strptime('1/1/2018', '%m/%d/%Y'), end_date=datetime.strptime('12/31/2018', '%m/%d/%Y'))
    #ret=metrics_handler.get_metrics_totals(component_id=6, start_date='5-1-2018', end_date='12-31-2018')
    #print(ret)
    print('hello_world')
