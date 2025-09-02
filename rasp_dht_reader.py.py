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