<h1 align="center">Modelo IoT Adaptativo para la Monitorización de Sistemas de Riego en Patios Traseros</h1>
<br/>
<hr>
<br/>

<h3>Módulo script de lectura de sensores DHT22.</h3>
<hr width=50% />
<b>Archivo rasp_dht_reader.py</b>

<br/>
<p>Para la lectura de los sensores se realizaron 3 archivos, el primero para leer los DHT22, se desarrolló el programa rasp_dht_reader.py en el cual se importaron las librerías de sys, time, json, paho-mqtt-client y DHTReader, se asignó un diccionario llamado SENSOR_GPIO_MAPPING en el que se establecieron los pines 12 para el sensor 1, el pin 16 para el sensor 2, el pin 25 para el sensor 3 y el pin 24 para el sensor 4, además se asignó la variable chip_path con la ruta de acceso a los pines desde Linux “/dev/gpiochip4”.</p>


<p>Para el acceso al servidor de thingboards en la nube, se establecieron las variables de THINGSBOARD_HOST y ACCESS_TOKEN, valores que se obtienen de la plataforma Thingboards; así mismo se instanció el objeto mqtt.client() especificando la versión 2 para su funcionamiento y se añadieron el host y el token en el puerto 1883 para luego iniciar el proceso de envío con el método client.loop.start().</p>


<p>Se asignó un diccionario llamado sensors con cada puerto de lectura, instanciándolos mediante el método DHTReader(dht_type, chip_path, gpio), para cada puerto y facilitar la llamada dentro del ciclo while. Para el envío de los datos, se realiza la lectura de cada elemento desde un ciclo for accediendo a la gpio(puerto), sensor_name(número de sensor) y leyendo los datos mediante humidity, temperature_c, temperature_f = sensors[gpio].read_data(), estos datos se agregan a un diccionario llamado sensor_data con los valores de temperatura y humedad, los cuales se añaden a la función de envío client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1). Posteriormente, para evitar saturación, se hace un retraso de envío de 60 segundos en cada iteración. Se recomienda cerrar el cliente mqtt mediante client.loop_stop() y client.disconnect()</p>
<br/>


```python
import sys, time, json
from dht_reader.dht_reader import DHTReader # type: ignore
import paho.mqtt.client as mqtt # type: ignore

SENSOR_GPIO_MAPPING = {
    12: "1", 16: "2", 25: "3", 24: "4" }

dht_type = "DHT22"
chip_path = "/dev/gpiochip4"
THINGSBOARD_HOST = "fvh.villahermosa.tecnm.mx"
ACCESS_TOKEN = 'ZEA_TOKEN_TODOS_LISTOS'

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(ACCESS_TOKEN)
client.connect(THINGSBOARD_HOST, 1883, 60)
client.loop_start()

sensors = {gpio: DHTReader(dht_type, chip_path, gpio) for gpio in SENSOR_GPIO_MAPPING}
while True:
    try:
        for gpio, sensor_name in SENSOR_GPIO_MAPPING.items():
            humidity, temperature_c, temperature_f = sensors[gpio].read_data()
            if humidity is not None and temperature_c is not None:
                print(f'Sensor{sensor_name} (GPIO {gpio}): Humidity: {humidity:.1f}% \
                      Temperature: {temperature_c:.1f}°C {temperature_f:.1f}°F')
                # Datos a edatanviar
                sensor_data = {
                    f'temperature_{sensor_name}': temperature_c,
                    f'humidity_{sensor_name}': humidity
                }
                # Publicar los datos en ThingsBoard
                client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
            else:
                print(f"Error leyendo sensor {sensor_name} en GPIO {gpio}")
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(60)  # Pequeño retraso para evitar saturación
client.loop_stop()
client.disconnect()
```
<h3>Módulo script de automatización de riego.</h3>
<hr width=50% />



Para el módulo de automatización del riego se crearon dos archivos agenda.json y riego_automatico.py; el primero se utiliza para establecer el horario en que se prenderá y apagará la bomba establecidas en las claves “HoraInicio” y en “HoraFin”, este archivo puede ser modificado por el agricultor desde un archivo de texto o una interfaz gráfica.
<b>Archivo agenda.json</b>

```json 

{
            "Lunes":{
                    "Veces":7,
                    "Horario":[
                        {"HoraInicio":"08:00","HoraFin":"08:01","Tiempo":"1m"},
                        {"HoraInicio":"10:00","HoraFin":"10:01","Tiempo":"1m"},
                        {"HoraInicio":"12:00","HoraFin":"12:01","Tiempo":"1m"},
                        {"HoraInicio":"14:00","HoraFin":"14:01","Tiempo":"1m"},
                        {"HoraInicio":"16:00","HoraFin":"16:01","Tiempo":"1m"},
                        {"HoraInicio":"18:00","HoraFin":"18:01","Tiempo":"1m"},
                        {"HoraInicio":"20:00","HoraFin":"20:01","Tiempo":"1m"}
                    ]
            },
            "Martes":{
                    "Veces":5,
                    "Horario":[
                        {"HoraInicio":"10:00","HoraFin":"10:01","Tiempo":"1m"},
                        {"HoraInicio":"12:00","HoraFin":"12:01","Tiempo":"1m"},
                        {"HoraInicio":"14:00","HoraFin":"14:01","Tiempo":"1m"},
                        {"HoraInicio":"16:00","HoraFin":"16:01","Tiempo":"1m"},
                        {"HoraInicio":"18:00","HoraFin":"18:01","Tiempo":"1m"}
                    ]
            },
            "Miercoles":{
                    "Veces":5,
                    "Horario":[
                        {"HoraInicio":"10:00","HoraFin":"10:01","Tiempo":"1m"},
                        {"HoraInicio":"12:00","HoraFin":"12:01","Tiempo":"1m"},
                        {"HoraInicio":"14:00","HoraFin":"14:01","Tiempo":"1m"},
                        {"HoraInicio":"16:00","HoraFin":"16:01","Tiempo":"1m"},
                        {"HoraInicio":"18:00","HoraFin":"18:01","Tiempo":"1m"}
                    ]
            },
            "Jueves":{
                    "Veces":5,
                    "Horario":[
                        {"HoraInicio":"11:02","HoraFin":"11:03","Tiempo":"1m"},
                        {"HoraInicio":"12:00","HoraFin":"12:01","Tiempo":"1m"},
                        {"HoraInicio":"14:00","HoraFin":"14:01","Tiempo":"1m"},
                        {"HoraInicio":"16:00","HoraFin":"16:01","Tiempo":"1m"},
                        {"HoraInicio":"18:00","HoraFin":"18:01","Tiempo":"1m"}
                    ]
            },
            "Viernes":{
                    "Veces":5,
                    "Horario":[
                        {"HoraInicio":"10:00","HoraFin":"10:01","Tiempo":"1m"},
                        {"HoraInicio":"12:00","HoraFin":"12:01","Tiempo":"1m"},
                        {"HoraInicio":"14:21","HoraFin":"14:23","Tiempo":"1m"},
                        {"HoraInicio":"16:00","HoraFin":"16:01","Tiempo":"1m"},
                        {"HoraInicio":"18:00","HoraFin":"18:01","Tiempo":"1m"}
                    ]
            },
            "Sabado":{
                    "Veces":5,
                    "Horario":[
                        {"HoraInicio":"10:00","HoraFin":"10:01","Tiempo":"1m"},
                        {"HoraInicio":"12:00","HoraFin":"12:01","Tiempo":"1m"},
                        {"HoraInicio":"14:00","HoraFin":"14:01","Tiempo":"1m"},
                        {"HoraInicio":"16:00","HoraFin":"16:01","Tiempo":"1m"},
                        {"HoraInicio":"18:00","HoraFin":"18:01","Tiempo":"1m"}
                    ]
            },
            "Domingo":{
                    "Veces":7,
                    "Horario":[
                        {"HoraInicio":"08:00","HoraFin":"08:01","Tiempo":"1m"},
                        {"HoraInicio":"10:00","HoraFin":"10:01","Tiempo":"1m"},
                        {"HoraInicio":"12:00","HoraFin":"12:01","Tiempo":"1m"},
                        {"HoraInicio":"14:00","HoraFin":"14:01","Tiempo":"1m"},
                        {"HoraInicio":"16:00","HoraFin":"16:01","Tiempo":"1m"},
                        {"HoraInicio":"18:00","HoraFin":"18:01","Tiempo":"1m"},
                        {"HoraInicio":"20:00","HoraFin":"20:01","Tiempo":"1m"}
                    ]
            }
}
```

<p>El archivo riego_automatico.py, permite activar y desactivar la bomba, así como el envío del estado actual de la bomba a la plataforma ThingsBoard. Primeramente, se especifican las librerías a utilizar, el PIN 26 considerado para activar o desactivar el relevador de 5V y los parámetros de acceso a la plataforma ThingsBoard, estos son: el host, el token y la instanciación del cliente PAHO-MQTT versión 2; además se anexa un diccionario sensor_data, que llevará a la nube un valor 0 indicando que la bomba está apagada y llevará un valor 1 cuando la bomba esté prendida.</p>


<p>En el mismo archivo riego_automatico.py, La función obtener_apuntador(veces, dia, hora_actual, mydata), busca en el archivo agenda.json coincidencias en el día actual y la hora y ejecuta el prendido o apagado de la bomba, al mismo tiempo envía el estado de la bomba a la plataforma Thingsboard</p>

<p>En el mismo archivo riego_automatico.py, se activa el envío de datos mediante MQTT desde el método client.loop_start() y se continúa con el While True: donde se hace la lectura del archivo de horarios con la instrucción with open("agenda.json","r") as j:, se obtiene la fecha y hora actual y con esto se determina el día de la semana a través de una condición if, la cual llama a la función obtener_apuntador(mydata[dia_hoy]["Veces"], "Lunes", hora_actual, mydata), pasándole los parámetros obtenidos.</p>
<b>Archivo riego_automatico.py</b>


```python
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

```


<h3>Módulo script de sensor de flujo de agua.</h3>
