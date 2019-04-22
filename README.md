# Pi Motion MQTT Sensor

This is a small script that turns a [Raspberry Pi](https://amzn.to/2PmapoY) with a [HC-SR501](https://amzn.to/2PpPj9u) PIR sensor into a Motion MQTT sensor for use with Home Assistant (or other IOT) equipment.

Other GPIO based PIR sensors should also work with minor or no edits.

- [Pi Motion MQTT Sensor](#pi-motion-mqtt-sensor)
  - [How to install](#how-to-install)
    - [Requirements](#requirements)
    - [Update Settings](#update-settings)
    - [(OPTIONAL) Add a service](#optional-add-a-service)
  - [How to use new Sensor](#how-to-use-new-sensor)
  - [Troubleshooting](#troubleshooting)

## How to install

### Requirements

To install the PIR Sensor with the Pi a good tutorial is found [here.](https://electrosome.com/pir-motion-sensor-hc-sr501-raspberry-pi/)

On the software side, you need to install the following requirements.
```bash
$ sudo apt install python3-gpiozero
$ pip3 install paho-mqtt 
```

### Update Settings

Update the settings install pimotion.py with your own configuration.

Specifically the MQTT settings and the GPIO Pin Setting at the top of the file:

```python
PIR_GPIO = 7 # GPIO Pin of PIR Sensor

# Update this to adjust sensitivity. Default is 0.5
PIR_THRESHOLD = 0.5

# Update the follow MQTT Settings for your system.
MQTT_USER = "mqtt"              # MQTT Username
MQTT_PASS = "mqtt_password"     # MQTT Password
MQTT_CLIENT_ID = "pisensor"     # MQTT Client Id
MQTT_HOST_IP = "127.0.0.1"      # MQTT HOST
MQTT_PORT = 1883                # MQTT PORT (DEFAULT 1883)
```

### (OPTIONAL) Add a service 
If you would like to have the Motion Sensor to restart on startup, create the a file in the in the following location `/etc/systemd/system/pimotion.service`

```conf
[Unit]
Description=Raspberry Pi Motion Sensor MQTT Service
After=network.target

[Service]
Type=idle
User=pi
ExecStart=/usr/bin/python3 /home/pi/studycam/pimotion.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Update the file location and other settings as required and then load the service as follows:

```shell
$ sudo systemctl daemon-reload
$ sudo systemctl enable pimotion.service
$ sudo systemctl start pimotion.service
```

## How to use new Sensor

To add the sensor to Home Assistant use the [MQTT Binary Sensor Component](https://home-assistant.io/components/binary_sensor.mqtt/) a sample configuration is below:

```yaml
binary_sensor:
  - platform: mqtt
    name: "Pi Motion Sensor"
    state_topic: "CHANNEL/Motion/Switch"
    device_class: motion
    payload_on: "1"
    payload_off: "0"
```

## Troubleshooting

The motion sensor is activating randomly even after reducing sensitvity.

There seems to be an issue (especially with the Raspbbery Pi 3) with having the Wifi module active and having it setting off the PIR.

Try turning off the wlan0 interface and see if it works.
```shell
$ sudo ifconfig wlan0 down
```

If you get better performance, take a look at permanently disabling your wlan0 card (For RPI 3):

```shell
$ echo "dtoverlay=pi3-disable-wifi" | sudo tee -a /boot/config.txt
```
Note to renable it, you will need to remove the above line from your /boot/config.txt file