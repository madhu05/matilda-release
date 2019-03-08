import pandas as pd
import numpy as np
import json

data=pd.read_excel('C:/Users/PC_User/Desktop/ServerExportTabbed.xlsx',sheet_name='Computer System')
data1=pd.read_excel('C:/Users/PC_User/Desktop/ServerExportTabbed.xlsx',sheet_name='Relationships')

#print(data)

#----------------------#Task1---------------------------------------#
task1= input('Enter your operating system').strip()    #Oracle Linux 6.9
data=data[data['Operating System'] == task1 ]
out=data[['Computer System Name', 'Hostname', 'Environment', 'Operating System']]

req=out.values.tolist()
#print(req)

out_json_noindex=out.to_json(orient='records')
print(out_json_noindex)
jb=json.loads(out_json_noindex)
print(type(jb))


#---------------------#Task2--------------------------------------#
task2 = input('Enter your relation item').strip()      #Computer System Name
j=json.loads(out_json_noindex)
p=[]
for i in j:
    k=i[task2]
    p.append(k)

f=len(p)

w=[]
for j in range(f):

    data2 = data1[data1['Computer System Name'] == p[j]]
    output = data2[['Computer System Name', 'Related Item', 'Related Type']].set_index('Computer System Name')
    w.append(output.to_json(orient='records'))
print(w)
print(type(w))
#------------------final json output-------------------------------#
d = {}
for i in range(len(req)):
    d[tuple(jb[i].items())] = w[i]

print(d)
print(type(d))


