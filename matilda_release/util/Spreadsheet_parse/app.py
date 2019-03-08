from flask import Flask,render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
import pandas as pd
import json

basedir=os.path.abspath(os.path.dirname(__file__))


app=Flask(__name__)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

app.config['UPLOAD_FOLDER'] = basedir
#basedir =os.path.abspath(os.path.dirname(app.config['UPLOAD_FOLDER']))


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/upload', methods=['POST','GET'])
def upload_files():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        flash("your file is saved on the database")


    return redirect(url_for('output'))

@app.route('/output')
def output():

    class Excel:

        def computersystem_list(self):
            data = pd.read_excel(app.config['UPLOAD_FOLDER']+'/ServerExportTabbed.xlsx', sheet_name='Computer System')
            self.task1 = input('Enter your operating system').strip()  # EX:- Oracle Linux 6.9
            data = data[data['Operating System'] == self.task1]
            out = data[['Computer System Name', 'Hostname', 'Environment', 'Operating System']]
            self.req = out.values.tolist()
            self.out_json_noindex = out.to_json(orient='records')
            print(self.out_json_noindex)
            self.jb = json.loads(self.out_json_noindex)
            # print(type(jb))

        def relationtype_list(self):

            data1 = pd.read_excel(app.config['UPLOAD_FOLDER']+'/ServerExportTabbed.xlsx', sheet_name='Relationships')
            self.task2 = input('Enter your relation item').strip()  # EX:- Computer System Name
            j = json.loads(self.out_json_noindex)
            p = []
            for i in j:
                k = i[self.task2]
                p.append(k)

            f = len(p)

            self.w = []
            for j in range(f):
                data2 = data1[data1['Computer System Name'] == p[j]]
                output = data2[['Computer System Name', 'Related Item', 'Related Type']].set_index(
                    'Computer System Name')
                self.w.append(output.to_json(orient='records'))
            print(self.w)

        def output(self):

            self.d = {}
            for i in range(len(self.req)):
                self.d[tuple(self.jb[i].items())] = self.w[i]

            print(self.d)

    p = Excel()
    p.computersystem_list()
    p.relationtype_list()
    p.output()
    c=p.d



    return render_template('thankyou.html',my_variable=c,my_variable1=p.task1,my_variable2=p.task2)

if __name__ == '__main__':
    app.run(debug=True)



