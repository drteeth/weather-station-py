import network
import time
from machine import I2C, Pin
from microdot import Microdot
import bme280

TEMP_SENSOR     = 118
BATTERY_CHARGER = 54
LIGHT_SENSOR    = 72

i2c = I2C(0, sda=Pin(6), scl=Pin(7))

def battery():
    raw_v = i2c.readfrom_mem(BATTERY_CHARGER, 0x02, 2)
    voltage = ((raw_v[0] << 8 | raw_v[1]) >> 4) * 78.125e-6
    raw_soc = i2c.readfrom_mem(BATTERY_CHARGER, 0x04, 2)
    percent = raw_soc[0] + raw_soc[1] / 256
    return f"{percent:.0f}%"

def wakeup_light_sensor():
    i2c.writeto_mem(LIGHT_SENSOR, 0x00, b"\x00\x00")

def light():
    raw = i2c.readfrom_mem(LIGHT_SENSOR, 0x04, 2)
    counts = raw[0] | (raw[1] << 8)
    return f"{counts * 0.0576:.0f} lux"

temp_sensor = bme280.BME280(i2c=i2c, address=TEMP_SENSOR)

wakeup_light_sensor()

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.config(hostname="weatherstation")
wifi.connect("Network", "password")

print("Connecting to WiFi...", end="")
while not wifi.isconnected():
    print(".", end="")
    time.sleep(0.5)

app = Microdot()


@app.route("/")
def index(request):
    temperature, pressure, humidity = temp_sensor.values
    battery_level = battery()
    light_level = light()

    html = f"""
    <!doctype html>
    <html>
        <head>
            <title>Weather Station</title>
            <meta http-equiv="refresh" content="10">
            <style>
                body {{
                    font-family:sans-serif;padding:2em
                }}

                h1 {{
                    color:#06c
                }}
            </style>
        </head>
        <body>
            <h1>Weather Station</h1>
            <p>Temperature: {temperature}</p>
            <p>Pressure: {pressure}</p>
            <p>Humidity: {humidity}</p>
            <p>Light: {light_level}</p>
            <p>Battery: {battery_level}</p>
        </body>
    </html>
    """

    return html, 200, {"Content-Type": "text/html"}

app.run(host="0.0.0.0", port=80)

ip_address = wifi.ifconfig()[0]
print(f"http://{ip_address}")
print("http://weatherstation.local")

