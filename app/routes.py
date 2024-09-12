from. import app, db
from flask import request, jsonify, render_template,redirect, url_for, flash, send_from_directory, session, make_response, flash
import json
import base64
import random # for removal for dev only
from datetime import datetime, timedelta
import requests
import os
import sqlite3
from werkzeug.utils import secure_filename
import uuid
import pickle
# AI libs
from langchain_community.chat_models import ChatDeepInfra
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler



from app.models import  Pages, Messages as DBMessage

os.environ["DEEPINFRA_API_TOKEN"] = "HTj80cPBu4Qaiw80oIUZAs6J9Nzg73XK"
CHAT_MODEL = 'meta-llama/Meta-Llama-3-70B-Instruct'

# messsages placeholder
info = '''
Anthony Estrada, A Filipino data engineer and analyst. Graduated at Jose Rizal University on year 2009. He has 12 years working experience in I.T industry. He started his career as Software engineer creating applications using
C#, ASP.net, PHP, Javascript and Python. He design applications using advance design patters like MVC. His journey in data engineering and analytics started when he is working at 
Isuzu Automotive dealership (2012 - 2015). After completing data related projects like data migration (Data Centralization, SSIS, MSSQL), data warehouse creation (SSIS and MS SQL)
and implementing business intelligence solution (QLIKView) he decided to more focused on that area. On Year 2016, He joined Asurion as Business Intelligence Developer. Started as 
contractor then after six months got absorbed as Team Lead of business intelligence team. The usual things he do at Aurion are create and design data warehouse using medallion concept
creating end-to-end reporting and analytics solution, perform couching to his colleague  and conduct training to other site and department in using Power BI. He also finished 3 big 
projects at Asurion. This are the reporting platform migration, data warehouse source migration and migration of data warehouse to AWS redshift Mysql. This is where he gain his
skill in cloud technologies like Azure Synapse, Data Factory, Databricks, Denodo and AWS Red Shift. On Nov 2022, he joined STMicroelectronics as Senior Engineer for Analystics. He 
got regularized after 3 month after deploying analytic implmenting self service solution using Power BI, Dataflow and Maria DB. He worked with Oracle and Mariadb for databases. 
Talend and Python Talend. Currently he is implementing Apache Airflor and deploying Microsoft Fabric. He is currently involve in data centralization project for ASIA sites. He continuesly
data engineering, data science and analytics to ensure he upgrades his skill progresively. He got training for Google Advance Analytics, Microsoft Certification for Azure Data Fundamental
and Azure Fabric Associate certificate. 
'''



messages = [
     SystemMessage(
            content=(
               f"You are a helpful assistant named Chesa You will only answer questions about Anthony Estrada.here is the information about him {info}"
                "if the user wish to contact anthony ask for email and phone number."
                "you can give his contact information which is antzestrada@outlook.com for email and https://www.linkedin.com/in/esthony/ for linkedin. only if they ask"
                 
            )
     )
]


@app.route('/')
@app.route('/index')
def index():

    '''
    pages = Pages.query.all()
    for page in pages:
        print(page.title, page.content)
    '''

    return render_template('index.html')

@app.route('/portpolio')
def portpolio():

    return render_template('portpolio.html')

@app.route('/chat')
def chat():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())  # generate a unique ID
        print(f"new user: {session['user_id']}")
    else:
        print(f"User has returned! {session['user_id']}")
    
    return render_template('chat.html')

@app.route('/contact',methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        u_name = request.form.get('name')
        u_email = request.form.get('email')
        u_subject = request.form.get('subject')
        u_message = request.form.get('message')

        print(f"name: {u_name}, email: {u_email}, subject: {u_subject}, msg: {u_message}")

        new_message = DBMessage(uname=u_name, email=u_email, subject=u_subject, msg=u_message)

        # Add the instance to the session and commit
        db.session.add(new_message)
        db.session.commit()
        flash('Your message is sent. Will contact you soon..')
      

        

    return render_template('contact.html')

@app.route('/services')
def services():
    return render_template('services.html')



@app.route('/chatx', methods=['POST'])
def chatx():

    data = request.get_json()  # Use request.form instead of request.get_json()
    msg = data.get('message')
    print(f"HUman message: {msg}")

    if msg == None:
        msg = "Who are you?" 


    chat = ChatDeepInfra(model=CHAT_MODEL) 

    add_human_message(msg)

    res = chat.invoke(messages)
    add_ai_message(res.content)
    print(res.content)
    print(type(res))

    # store to session handler
    # Serialize the SystemMessage objects using pickle
    messages_pickle = pickle.dumps(messages)

    # Store the serialized messages in a session
    session['messages'] = messages_pickle

        
   
    response = make_response(jsonify({'message': res.content}))
  
    print("compleed")
    return response
    #print(data)
    # Process the data
   # return jsonify({'message': 'Chat message received!'})

@app.route('/chat2')
async def chat2():
  chat = ChatDeepInfra(model=CHAT_MODEL)
  await chat.agenerate([messages])

@app.route('/chat3')
def chat3():
  chat = ChatDeepInfra(
      streaming=True,
      verbose=True,
      callbacks=[StreamingStdOutCallbackHandler()],
)
  print(chat.invoke(messages))

def add_ai_message(content):
    messages.append(AIMessage(content=content))

def add_human_message(content):
    messages.append(HumanMessage(content=content))



