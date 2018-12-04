# See https://docs.pycom.io for more information regarding library specifics

from pysense import Pysense
# seule la librairie pour la température est importée pour ce modèle
from SI7006A20 import SI7006A20

from MPL3115A2 import MPL3115A2

from wifi import WiFi
from mqtt import MQTTClient
import time

seuils = [940,980,1000,1025,1045]

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

    offset = 5
    ourPressure = b.pressure()/100

    if(ourPressure >= 940 and ourPressure < 980):
        currentState = 0

    if(ourPressure >= 980 and ourPressure < 1000):
        currentState = 1

    if(ourPressure >= 1000 and ourPressure < 1025):
        currentState = 2

    if(ourPressure >= 1025 and ourPressure < 1045):
        currentState = 3

    if(ourPressure >= 1045 and ourPressure <= 1075):
        currentState = 4

    while True:
        ourPressure = b.pressure()/100

        if(ourPressure >= 925 and ourPressure <= 1075):
            print("Sending")
            msg='{'
            msg+='"hPa":'+str(b.pressure()/100)

            print(str(ourPressure))
            print(seuils[currentState]+offset)
            if(ourPressure >= seuils[currentState+1]+offset) :
                currentState+=1
                msg+=',"tendance":"Amelioration"'

            if(ourPressure <= seuils[currentState]) :
                if(currentState != 0):
                    currentState-=1
                    msg+=',"tendance":"Degradation"'
                else:
                    msg+=',"tendance":"Aucune"'

            else :
                msg+=',"tendance":"Aucune"'

            msg+='}'
            print(str(msg))
            client.publish(topic="iot-2/evt/data/fmt/json", msg=msg)


        # if(ourPressure >= 925 and ourPressure <= 1075):
        #     tendances.append(1010)
        #     if(len(tendances) == 20):
        #         if(tendances[0] - tendances[19] < -5):
        #             maTendance = "Il va faire beau"
        #         elif(tendances[0] - tendances[19] > 5):
        #             maTendance = "Il va faire mauvais"
        #         tendances = []
        #         print(str(maTendance))
        #

        time.sleep(1)

except Exception as e:
    print("Exception" + str(e.args))
