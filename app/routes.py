from app import app
from flask import request, jsonify, render_template,redirect, url_for, flash, send_from_directory, session, make_response
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

os.environ["DEEPINFRA_API_TOKEN"] = "HTj80cPBu4Qaiw80oIUZAs6J9Nzg73XK"
CHAT_MODEL = 'meta-llama/Meta-Llama-3-70B-Instruct'

# messsages placeholder
info = '''
Anthony Estrada, a 30-year-old Filipino data engineer and analyst, sat in front of his computer, sipping his morning coffee and staring at the lines of code on his screen. He was working on a project for a major Philippine bank, building a predictive model to forecast credit risk for their clients.
As he worked, Anthony's mind wandered back to his childhood in the bustling streets of Manila. Growing up, he was always fascinated by numbers and patterns. He spent hours playing with his calculator, creating complex math problems for himself to solve. His parents, both teachers, encouraged his curiosity, gifting him books on programming and statistics.
After completing his degree in Computer Science from the Jose Rizal University, Anthony landed a job at a small data analytics firm. He quickly proved himself to be a rising star, impressing his colleagues with his attention to detail and creative problem-solving skills.
But Anthony's true passion was using data to drive social impact. He spent countless hours volunteering for non-profits, helping them analyze and visualize data to inform their policy decisions. His work caught the attention of the Philippine government, who offered him a grant to build a data platform for tracking poverty rates across the country.
Anthony's project, dubbed "Tala" (meaning "star" in Filipino), used machine learning algorithms to identify areas of high poverty and recommend targeted interventions. The platform was a huge success, earning Anthony recognition from the international data science community.
Now, as a senior data engineer at a leading fintech company, Anthony was working on some of the most complex data projects in the country. But he never forgot his roots, always looking for ways to apply his skills to make a positive difference in the lives of Filipinos.
As he finished his coffee, Anthony refocused on his screen, ready to tackle the next challenge in his code. He smiled to himself, knowing that the work he was doing would help shape the future of the Philippines, one data point at a time.
'''

messages_template = [
     SystemMessage(
            content=(
                f"You are a helpful assistant named Chesa You will only answer questions about Anthony Estrada. here is the information about him {info}"
                
            )
     )
]

messages = [
     SystemMessage(
            content=(
                f"You are a helpful assistant named Chesa You will only answer questions about Anthony Estrada. here is the information about him {info}"
                
            )
     )
]


@app.route('/')
@app.route('/index')
def index():

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

@app.route('/contact')
def contact():

    return render_template('index.html')

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



