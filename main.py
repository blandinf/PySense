# See https://docs.pycom.io for more information regarding library specifics

from pysense import Pysense
# seule la librairie pour la température est importée pour ce modèle
from SI7006A20 import SI7006A20

from MPL3115A2 import MPL3115A2


from wifi import WiFi
from mqtt import MQTTClient
import time

IBMorgID='3q2ia6' # Identifiant de l'instance 'IoT PLatform' sur 6 caractères
deviceType='Pycom' # Nom du 'Device Type' défini dans le IoT Platform
deviceID='6651' # ID du device (4 dernieres caractères du SSID)
deviceToken='hibWV&6odxwTyXa@V&' # Token (mot de passe) défini pour le device dans le Iot Platform


py = Pysense()
si = SI7006A20(py)
b = MPL3115A2(py)


wifi = WiFi()


print("Temperature: " + str(si.temperature())+ " deg C and Relative Humidity: " + str(si.humidity()) + " %RH")
print("Dew point: "+ str(si.dew_point()) + " deg C")

print("wifi:")
print (WiFi.connectwifi('floki_io','F10kiN37w0rk!'))

try:
    # Syntaxe pour envoyer un paquet MQTT à IBM Cloud
    client = MQTTClient("d:"+IBMorgID+":"+deviceType+":"+deviceID, IBMorgID +".messaging.internetofthings.ibmcloud.com", user="use-token-auth", password=deviceToken, port=8883,ssl=True)
    print(client.connect())

    while True:
        print("Sending")
        mqttMsg = '{'
        mqttMsg = mqttMsg + '"hPa":' + str(b.pressure()/100)
        mqttMsg = mqttMsg + '}'
        client.publish(topic="iot-2/evt/data/fmt/json", msg=mqttMsg)
        time.sleep(1)


except Exception as e:
    print("Exception" + str(e.args))
