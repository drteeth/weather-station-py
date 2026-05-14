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

| Part | Model | Price (CAD) | Link |
|---|---|---|---|---|
| Microcontroller | SparkFun Thing Plus ESP32-C6 | $34.65 | [DigiKey](https://www.digikey.ca/en/products/detail/sparkfun-electronics/22924/22321033) [Mouser](https://www.mouser.ca/ProductDetail/SparkFun/DEV-22924?qs=dbcCsuKDzFVe7EVKMM7Bfg%3D%3D)|
| Temperature Sensor | BME280 | $14.75 | [Abra electronics](https://abra-electronics.com/sensors/sensors-temperature-en/sens-64-3-3v.html) |
| Battery | 3.7V 500 mAh LiPo, JST-PH | $8.65 | [Abra electronics](https://abra-electronics.com/batteries-holders/batteries-polymer-lithium-ion/bat-lipo-3-7-500-3-7v-500mah-lithium-ion-polymer-battery.html) |
| I2C adapter cable | Flexible Qwiic Cable — Female Jumpers | $3.37 | [Abra electronics](https://abra-electronics.com/interconnects/connectors/qwiic/flexible-qwiic-cable-female-jumper-4-pin.html) |

### Also need

- USB-C cable (for flashing and charging)
- Soldering iron + lead-free solder (for attaching the BME280 header pins)

### Optional stretch goal

| Part | Model | Vendor | Price (CAD) | Link |
|---|---|---|---|---|
| Light sensor | SparkFun VEML7700 | ABRA Electronics | $11.75 | [Abra electronics](https://abra-electronics.com/sensors/sensors-light-imaging-en/sen-29211-sparkfun-ambient-light-sensor-veml7700.html) |

### Potential 3D printed case
https://www.thingiverse.com/thing:1564828
