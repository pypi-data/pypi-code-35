#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import socket
import ssl
import traceback

import time
from _thread import start_new_thread
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from homevee import translate
from homevee.Helper import Logger
from .Helper import compression
from .Helper.helper_functions import remote_control_enabled
from .API import process_data
from .constants import END_OF_MESSAGE
from .db_utils import get_database_con, set_server_data, get_server_data

CLOUD_URL = "premium.cloud.homevee.de"
CLOUD_PORT = 7778

#Verbindung zu Cloud herstellen

#Auf Befehl warten, ausführen und Ergebnis zurück an Server senden

def cloud_connection_loop():
    db = get_database_con()
    REMOTE_ID, ACCESS_TOKEN = get_remote_data(db)
    if REMOTE_ID is None or ACCESS_TOKEN is None:
        REMOTE_ID, ACCESS_TOKEN = register_to_cloud(db)
        # Logger.log("NO CLOUD CONNECTION CREDENTIALS")

    print(translate('your_remote_id_is') + REMOTE_ID)

    while(True):
        connect_to_cloud()

def keep_connection_alive(conn, time):
    while True:
        try:
            #Send some data every minute
            time.sleep(time)
            Logger.log("sending ping")
            conn.send(1)
        except:
            break

def connect_to_cloud():
    db = get_database_con()

    conn = None

    if(not remote_control_enabled(db)):
        #Logger.log("REMOTE CONTROL NOT ENABLED")
        #time.sleep(5 * 60)  # 5 Minuten warten
        return

    cloud_to_use = get_cloud_to_use(db)

    if cloud_to_use is not None:
        Logger.log("using cloud: "+cloud_to_use)
    else:
        cloud_to_use = 'free.cloud.homevee.de'
        Logger.log("using default cloud: "+cloud_to_use)

    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #conn.settimeout(5*60)

        #conn.connect((CLOUD_URL, CLOUD_PORT))

        #Logger.log("Connected")

        '''
        conn = ssl.wrap_socket(conn,
                                     ca_certs=SSL_FULLCHAIN,
                                     cert_reqs=ssl.CERT_REQUIRED,
                                     ssl_version=ssl.PROTOCOL_SSLv23)
        '''

        #SSL aktivieren
        conn = ssl.wrap_socket(conn)

        #Logger.log("Wrapping SSL")

        #Logger.log(("Connecting to cloud ("+CLOUD_URL+")..."))
        conn.connect((cloud_to_use, CLOUD_PORT))

        start_new_thread(keep_connection_alive, (conn, 60))

        #print ("SSL connected")

        #Logger.log("Connection successful!")

        REMOTE_ID, ACCESS_TOKEN = get_remote_data(db)

        data_dict = {'access_token': ACCESS_TOKEN, 'remote_id': REMOTE_ID}

        data = json.dumps(data_dict)+END_OF_MESSAGE

        len_send = conn.send(bytes(data, 'utf-8'))

        while 1:
            try:
                data = conn.recv(8192).decode('utf-8')
            except:
                data = None

            if data is None or data == "":
                db.close()
                conn.close()
                return

            Logger.log("")
            Logger.log(("Received from Cloud: " + data))

            data_parts = data.split(END_OF_MESSAGE)

            for data_part in data_parts:
                if data_part is None or data_part == "":
                    continue

                Logger.log("")
                Logger.log(data_part)

                data_dict = json.loads(data_part)

                if 'result' in data_dict:
                    Logger.log(data_dict)

                    if(data_dict['result'] == "error"):
                        Logger.log("couldn't connect to cloud")
                        time.sleep(60) #1 Minute warten
                else:
                    Logger.log("Processing data:")
                    Logger.log(data_dict)
                    try:
                        client_id = data_dict['client_id']

                        data_dict = json.loads(data_dict['msg'])

                        msg = process_data(data_dict, db)

                        #start_time = time.time()
                        #compressed_message = compression.compress_string(msg)
                        #end_time = time.time()

                        #print "uncompressed: " + str(len(msg))
                        #print "compressed: " + str(len(compressed_message)) + ", time: " + str(end_time - start_time)
                        #compressed_message = compressed_message.decode('iso-8859-1').encode('utf8')

                        data = {}
                        data['msg'] = msg
                        data['client_id'] = client_id
                        data = json.dumps(data)

                        if data is None:
                            data = {'status': 'error'}
                            data['client_id'] = client_id
                            data = json.dumps(data)
                        #else:
                        #    data['client_id'] = client_id
                        #    data['msg'] = json.dumps(msg)
                        #    data = json.dumps(data)

                        data_to_send = data+END_OF_MESSAGE

                        len_send = conn.send(data_to_send.encode('utf-8'))

                        Logger.log(("Sent to remote Server ("+data_dict['action']+")(client: "+str(client_id)+"): "+data))
                    except Exception as e:
                        #traceback.print_exc()
                        if 'status' in data_dict:
                            if data_dict['status'] == 'connectionok':
                                Logger.log('connectionok')
                                pass
                            if data_dict['status'] == 'nocredentials':
                                #Credentials wrong
                                #deleting them from db
                                with db:
                                    #Logger.log("wrongcredentials")
                                    time.sleep(60) #1 Minute warten
                                    #cur = db.cursor()
                                    #cur.execute("DELETE FROM SERVER_DATA WHERE KEY IN ('REMOTE_ID', 'REMOTE_ACCESS_TOKEN')")

    except Exception as e:
        #do not print errors
        traceback.print_exc()
        time.sleep(5)

        if conn is not None:
            conn.close()

    db.close()

def save_remote_control_data(remote_id, access_token, db):
    with db:
        cur = db.cursor()

        #cur.execute("INSERT INTO SERVER_DATA (KEY, VALUE) VALUES (:key, :value)",
        #            {'key': 'REMOTE_ID', 'value': remote_id})
        #cur.execute("INSERT INTO SERVER_DATA (KEY, VALUE) VALUES (:key, :value)",
        #            {'key': 'REMOTE_ACCESS_TOKEN', 'value': access_token})

        REMOTE_ID, REMOTE_SECRET = get_remote_data(db)

        if REMOTE_ID is None or REMOTE_SECRET is None:
            Logger.log("insert remote data")
            cur.execute("INSERT INTO SERVER_DATA (KEY, VALUE) VALUES ('REMOTE_ID', :remote_id)",
                    {'remote_id': remote_id})
            cur.execute("INSERT INTO SERVER_DATA (KEY, VALUE) VALUES ('REMOTE_ACCESS_TOKEN', :token)",
                    {'token': access_token})
        else:
            Logger.log("update remote data")
            cur.execute("UPDATE SERVER_DATA SET VALUE = :remote_id WHERE KEY = 'REMOTE_ID'",
                {'remote_id': remote_id})

            cur.execute("UPDATE SERVER_DATA SET VALUE = :token WHERE KEY = 'REMOTE_ACCESS_TOKEN'",
                {'token': access_token})

#Returns a tuple: (REMOTE_ID, PRIVATE_KEY)
def get_remote_data(db):
    with db:
        cur = db.cursor()

        #cur.execute("DELETE FROM SERVER_DATA WHERE KEY IN ('REMOTE_ACCESS_TOKEN', 'REMOTE_ID')")

        cur.execute("SELECT VALUE FROM SERVER_DATA WHERE KEY = 'REMOTE_ID'")

        result = cur.fetchone()

        if(result is None):
            return None, None
        else:
            remote_id = result['VALUE']
            #Logger.log(("Die Remote-ID lautet: "+remote_id))

        cur.execute("SELECT VALUE FROM SERVER_DATA WHERE KEY = 'REMOTE_ACCESS_TOKEN'")

        result = cur.fetchone()

        if(result is None):
            return None, None
        else:
            remote_access_token = result['VALUE']
            #Logger.log(("Access Token: "+remote_access_token))

    return (remote_id, remote_access_token)

def get_cloud_to_use(db):
    REMOTE_ID, ACCESS_TOKEN = get_remote_data(db)

    url = 'https://cloud.homevee.de/server-api.php'  # Set destination URL here
    post_fields = {'action': 'getcloudtouse',
                   'remoteid': REMOTE_ID,
                   'accesstoken': ACCESS_TOKEN}  # Set POST fields here

    #Logger.log(url+"?action=getcloudtouse&remoteid="+REMOTE_ID+"&accesstoken="+ACCESS_TOKEN)

    request = Request(url, urlencode(post_fields).encode())
    response = urlopen(request).read().decode()

    try:
        data = json.loads(response)
        return data['cloud']
    except:
        return None

def register_to_cloud(db):
    url = 'https://cloud.homevee.de/server-api.php'  # Set destination URL here
    post_fields = {'action': 'generateremoteid'}  # Set POST fields here

    request = Request(url, urlencode(post_fields).encode())
    response = urlopen(request).read().decode()

    data = json.loads(response)

    remote_id = data['remote_id']
    access_token = data['access_token']

    #Logger.log("Deine Remote-ID lautet: "+remote_id)

    #save remote id
    set_server_data("REMOTE_ID", remote_id, db)
    set_server_data("REMOTE_ACCESS_TOKEN", access_token, db)

    return remote_id, access_token

def register_to_cloud_2(db):
    try:
        Logger.log("Registrating at cloud...")
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #conn.connect((CLOUD_URL, CLOUD_PORT))

        #Logger.log("Connected")
        '''
        conn = ssl.wrap_socket(conn,
                                   ca_certs=SSL_FULLCHAIN,
                                   cert_reqs=ssl.CERT_REQUIRED,
                                   ssl_version=ssl.PROTOCOL_SSLv23)
        '''
        #Logger.log("Wrapping SSL")

        # SSL aktivieren
        conn = ssl.wrap_socket(conn)

        conn.connect((CLOUD_URL, CLOUD_PORT))

        #print ("SSL connected")

        len_send = conn.send('registration'+END_OF_MESSAGE)

        #Logger.log("Sent data")

        while 1:
            data = conn.recv(8192)

            if data == "":
                db.close()
                conn.close()
                return
            #Logger.log(("Received: " + data))

            data_dict = json.loads(data)

            if 'result' in data_dict:
                if data_dict['result'] == "registrationok":
                    remote_id = data_dict['remote_id']
                    access_token = data_dict['access_token']

                    save_remote_control_data(remote_id, access_token, db)

                    Logger.log("Registration successful!")

                    return remote_id, access_token

    except Exception as e:
        traceback.print_exc()