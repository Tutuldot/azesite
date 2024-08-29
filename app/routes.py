from app import app
from flask import request, jsonify, render_template,redirect, url_for, flash, send_from_directory
import json
import base64
import random # for removal for dev only
from datetime import datetime
import requests
import os
import sqlite3
from werkzeug.utils import secure_filename


@app.route('/')
@app.route('/index')
def index():

    return render_template('index.html')

@app.route('/portpolio')
def portpolio():

    return render_template('portpolio.html')

@app.route('/chat')
def chat():

    return render_template('chat.html')

@app.route('/contact')
def contact():

    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')
'''

@app.route('/configuration',methods=['GET', 'POST'])
def configuration():
    c_schema = load_schema()
    json_data = []
    uploaded_json = None
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file_content = file.read()
            uploaded_json = json.loads(file_content.decode('utf-8'))
            filename = secure_filename(file.filename)
            
            try:
                validate(instance=uploaded_json, schema=c_schema)
            except ValidationError as e:
                flash('Invalid Json Format. Please refer to existing uploaded files.')
                return redirect(request.url)
            except json.JSONDecodeError:
                flash('Invalid Json File. Please check content')
                return redirect(request.url)
            except Exception as e:
                flash('Error on uploaded file: {}'.format(str(e)))
                return redirect(request.url)
            
            uploaded_machine = uploaded_json[0]['name']

            uploaded_formats = uploaded_json[0]['files_to_monitor']

            for i in uploaded_formats:
                check_machine(uploaded_machine,i['type'])

            #file.save(current_path + directory + "/" + filename)
            flash('File successfully uploaded! {}'.format(uploaded_json[0]['name']))
            return redirect(url_for('configuration'))
        else:
            flash('Allowed file types are .json')
            return redirect(request.url)

    
    json_files = [f for f in os.listdir(current_path + directory) if f.endswith('.json')]
    

    for file_name in json_files:
        file_path = os.path.join(current_path + directory, file_name)
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            json_data.append({'file_name': file_name, 'content': data})

    return render_template('conf_home.html', json_data=json_data, current_path = current_path, uploaded_json = uploaded_json)

@app.route('/delete-config/<string:config_name>', methods=['POST'])
def delete_config(config_name):

# Ensure the filename is secure and prevent directory traversal attacks
  
    filename = secure_filename(config_name)
    
    # Construct the full file path
    file_path = current_path + directory + "/" + filename
    
    # Check if the file exists
    if os.path.exists(file_path):
        # Delete the file
        os.remove(file_path)
        flash('Config file {} successfully deleted'.format(config_name))
    else:
        flash('File not found')

    
    return redirect(url_for('configuration'))



@app.route('/download/<filename>')
def download_file(filename):
  
    try:
        return send_from_directory(current_path + directory, filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)


@app.route('/data')
def data():

    result = get_machines_logs()
    html_table = result.to_html(index=False, classes='table table-striped')
   

    return render_template('data.html', html_table = html_table)

@app.route('/settings')
def settings():
   
  

    return render_template('setting.html')

@app.route('/categorize', methods=['POST'])
def categorize():

    # handling of post data
    test_type = None
    message = request.json.get('message')
    test_type = request.json.get('test_type') # expected value is blank or Yes
    if not message:
        return jsonify({"error": "No message provided"}), 400

    if not test_type:
        test_type = "NA"
    


    #output to api
    return jsonify({"message": message, "result": test_type})



# functions here

def get_all_log_count():

    conn = sqlite3.connect('data/database.db')
    query = "SELECT * FROM machine_log_count"
    machine_log_count_df = pd.read_sql_query(query, conn)
    
    # Close the connection
    conn.close()
    return machine_log_count_df


def pivot_machines(dff):
    df_logs = pd.DataFrame(dff, columns=['created', 'machine_name', 'log_count'])
    df_logs['created'] = pd.to_datetime(df_logs['created'])
    df_logs['created'] = df_logs['created'].dt.strftime('%b %d')
    # Pivot the DataFrame to get 'Machine_Name' as columns and 'Date' as rows
    df_pivoted = df_logs.pivot_table(index='created', columns='machine_name', values='log_count', fill_value=0)

    labels = df_pivoted.index.tolist()
    machine_names  = df_logs['machine_name'].unique().tolist()

    datasets = []
    for column in df_pivoted.columns:
            datasets.append({
                'label': column,
                'data': df_pivoted[column].tolist(),
                'backgroundColor': 'rgba(54, 162, 235, 1)', # Add your colors
                'borderColor': 'rgba(54, 162, 235, 1)', # Add your colors
                'borderWidth': 1
            })

    return labels, datasets, machine_names

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_schema(schema_path = SCHEMA_PATH):
    """Load JSON schema from a file."""
    with open(schema_path, 'r') as file:
        schema = json.load(file)
    return schema


def check_machine(m_name,m_type):

    try:
        # check if exist
        conn = sqlite3.connect('database.db')

        cursor = conn.cursor()
        query = "SELECT * FROM machine_activity where machine_name = ?"
        cursor.execute(query,(m_name,))
        results = cursor.fetchall()

    

        if len(results) <= 0:
            cursor.execute("INSERT INTO machine_activity (machine_name, current_work_week, current_date,log_type) VALUES (?, ?, ?, ?)",(m_name, 0,'2024-01-01',m_type))


        cursor.close()
        conn.close()

        return True
    except Exception as e:
        return False




def get_machines(m_name = None):


    conn = sqlite3.connect('database.db')

    cursor = conn.cursor()
    query = None
    if m_name == None:
        query = "SELECT * FROM machine_activity"
        cursor.execute(query)
    else:
        query = "SELECT * FROM machine_activity where machine_name = ?" 
        cursor.execute(query,(m_name,))
    
  
    results = cursor.fetchall()

    


    cursor.close()
    conn.close()

    return results



def get_machines_logs(m_name = None, start_date = None, end_date = None):


    conn = sqlite3.connect(current_path + "/data/database.db" )

    cursor = conn.cursor()
    query = None
    if m_name == None:
        if start_date == None:
            query = "SELECT * FROM machine_log_count"
            cursor.execute(query)
        else:
            query = "SELECT * FROM machine_log_count where created between ? and ?"
            cursor.execute(query,(start_date,end_date,))

    else:
        query = "SELECT * FROM machine_log_count where machine_name = ?" 
        cursor.execute(query,(m_name,))
    
  
    results = cursor.fetchall()

    


    cursor.close()
    conn.close()

    return results
    
    


'''
