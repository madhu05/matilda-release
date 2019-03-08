import pandas as pd
import json,sys
import numpy as np
from matilda_release.db import api as db_api
from matilda_release.db.sqlalchemy import models
from datetime import datetime
from matilda_release.util.status_helper import Appcat_table_Definition as metric
from matilda_release.api.v2.handler import metrics_handler
from matilda_release.util.status_helper import Appsubcomp_table_Definition as subcomp

def read_excel(excel_name=None,st_name=None,startrow=None,intrval=None):
    data=pd.read_excel(excel_name,sheet_name=st_name,header=startrow,index_col=None,interval=intrval)
    cat_array=[]
    subcat_array=[]
    metrics_subcat = []
    metrics=[]
    dt_key=[]
    print('Headers',data.keys())
    if st_name =='STE':
        cat_array.append(st_name)
        dt=data.loc[data.Category != 'Category','Category']
        print('datakk',data)
        dt1=data.loc[(data['App'] != 'App') & (data.App.notnull()) & (data.App != 'STE'),'App']
        print('processed-data',dt.unique(),dt1.unique())
        cat = dt.unique()
        metrics_temp=dt1.unique()
        metrics_subcat=subcomponent_lookup(metrics_temp)
        cat1=[x for x in cat if isinstance(x,str)]
        subcat_temp=category_lookup(cat1)
        subcat_array=[subcat_temp[:4],subcat_temp[4:7]]
        print(data.shape,dt.shape)
        ind=2
        i =ind
        keys=list(data.keys())
        while i < (len(keys)):
            print(keys[i],':',data[keys[i]])
            print('length',len(data[keys[i]]))
            dt_key.append(datetime.strftime(keys[i], '%m/%d/%Y'))
            data[keys[i]].replace(np.nan, 0, inplace=True)
            feature_temp=list(data[keys[i]])[:9]
            qa_temp=list(data[keys[i]])[16:23]
            f_temp=[x for x in feature_temp if not isinstance(x,datetime)]
            q_temp=[x for x in qa_temp if not isinstance(x,datetime)]
            feature_arr=[f_temp[:4],f_temp[4:len(f_temp)]]
            qa_arr=[q_temp[:3],q_temp[3:len(q_temp)]]
            metrics.append([feature_arr,qa_arr])

            i+=1
    elif st_name =='Core Ops' or st_name=='Salesforce':
        if st_name=='Core Ops':
            cat_array.append('Core_Ops')
        else:
            cat_array.append(st_name)
        dt1=data.loc[(data['App'] != 'App') & (data.App.notnull()) & (data.App != 'STE'),'App']
        metrics_subcat=dt1.unique()
        ind = 2
        i = ind
        keys = list(data.keys())
        while i < (len(keys)):
            print(keys[i], ':', data[keys[i]])
            print('length', len(data[keys[i]]))
            dt_key.append(datetime.strftime(keys[i], '%m/%d/%Y'))
            data[keys[i]].replace(np.nan, 0, inplace=True)
            feature_temp = list(data[keys[i]])[:4]
            qa_temp = list(data[keys[i]])[4:8]
            f_temp = [x for x in feature_temp if not isinstance(x, datetime)]
            q_temp = [x for x in qa_temp if not isinstance(x, datetime)]
            metrics.append([f_temp,q_temp])
            i+=1

    return(cat_array,metrics_subcat,subcat_array,metrics,dt_key)


def create_app_category(datak):
    for dat in datak:
        sof = models.AppMetricsCategory()
        sof.category_name = dat
        db_api.create_app_category(sof)


def create_app_subcomponent(datak):
    for dat in datak:
        sof = models.AppMetricsSubComponent()
        sof.subcomponent_name = dat
        db_api.create_app_subcomponent(sof)


def create_app_component(datak):
    for dat in datak:
        sof = models.AppMetricsComponent()
        sof.component_name = dat
        db_api.create_app_component(sof)

def category_lookup(category):
    category_db = []
    for i in range(len(category)):
        if metric.Planned_Changes.sheet_col == category[i]:
            category_db.append(metric.Planned_Changes.metrics_col)
        elif metric.Changes_with_Issues.sheet_col == category[i]:
            category_db.append(metric.Changes_with_Issues.metrics_col)
        elif metric.Changes_Rolled_Back.sheet_col == category[i]:
            category_db.append(metric.Changes_Rolled_Back.metrics_col)
        elif metric.Successful_Changes.sheet_col == category[i]:
            category_db.append(metric.Successful_Changes.metrics_col)
        elif metric.SonarQube_Blocker.sheet_col == category[i]:
            category_db.append(metric.SonarQube_Blocker.metrics_col)
        elif metric.SonarQube_Critical.sheet_col == category[i]:
            category_db.append(metric.SonarQube_Critical.metrics_col)
        elif metric.SonarQube_Major.sheet_col == category[i]:
            category_db.append(metric.SonarQube_Major.metrics_col)
        else:
            category_db.append(category[i])

    return category_db

def subcomponent_lookup(sub):
    sub_db=[]
    for i in range(len(sub)):
        if subcomp.eSign_Access.sheet_col == sub[i]:
            sub_db.append(subcomp.eSign_Access.metrics_col)
        else:
           sub_db.append(sub[i])
    return sub_db


def create_app_metrics(id=None,subid=None,cat_id=None,date_val=None,datak=None):
    #for i in range(len(datak)):
    sof = models.AppMetrics()
    sof.component_id = id
    sof.subcomponent_id=subid
    sof.category_id=cat_id
        #a=datak[0]
    sof.metrics=datak
    sof.date = datetime.strptime(date_val, '%m/%d/%Y')
    db_api.create_app_metrics(sof)

def process_metrics(component=None,subcomponent=None,category=None,data=None,date1=None,st_name=None):
    out=[]
    outcat=[]
    tempcomp_id=[]
    for comp in subcomponent:
        tempcomp_id.append(db_api.get_app_subcomponent(subcomponent_name=comp))

    subcomp_id=[x[0]['subcomponent_id'] for x in tempcomp_id]
    for cat3 in category:
        tempcat=[]
        for cat4 in cat3:
            tempcat_id = db_api.get_app_category(category_name=cat4)
            tempcat.append(tempcat_id[0].get('category_id'))
        outcat.append(tempcat)
    if st_name=='STE':
        for comp in component:
            comp_id=db_api.get_app_component(component_name=comp)
            for (dt1,dtval) in zip(data,date1):
                for (dt2,cat) in zip(dt1,outcat):
                    for (dt3,subcomp)  in zip(dt2,subcomp_id):
                        for (dt4,cat1)  in zip(dt3,cat):
                            out.append([comp_id,dtval,subcomp,cat1,dt4])
                            create_app_metrics(id=comp_id[0].get('component_id'),subid=subcomp,cat_id=cat1,date_val=dtval,datak=dt4)
    else:
        for comp in component:
            comp_id=db_api.get_app_component(component_name=comp)
            for (dt1,dtval) in zip(data,date1):
                for (dt2,cat) in zip(dt1,outcat):
                    for subcomp  in subcomp_id:
                        for (dt3,cat1)  in zip(dt2,cat):
                            out.append([comp_id,dtval,subcomp,cat1,dt3])
                            create_app_metrics(id=comp_id[0].get('component_id'),subid=subcomp,cat_id=cat1,date_val=dtval,datak=dt3)

    print('out',out)
    return

def main():
    for arg in sys.argv[1:]:
        if arg == 'create_supporttbl':

            '''(component,subcomponent,category,dt,date_array) = read_excel(excel_name='App_Release_Metrics_12212018.xlsx', \
                                           st_name='STE',startrow=1,intrval=4)
            #create_app_component(component)'''
            '''create_app_subcomponent(subcomponent)
            for cat in category:
                create_app_category(cat)'''
            '''save_cat=category
            process_metrics(component=component,subcomponent=subcomponent,category=category,data=dt,date1=date_array,st_name='STE')
            (component,subcomponent,category,dt,date_array) = read_excel(excel_name='App_Release_Metrics_12212018.xlsx', \
                                                                         st_name='Core Ops',startrow=1,intrval=4)'''
            #create_app_component(component)
            '''create_app_subcomponent(subcomponent)'''
            '''process_metrics(component=component,subcomponent=subcomponent,category=save_cat,data=dt,date1=date_array,st_name='Core Ops')
            (component,subcomponent,category,dt,date_array) = read_excel(excel_name='App_Release_Metrics_12212018.xlsx', \
                                                                         st_name='Salesforce',startrow=1,intrval=4)
            process_metrics(component=component,subcomponent=subcomponent,category=save_cat,data=dt,date1=date_array,st_name='Salesforce')'''
            #create_app_component(component)
            '''create_app_subcomponent(subcomponent)'''
            metrics_handler.get_app_metrics_data(component_id=2, start_date='9-1-2018',end_date='1-1-2019')

if __name__=='__main__':
    main()
    print('hello_world')
