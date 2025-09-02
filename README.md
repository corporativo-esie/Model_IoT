<h1 align="center">Modelo IoT Adaptativo para la Monitorización de Sistemas de Riego en Patios Traseros</h1>
<br/>
<hr>
<br/>

<h3>Módulo script de lectura de sensores DHT22.</h3>
<hr width=50% />
<b>Archivo rasp_dht_reader.py</b>

<br/>
<p>Para la lectura de los sensores se realizaron 3 archivos, el primero para leer los DHT22, se desarrolló el programa rasp_dht_reader.py en el cual se importaron las librerías de sys, time, json, paho-mqtt-client y DHTReader, se asignó un diccionario llamado SENSOR_GPIO_MAPPING en el que se establecieron los pines 12 para el sensor 1, el pin 16 para el sensor 2, el pin 25 para el sensor 3 y el pin 24 para el sensor 4, además se asignó la variable chip_path con la ruta de acceso a los pines desde Linux “/dev/gpiochip4”.<p>
<p>Para el acceso al servidor de thingboards en la nube, se establecieron las variables de THINGSBOARD_HOST y ACCESS_TOKEN, valores que se obtienen de la plataforma Thingboards; así mismo se instanció el objeto mqtt.client() especificando la versión 2 para su funcionamiento y se añadieron el host y el token en el puerto 1883 para luego iniciar el proceso de envío con el método client.loop.start().</p>
<p>Se asignó un diccionario llamado sensors con cada puerto de lectura, instanciándolos mediante el método DHTReader(dht_type, chip_path, gpio), para cada puerto y facilitar la llamada dentro del ciclo while. Para el envío de los datos, se realiza la lectura de cada elemento desde un ciclo for accediendo a la gpio(puerto), sensor_name(número de sensor) y leyendo los datos mediante humidity, temperature_c, temperature_f = sensors[gpio].read_data(), estos datos se agregan a un diccionario llamado sensor_data con los valores de temperatura y humedad, los cuales se añaden a la función de envío client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1). Posteriormente, para evitar saturación, se hace un retraso de envío de 60 segundos en cada iteración. Se recomienda cerrar el cliente mqtt mediante client.loop_stop() y client.disconnect()</p>

<h3>Módulo script de automatización de riego.</h3>
<hr width=50% />
<h3>Módulo script de sensor de flujo de agua.</h3>
