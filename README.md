<h1 align="center">Modelo IoT Adaptativo para la Monitorización de Sistemas de Riego en Patios Traseros</h1>
<br/>
<hr>
<br/>

<h3>Módulo script de lectura de sensores DHT22.</h3>
<hr width=50% />
<b>Archivo rasp_dht_reader.py</b>
<br/>
Para la lectura de los sensores se realizaron 3 archivos, el primero para leer los DHT22, se desarrolló el programa rasp_dht_reader.py en el cual se importaron las librerías de sys, time, json, paho-mqtt-client y DHTReader, se asignó un diccionario llamado SENSOR_GPIO_MAPPING en el que se establecieron los pines 12 para el sensor 1, el pin 16 para el sensor 2, el pin 25 para el sensor 3 y el pin 24 para el sensor 4, además se asignó la variable chip_path con la ruta de acceso a los pines desde Linux “/dev/gpiochip4”.
Para el acceso al servidor de thingboards en la nube, se establecieron las variables de THINGSBOARD_HOST y ACCESS_TOKEN, valores que se obtienen de la plataforma Thingboards; así mismo se instanció el objeto mqtt.client() especificando la versión 2 para su funcionamiento y se añadieron el host y el token en el puerto 1883 para luego iniciar el proceso de envío con el método client.loop.start().


<h3>Módulo script de automatización de riego.</h3>
<hr width=50% />
<h3>Módulo script de sensor de flujo de agua.</h3>
