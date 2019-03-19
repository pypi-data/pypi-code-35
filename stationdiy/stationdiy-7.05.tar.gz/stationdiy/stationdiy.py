########### Dev : Baurin Leza ############
# Cliente MQTT de pruebas


import paho.mqtt.client as mqtt
import requests
import threading
import json
from .decorators import *
import time
from requests import get


class StationDiY():

    def __init__(self, host="stationdiy.eu", username="", port=80,
                 multidevice=True, password="", device="", actioner="",
                 data_actioner="", sensor="", data="", longitud="",
                 latitud="", type_data="string", max_value="",
                 min_value="", mqtt_port = 1883):

        # self.device = device
        # self.sensor = sensor
        # self.data = data
        # self.actioner = actioner
        # self.data_actioner = data_actioner
        # self.longitud = longitud
        # self.latitud = latitud
        # self.type_data = type_data
        # self.multidevice = multidevice
        # self.max_value, self.min_value = max_value, min_value
        try:
            self.ip = get('https://api.ipify.org').text
        except Exception as e:
            self.ip = "0.0.0.0"
        self.host = host
        self.port = port
        self.authenticated = False
        self.url = "http://%s:%s/" % (self.host, self.port)
        self.mqtt_port = mqtt_port

    def connect_mqtt(self):

        """
        Connect MQTT Client
        """

        def on_connect(mqttc, userdata, rc):

            self.connected = True

        def on_publish(mqttc, userdata, mid):

            self.connected = False

        self.mqttc = mqtt.Client()
        self.mqttc.username_pw_set(self.username, password=self.password)
        self.mqttc.on_connect = on_connect
        self.mqttc.on_publish = on_publish

        self.mqttc.connect(
            host=self.host,
            port=self.mqtt_port,
            keepalive=60,
            bind_address="")

        def background_connection():

            self.mqttc.loop_forever()
            return

        t = threading.Thread(target=background_connection)
        t.daemon = True
        t.start()

    ####################### AUTH ###########################

    def login(self, username, password):
        """ Save auth credentials to objects return """

        payload = {'password': password, 'username': username}
        response = requests.post(self.url + "api-token-auth/", data=payload)

        if response.status_code == 200:
            self.username = username
            self.password = password
            self.authenticated = True
            self.user_hash = response.json()["token"]
            self.headers = {
                'Authorization': 'Token %s' % self.user_hash
            }
            self.connect_mqtt()

        else:
            self.authenticated = False

    def register(self, username, password, last_name="", first_name=""):
        """ Save auth credentials to objects return """

        payload = {
            'password1': password,
            "password2": password,
            'username': username,
            "first_name": first_name,
            "last_name": last_name
        }
        response = requests.post(self.url + "register_api/", data=payload)
        return response

    ####################### MQTT ###########################

    @validate_user
    def subscribe_actioner(self, device, actioner, on_data):

        """
        Subscribe to concrete actioner
        """

        def on_publish(mqttc, userdata, mid):
            mqttc.disconnect()

        def on_message(mqtcc, userdata, message):

            on_data(json.loads(message.payload))

        client = mqtt.Client()
        client.username_pw_set(self.username, password=self.password)
        client.on_message = on_message
        client.connect(
            host=self.host,
            port=self.mqtt_port,
            keepalive=60,
            bind_address="")

        print ("Subscribe to --->  %s - %s" % (device, actioner))

        def worker():
            # print "WORKER"
            client.loop_forever()
            return

        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()
        # print "subscrito a ->"
        # print "StationDiy/sensor/%s/%s/%s"%(self.user_hash,device,sensor)
        client.subscribe("stationdiy/%s/%s/actioner/%s" % (
            self.user_hash,
            device,
            actioner))

    @validate_user
    def subscribe_sensor(self, device, sensor, on_data):

        """
        Subscribe to concrete actioner
        """

        def on_publish(mqttc, userdata, mid):
            mqttc.disconnect()

        def on_message(mqtcc, userdata, message):

            on_data(json.loads(message.payload))

        client = mqtt.Client()
        client.username_pw_set(self.username, password=self.password)
        client.on_message = on_message
        client.connect(
            host=self.host,
            port=self.mqtt_port,
            keepalive=60,
            bind_address="")

        print ("Subscribe to --->  %s - %s" % (device, sensor))

        def worker():
            # print "WORKER"
            client.loop_forever()
            return

        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()
        # print "subscrito a ->"
        # print "StationDiy/sensor/%s/%s/%s"%(self.user_hash,device,sensor)
        client.subscribe("stationdiy/%s/%s/sensor/%s" % (
            self.user_hash,
            device,
            sensor))


    @validate_user
    def subscribe_device(self, device, on_data):

        """
        Subscribe to concrete actioner
        """

        def on_publish(mqttc, userdata, mid):
            mqttc.disconnect()

        def on_message(mqtcc, userdata, message):

            on_data(json.loads(message.payload))

        client = mqtt.Client()
        client.username_pw_set(self.username, password=self.password)
        client.on_message = on_message
        client.connect(
            host=self.host,
            port=self.mqtt_port,
            keepalive=60,
            bind_address="")

        print ("Subscribe to --->  %s " % (device))

        def worker():
            # print "WORKER"
            client.loop_forever()
            return

        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()
        # print "subscrito a ->"
        # print "StationDiy/sensor/%s/%s/%s"%(self.user_hash,device,sensor)
        client.subscribe("stationdiy/%s/%s" % (
            self.user_hash,
            device,
            ))

    @validate_user
    def set_device(self, **kwargs):
        """ Set sensor by mqtt """

        data = {}
        if "ip" in kwargs or "latitude" in kwargs or "longitude" in kwargs:

            if "ip" in kwargs:
                data["ip"] = kwargs["ip"]
            if "latitude" in kwargs:
                data["latitude"] = kwargs["latitude"]
            if "longitude" in kwargs:
                data["longitude"] = kwargs["longitude"]

            self.sendMQTT(topic="stationdiy/%s/%s" % (
                self.user_hash,
                kwargs["device"]), data = data)

        return


    @validate_user
    def sendMQTT(self, **kwargs):
        """ Send message """

        data = {
            "data": kwargs["data"],
            "dt": time.time(),
            "ip": self.ip
        }

        payload = json.dumps(data)

        self.mqttc.publish(topic=kwargs["topic"], payload=payload, qos=0)

        # def on_connect(mqttc, userdata, rc):

        #     payload = json.dumps({
        #         "data": kwargs["data"],
        #         "dt": time.time()
        #     })

        #     mqttc.publish(topic=kwargs["topic"], payload=payload, qos=0)

        # def on_disconnect(mqttc, userdata, rc):
        #     pass
        #     # print('Disconnect...rc=' + str(rc))

        # def on_subscribe(mqttc, userdata, mid, granted_qos):
        #     print('subscribed (qos=' + str(granted_qos) + ')')

        # def on_unsubscribe(mqttc, userdata, mid, granted_qos):
        #     print('unsubscribed (qos=' + str(granted_qos) + ')')

        # def on_message(mqttc, userdata, msg):
        #     print('message received...')
        #     print ("-->%s" % userdata)
        #     print('topic: ' + msg.topic + ', qos: ' +
        #           str(msg.qos) + ', message: ' + str(msg.payload))

        # def on_publish(mqttc, userdata, mid):
        #     mqttc.disconnect()

        # self.mqttc = mqtt.Client()
        # self.mqttc.username_pw_set(self.username, password=self.password)
        # self.mqttc.on_connect = on_connect
        # self.mqttc.on_publish = on_publish

        # self.mqttc.connect(
        #     host=self.host,
        #     port=self.mqtt_port,
        #     keepalive=60,
        #     bind_address="")
        # self.mqttc.loop_forever()

    ####################### REST ###########################

    @validate_user
    def set_sensor(self, **kwargs):
        """ Set sensor by mqtt """

        self.sendMQTT(topic="stationdiy/%s/%s/sensor/%s" % (
            self.user_hash,
            kwargs["device"],
            kwargs["sensor"]), data = kwargs["data"])

    @validate_user
    def set_actioner(self, **kwargs):
        """ Set actioner data by mqtt """

        self.sendMQTT(topic="stationdiy/%s/%s/actioner/%s" % (
            self.user_hash,
            kwargs["device"],
            kwargs["actioner"]), data = kwargs["data"])

    @validate_user
    def getIntervalAlerts(self):
        """
        Get interval alerts
        """

        pass

    @validate_user
    def getPIDS(self):
        """
        Get interval PIDS
        """

        pass

    @validate_user
    def getPolynomials(self):
        """
        Get interval Polynomials
        """

        pass

    @validate_user
    def localeIntervalAlert(self):
        """
        Get interval alerts
        """

        pass

    @validate_user
    def localePID(self):
        """
        Get interval PIDS
        """

        pass

    @validate_user
    def localePolynomials(self):
        """
        Get interval Polynomials
        """

        pass

    @validate_user
    def getDevices(self):

        """
        Get all my Devices
        """

        response = requests.get(self.url + "api/device/", headers=self.headers)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return -1

    @validate_user
    def getSensors(self):

        """
        Get all my Sensors
        """

        response = requests.get(self.url + "api/sensor/", headers=self.headers)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return -1

    @validate_user
    def getActioners(self):

        """
        Get all my Actioners
        """

        response = requests.get(
            self.url + "api/actioner/", headers=self.headers)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return -1

    @validate_user
    def deleteDevices(self, name):

        """
        Get all my Devices
        """

        response = requests.get(self.url + "api/device/", headers=self.headers)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return -1

    @validate_user
    def deleteSensors(self, name_device, name_sensor):

        """
        Get all my Sensors
        """

        response = requests.get(self.url + "api/sensor/", headers=self.headers)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return -1

    @validate_user
    def deleteActioners(self, name_device, name_actioner):

        """
        Get all my Actioners
        """

        response = requests.get(
            self.url + "api/actioner/", headers=self.headers)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return -1

    # def setRemoteAlert(self, device, sensor, actioners):
    #     """ One sensor is able to actioner more than one actioners """
    #     # set remote alert
    # def subscribeSensor(self, device, sensor, callback):
    #     """ Subscribe to sensor """
    #     subscribe_client = mqtt.Client()
    #     subscribe_client.on_connect = on_connect
    #     subscribe_client.on_disconnect = on_disconnect
    #     subscribe_client.on_message = on_message
    #     subscribe_client.on_subscribe = on_subscribe

# python setup.py register -r pypitest
# python setup.py sdist upload -r pypitest
# python setup.py register -r pypi
# python setup.py sdist upload -r pypi
