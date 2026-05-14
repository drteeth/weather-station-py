# MicroPython weather station

A tiny weather station that reads the air around it — temperature, humidity, and air pressure — and serves the readings on a webpage you can open from any device on your WiFi. Plugs into USB-C, or runs on a small rechargeable battery so you can move it around the house.

## Getting started

You'll need Python 3.10+ with `pip` and `curl` on your laptop, and the Thing Plus plugged into a USB-C port. The board appears as `/dev/ttyACM0` or `/dev/tty.usbmodem83201` on Linux and Mac (set `PORT=/dev/ttyXXX` otherwise).

```bash
script/setup                       # 1. install tools, download firmware + libraries
script/flash-firmware              # 3. one-time: wipe the board and install MicroPython
script/flash                       # 4. copy the code onto the board and start it
script/connect                     # 5. watch the boot output for the IP address
```

`script/connect` prints something like `IP address: http://192.168.1.42` — open that URL in a browser on the same WiFi to see the readings. Press **Ctrl+]** to disconnect.

A few useful keystrokes inside `script/connect`:

- **Ctrl+C** — interrupt the running program (drops you to a `>>>` prompt).
- **Ctrl+D** — soft reset, re-runs the program from the top so you can watch it boot.
- **Ctrl+]** — disconnect.

The physical **RST** button on the Thing Plus does a hard reset.

## Weather Station Parts List

### Required parts

| Part | Model | Vendor | Price (CAD) | Link |
|---|---|---|---|---|
| Microcontroller | SparkFun Thing Plus ESP32-C6 (DEV-22924) | Digi-Key Canada | $34.65 | https://www.digikey.ca/en/products/detail/sparkfun-electronics/22924/22321033 |
| Sensor | GY-BME280-3.3V (SENS-64-3.3V) | ABRA Electronics | $14.75 | https://abra-electronics.com/sensors/sensors-temperature-en/sens-64-3-3v.html |
| Battery | 3.7V 500 mAh LiPo, JST-PH (BAT-LIPO-3.7-500) | ABRA Electronics | $8.65 | https://abra-electronics.com/batteries-holders/batteries-polymer-lithium-ion/bat-lipo-3-7-500-3-7v-500mah-lithium-ion-polymer-battery.html |
| I²C adapter cable | Flexible Qwiic Cable — Female Jumper (4-pin) | ABRA Electronics | $3.37 | https://abra-electronics.com/interconnects/connectors/qwiic/flexible-qwiic-cable-female-jumper-4-pin.html |

### Also need

- USB-C cable (for flashing and charging)
- Female-to-female Dupont jumper wires (4 wires, or 8 if adding the light sensor)
- Soldering iron + solder (for the BME280 header pins)


### Optional stretch goal

| Part | Model | Vendor | Price (CAD) | Link |
|---|---|---|---|---|
| Light sensor | SparkFun VEML7700 (SEN-29211) | ABRA Electronics | $11.75 | https://abra-electronics.com (search "SEN-29211") |

### Potential 3D printed case
https://www.thingiverse.com/thing:1564828
