from flask import Flask, jsonify, request
import re
import logging
import json

# SETTINGS #####
HOST = '0.0.0.0'
PORT = 4000
mask = r'\+7\(\d{3}\)-\d{3}-\d{2}-\d{2}'
################

#пример запроса
#curl -X POST 127.0.0.1:4000/ -d data="{"cmd":"get_data"}"

app = Flask(__name__)

def setup_logger():
    logging.basicConfig(filename="log.log", level=logging.INFO)
    return logging.getLogger("log")

logger = setup_logger()

@app.route('/', methods=['POST'])
def api():
    ''' endpoint '''
    msg = " request - %s" % json.dumps(request.form)
    logger.info(msg)
    
    data = request.form.get('data', None)


    if not data:
        return {"answer": "fail", "status": "error", "msg": "invalid 'data'-params"}
    else:
        data = json.loads(data)

    meth = data.get('cmd', None)
    result = {}
    if meth == 'get_data':
        result = get_data()

    elif meth == 'post_data':
        post = data.get('data', None)
        result = post_data(post)

    else:
        result = {"answer": "fail", "status": "error", "msg": "invalid 'cmd'-params"}

    msg = " response - %s" % json.dumps(result)
    logger.info(msg)

    return jsonify(result)

def get_data():
    return {
        "answer": {
            "field1": [
                {"id": 1, "data": "some_data1"},
                {"id": 2, "data": "some_data2"},
                {"id": 3, "data": "some_data3"}
            ]
        },
        "status": "ok" }

def post_data(data):
    result = {}
    if not data:
        return {"answer": "fail", "status": "error", "msg": "invalid 'data'-params"}

    if not isinstance(data, list):
        return {"answer": "fail", "status": "error", "msg": "'data'-prams isn't array"}
    
    keys = []
    try:
        keys = [x['name'] for x in data]
    except Exception as ex:
        return {"answer": "fail", "status": "error", "msg": "invalid struct 'data'-params"}

    for field in ('field1', 'field2', 'field3'):
        if field in keys:
            continue
        else:
            return {"answer": "fail", "status": "error", "msg": "invalid struct 'data'-params"}

    for obj in data:
        name_field = obj['name']
        if name_field == 'filed1':
            if obj['val'] not in (1, 2, 3):
                return {"answer": "fail", "status": "error", "msg": "invalid value 'field1'-param"}
        
        elif name_field == 'filed2':
            patter = re.compile(mask)
            result = patter.findall(obj['val'])
            if not result:
                return {"answer": "fail", "status": "error", "msg": "invalid value 'field2'-param, mask: %s" % mask}

        elif name_field == 'filed3':
            if len(obj['val']) > 1000:
                return {"answer": "fail", "status": "error", "msg": "invalid value 'field3'-param, val > 1000 chars"}  

    return {"answer": "success", "status": "ok"}

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)