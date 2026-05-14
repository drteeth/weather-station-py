---
marp: true
theme: default
paginate: true
---

# Weirdmageddon weather station

A tiny computer that senses the weather and shows it as a webpage.

This party never stops!
Time is dead and meaning has no meaning!
Existence is upside-down and I reign supreme!
Welcome, one and all, to Weirdmageddon!

---

## What we're building

You will build a weather station specific to the weather at your house, and only available to your house.

- Hardware (computer, sensors)
- Software (to control everything)
- An outdoor case with a rechargeable battery

---

## How it will work

- Measures **Temperature** — how warm the air is
- Measures **Humidity** — how much water is in the air
- Measures **Pressure** — how heavy the air is pushing down (this is what tells you a storm is coming!)
- Serves a webpage — open it from any phone or laptop on your WiFi
- Runs on a small rechargeable battery
- Weatherproof enclosure allows it to live outside and give you the weather

---

## The brains (AKA "Bill")

An ESP32 "microcontroller"

- This is a tiny, tiny computer that doesn't use much power.
- It doesn't have a screen, mouse, keyboard, or even any way of plugging things into it
- It just has metal "pins" that we can attach wires to.
- Ok fine they are holes, but we call them pins. Deal with it.
- For convenience, it also has a "Qwiic" connector
- That lets us connect wires without soldering. (Pronounced "Soddering", also deal with it)

---

## Get ready... to get ready
- We can connect to the ESP32 by "tunnelling" into it from our big computers
- This allows us to send code to the ESP32, and have it run there

Open a terminal and navigate to the folder:

```bash
cd ~/Documents/weather-station-py
```

Run the setup script to install the tools we're going to need

```bash
script/setup
```

---

## Get MicroPython onto the ESP32

We need to get MicroPython installed onto the ESP32, we do this by "flashing" it to Bill

```bash
script/flash-firmware
```

---

## Run some code on the board

You're setup, we can now run code on the ESP32

```sh
script/connect
```

What you type is now tunnelled over the USB cable to the ESP32
It accepts Python code only. Try some:

```python
4 + 5
print("reality is an illusion")
```

Disconnect when you are done noodling around by pressing:

```bash
Ctrl-]
```

---

## Writing permanent code

We need to be able to write code on our computers and flash it onto the board so it will be remembered.

- Open Visual Studio Code
- Open `main.py` and write:

```python
import time

while True:
    print("We punch what we don't understand!")
    time.sleep(5)
```

Save your changes

---

## Send the code to the board

Flash the code to the board:
```bash
script/flash
```

Connect to the board:
```bash
script/connect
```

Reset the board:
```bash
Ctrl-d
```

You should now see your quote every 5 seconds

---

## Sensing!

Our weather station needs to be able to sense the weather.

We'll do that with the BME280 environmental sensor

- A small sensor that the ESP32 can connect to for temperature, humidity, and pressure
- Mounted on a 'breakout board'
- Has 6 metal "header" pins that I've attached to the holes with solder
- We'll use a "Jumper cable" to Qwiic connector to wire it up

---

## In electronics and hardware, the wires have different purposes

The BME280 has 6 pins, but we're only going to use 4:

- VCC - Voltage - This is power (3.3 Volts)
- GND — Ground - power flows through the device to ground
- SCL — Clock - tells the microcontroller when to read
- SDA — Data - carries the data the microcontroller will read (temperature, etc)

---

## The jumper cable has 4 matching colours:

- Red = 3.3V - connect this to VCC on the sensor
- Black = GND - connect this to GND on the sensor
- Yellow = SCL - connect this to SCL on the sensor
- Blue = SDA - connect this to SDA on the sensor

After you connect these 4 jumpers to the sensor, connect the other end to Bill

---

# The "Pinout" diagram

```
                ┌─ antenna ─┐
            ┌───┴───────────┴──┐
     IO9 ───┤ ○              ○ ├ IO6 / SDA <-- ** remember this **
 IO16 / TX ─┤ ○              ○ ├ IO7 / SCL <-- ** and this **
 IO17 / RX ─┤ ○              ○ ├ IO15
IO21 / POCI ┤ ○              ○ ├ IO23    The microcontroller has:
IO20 / PICO ┤ ○              ○ ├ IO8     3V3 (VCC), GND, SDA, and SCL
 IO19 / SCK ┤ ○  Thing Plus  ○ ├ IO10
     IO5 ───┤ ○   ESP32-C6   ○ ├ IO11    Connecting them is done for us
     IO4 ───┤ ○              ○ ├ IO22    by the Qwiic cable.
     IO3 ───┤ ○              ○ ├ IO18
     IO2 ───┤ ○              ○ ├ VUSB
     IO1 ───┤ ○              ○ ├ EN
     IO0 ───┤ ○              ○ ├ VBAT
     GND ───┤ ○                │
     3V3 ───┤ ○                │
     RST ───┤ ○                │
            │      [USB]       │
            └──────────────────┘
```

---

## Back to software

The voltage, ground, clock and data lines of both boards are now connected
...but it doesn't do anything.

Bill is trapped in the void.

We need a way to get the data from the sensor.

You are going to use software (code) to control the microcontroller to ask the sensor for readings

---

## Talking to the hardware from software


We going to use something called "I2C" (Eye Two Sea) to communicate between the microcontroller and the sensor boards

In `main.py` add this line to the "imports" section (the top)

```python
from machine import I2C, Pin
```

Delete your "while loop" and replace it with this code:

```python
sda_pin = Pin(6)
scl_pin = Pin(7)
i2c = I2C(0, sda=sda_pin, scl=scl_pin)
```

Notice the pin numbers match the Pinout diagram for the microcontroller

---

## Finding the address of the sensor

Flash, and connect to your board again

```bash
script/flash
script/connect
```

Now we're back in Python on the board, find out the "address" of the BME280:

```python
i2c.scan()
```

You should see a list of addresses, something like:
```python
[54, 118]
```
`118` is the sensor's address, remember it (`118` is `0x76` in 'hexadecimal')

Disconnect from the board again (`Ctrl-]`)

---

## Reading from the sensor

Back in `main.py` add these lines

```python
import bme280
TEMP_SENSOR = 118
temp_sensor = bme280.BME280(i2c=i2c, address=TEMP_SENSOR)
```

Flash, connect, and then type:

```python
temp_sensor.values
```

That gives you the temperature, pressure, and humidity all at once — three readings packed into a little group called a "tuple".

Disconnect from the board after noodling

---

## Make it automatic

In `main.py` add the following lines

```python
while True:
    temperature, pressure, humidity = temp_sensor.values

    print("")
    print(f"Temperature: {temperature}")
    print(f"Pressure: {pressure}")
    print(f"Humidity: {humidity}")

    time.sleep(5)
```

The first line splits the three readings out into separate variables.

Flash your code, connect and watch the values change over time

---

## That's cool, but...

We want to show the weather on a webpage for anyone on our network to see.

To do that we need to:
1. Connect to WiFi network in the house
2. Turn our microcontroller into a web server

---

## Configuring WiFi

In order for devices that aren't attached to the microcontroller by the USB cable to connect to it, the microcontroller needs to join the same (2.4Ghz!) wireless network that your computer is on.

Add the network import to the imports section:
```python
import network
```

In `main.py` before your while loop, add:

```python
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.config(hostname="weatherstation")
wifi.connect("Network", "password")
```

Replace 'Network' and 'password' with the name and password of your network


---

## Connecting the network

Now that the configuration is done, you can use it to connect.

In `main.py` continue by adding:

```python
print("Connecting to WiFi...", end="")
while not wifi.isconnected():
    print(".", end="")
    time.sleep(0.5)

print(f"http://{wifi.ifconfig()[0]}")
```

Flash, connect, reset, and make sure WiFi connects.

---

## A web server

A web server shows HTML when a browser visit it by typing its address into the address bar.

try the numerical address it shows you, or try: http://weatherstation.local

Neither will work though, until we create a webserver and tell it what to show

---

## A basic web server

Microdot is a webserver we can use in MicroPython

in `main.py` add this line to the imports section:

```python
from microdot import Microdot
```


Then replace your while loop with:

```python
app = Microdot()

@app.route("/")
def index(request):
    return f"<h1>Reality is an illusion, the universe is a hologram, buy gold byeeeee!!!</h1>

app.run(host="0.0.0.0", port=80)
```

Flash it, and refresh your browser, you should see your text

---

## Showing weather data

We want to show the weather on our page, so let's make that change

Add this line to take the measurements and hold them in variables

```python
temperature, pressure, humidity = temp_sensor.values
```

---

## Measurements as HTML

Let's get weird by writing html code INSIDE python code. Like Mabeland is inside Gravity Falls.

```python
    html = f"""
    <!doctype html>
    <html>
        <head>
            <title>Weather station</title>
        </head>
        <body>
            <h1>Weather Station</h1>
            <p>Temperature: {temperature}</p>
            <p>Pressure: {pressure}</p>
            <p>Humidity: {humidity}</p>
        </body>
    </html>
    """
    return html, 200, {"Content-Type": "text/html"}
```
---


## Test it out

Flash and refresh your browser!

As you refresh you should see the numbers change slightly

---

## Refresh automatically

A billion years in the void gets annoying, and so does refreshing the page.

The browser will refresh on it's own if you add this line to the `<head>` section of the html

Add this line after the `<title>` line:

```html
<meta http-equiv="refresh" content="10">
```

The browser will now refresh every 10 seconds

---

## Make it look a little better

Add these lines after the `<meta` line you just added

```html
<style>
    body {{ font-family:sans-serif;padding:2em }}
    h1 {{ color:#06c }}
</style>
```

Flash, then refresh your browser, it should have a blue title look a little better.

---

## Cut the cord

This is great, it does what we want. You can now unplug the USB cable, and plug the battery in. It might take a minute, but you should be able to see the weather in your browser again.

We've just added a Lithium Polymer battery
- It will power the weather station
- It's rechargeable

---

## What's next?

You did it! Congratulations!

If you want to keep going, you can:

- Add the battery level on the page
- Add a daylight detector
- Graph the weather data with AI
- Make the battery last longer
- Build a weatherproof case and put it outside

---

## Add the battery level on the page

In `main.py` add a constant for the battery charger's address
Remember `54` from the `i2c.scan()` list? That's the battery charger.

```python
BATTERY_CHARGER = 54
```

Constants give names to 'magic' values like 54

---

## Create a function for reading the battery level

After defining the `i2c` variable with it's pins, add:

```python
def battery():
    raw_v = i2c.readfrom_mem(BATTERY_CHARGER, 0x02, 2)
    voltage = ((raw_v[0] << 8 | raw_v[1]) >> 4) * 78.125e-6
    raw_soc = i2c.readfrom_mem(BATTERY_CHARGER, 0x04, 2)
    percent = raw_soc[0] + raw_soc[1] / 256
    return f"{percent:.0f}%"
```

This is a "function" and when we use it, it will give us the percentage of battery left.

---

## Show the battery on the page

In the index route, use the battery function to get the percentage

```python
battery_level = battery()
```
and add it to the HTML

```python
<p>Battery: {battery_level}</p>
```

---

## Add a daylight detector

The VEML7700 ambient light sensor measures brightness in **lux**.

- Disconnect the temperature sensor from Bill
- Attach a Qwiic cable from Bill to the light sensor
- Attach the temperature sensor to the light sensor

You should now have a chain: Bill :: light sensor :: temperature sensor

I2C is called a communication **bus** because they form this line. A bus... with addresses...

---

## Teaching Bill to see the light

In `main.py`, add a new constant with the others:

```python
LIGHT_SENSOR = 72
```

Then add two new functions, one to wake the light sensor, and one to read from it:

```python
def wakeup_light_sensor():
    i2c.writeto_mem(LIGHT_SENSOR, 0x00, b"\x00\x00")

def light():
    raw = i2c.readfrom_mem(LIGHT_SENSOR, 0x04, 2)
    counts = raw[0] | (raw[1] << 8)
    return f"{counts * 0.0576:.0f} lux"
```

---

## Show the light level

Use the wake function somewhere before the `app.run(...)` line:

```python
wakeup_light_sensor()
```

In the index route, use the `light` function to get the light value

```python
light_level = light()
```

and add it to the HTML:

```python
<p>Light: {light_level}</p>
```

Flash, refresh, and try covering the sensor with your hand!

---

## Graph the weather data with AI

We want graphs that show how the temperature, humidity, and pressure have changed over time.

Time to try something new — we're going to ask **Claude** (an AI) to add a feature for us.

Open Claude and give it this prompt:

> Add a chart to my weather station page showing how the temperature, humidity, and pressure have changed recently. Keep the change small and easy to read.

Then flash, refresh your browser, and see what happened.

Can you read the code Claude wrote? Does it do what you expected?

---

## Make the battery last longer

Bill's WiFi radio is always awake — even when nobody is looking at the weather. Listening burns battery, just like talking does.

The good news: every WiFi network sends out a little "anything for you?" signal about ten times a second. The radio only really needs to wake up for those.

After the WiFi-connecting loop in `main.py`, add this line:

```python
wifi.config(pm=wifi.PM_POWERSAVE)
```

`pm` is short for "power management". `PM_POWERSAVE` tells the radio it's allowed to take little naps in between the check-ins. The page will load just a tiny bit slower, but the battery will last *much* longer.

---

## Build a weatherproof case and put it outside

We can't put this bundle of wires and electronics outside in the rain to get ... weird. We need some kind of protective shell to shield it from the snow, sun, rain, squirels, bats, Henchmanics, etc.

The trick is that we **don't** want to shield it from temperature, pressure, and humidity. And the light sensor (if you decided to add it), will need to be exposed to the light.

We need a case that will handle all of this.
