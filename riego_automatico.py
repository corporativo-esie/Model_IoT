import json, time
from datetime import datetime

import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
# sección del GPIO 26 relevador
PIN = 26
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN, GPIO.OUT)
GPIO.output(PIN, GPIO.HIGH)

#plataforma thingsboard
THINGSBOARD_HOST = "fvh.villahermosa.tecnm.mx"
ACCESS_TOKEN = 'ZEA_TOKEN_TODOS_LISTOS'
sensor_data = {'bomba':0}
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(ACCESS_TOKEN)
client.connect(THINGSBOARD_HOST, 1883, 60)



# Función que obtiene la posicion de hora inicio y fin para prender la bomba
def obtener_apuntador(Veces, dia, hora_actual, mydata):
    hora_inicia = mydata[dia]["Horario"][0]["HoraInicio"]
    hora_fin  = mydata[dia]["Horario"][Veces-1]["HoraFin"]
    posicion = 99
    if hora_actual>=hora_inicia and hora_actual<=hora_fin:
        #return 1
        for contador in range(0, Veces):
            hora_i  = mydata[dia]["Horario"][contador]["HoraInicio"]
            hora_f  = mydata[dia]["Horario"][contador]["HoraFin"]
            if hora_actual>=hora_i and hora_actual<=hora_f:
                posicion = contador
                print("Bomba Prendida")
                GPIO.output(PIN, GPIO.HIGH)
                try:
                    sensor_data['bomba'] = 100
                    client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
                except Exception as e:
                    print(str(e))
        if posicion == 99:
           print("Bomba Apagada1")
           try:
             sensor_data['bomba'] = 0
             client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
           except Exception as e:
             print(str(e)) 
        return posicion   
    else:
        print("Bomba Apagada2")
        GPIO.output(PIN, GPIO.LOW)
        try:
           sensor_data['bomba'] = 0
           client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
        except Exception as e:
             print(str(e))
        return posicion

#declara los días de semana
days = ["Lunes","Martes","Miercoles","Jueves","Viernes","Sabado","Domingo"]
client.loop_start()
while True:
    with open("agenda.json","r") as j:
        mydata = json.load(j)
    fecha_hoy = datetime.now()
    dia_hoy = days[fecha_hoy.weekday()]
    hora_actual = str(fecha_hoy.strftime("%H:%M"))
    if dia_hoy == "Lunes":
        apuntador = obtener_apuntador(mydata[dia_hoy]["Veces"], "Lunes", hora_actual, mydata)
    elif dia_hoy == "Martes":
        apuntador = obtener_apuntador(mydata[dia_hoy]["Veces"], "Martes", hora_actual, mydata)
    elif dia_hoy == "Miercoles":
        apuntador = obtener_apuntador(mydata[dia_hoy]["Veces"], "Miercoles", hora_actual, mydata)
    elif dia_hoy == "Jueves":
        apuntador = obtener_apuntador(mydata[dia_hoy]["Veces"], "Jueves", hora_actual, mydata)
    elif dia_hoy == "Viernes":
        apuntador = obtener_apuntador(mydata[dia_hoy]["Veces"], "Viernes", hora_actual, mydata)
    elif dia_hoy == "Sabado":
        apuntador = obtener_apuntador(mydata[dia_hoy]["Veces"], "Sabado", hora_actual, mydata)
    elif dia_hoy == "Domingo":
        apuntador = obtener_apuntador(mydata[dia_hoy]["Veces"], "Domingo", hora_actual, mydata)
        print(" Resultado ", apuntador)
        print("Hora actual :", hora_actual)
    time.sleep(1) # 1 segundo

client.loop_stop()
client.disconnect()
