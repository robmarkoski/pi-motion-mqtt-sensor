#!/usr/bin/python3
#
#   Pi PIR Motion Detecting MQTT Client
#
#   Version:    0.1
#   Status:     Development
#   Github:     https://github.com/robmarkoski/pi-motion-mqtt-sensor
#

import os
import logging
from gpiozero import MotionSensor
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt


PIR_GPIO = 7 # GPIO Pin of PIR Sensor

# Update this to adjust sensitivity. Default is 0.5
PIR_THRESHOLD = 0.5

# Update the follow MQTT Settings for your system.
MQTT_USER = "mqtt"              # MQTT Username
MQTT_PASS = "mqtt_password"     # MQTT Password
MQTT_CLIENT_ID = "pisensor"     # MQTT Client Id
MQTT_HOST_IP = "127.0.0.1"      # MQTT HOST
MQTT_PORT = 1883                # MQTT PORT (DEFAULT 1883)


MQTT_AUTH = {
    'username': MQTT_USER,
    'password': MQTT_PASS
}
# Set up logging.
LOG_FILE = os.path.dirname(os.path.realpath(__file__)) + "/" + "pimotion.log"      # Name of log file
LOG_LEVEL = logging.INFO     # Change info to debug for debugging.

LOG_FORMAT = "%(asctime)-15s %(message)s"
logging.basicConfig(filename=LOG_FILE,
                    level=LOG_LEVEL,
                    format=LOG_FORMAT,
                    datefmt='%Y-%m-%d %H:%M:%S')

try:
    logging.info("Creating MotionSensor Instance")
    pir = MotionSensor(PIR_GPIO, threshold=PIR_THRESHOLD)
    logging.info("MotionSensor Created - Starting Server")
    # This initial wait for below is to ensure no motion is sensed once your turning it on.
    # This is useful for using the sensor in alarm situations.
    pir.wait_for_no_motion()
    while True:
        pir.wait_for_motion()
        logging.debug("Motion Sensed.")
        logging.debug(pir.value)
        try:
            publish.single("CHANNEL/Motion/Switch",
                payload="1",
                hostname=MQTT_HOST_IP,
                client_id=MQTT_CLIENT_ID,
                auth=MQTT_AUTH,
                port=MQTT_PORT,
                protocol=mqtt.MQTTv311)
        except:
            logging.exception("MQTT Publish ON Error")
        pir.wait_for_no_motion()
        logging.debug("Motion No Longer Sensed.")
        try:
            publish.single("CHANNEL/Motion/Switch",
                payload="0",
                hostname=MQTT_HOST_IP,
                client_id=MQTT_CLIENT_ID,
                auth=MQTT_AUTH,
                port=MQTT_PORT,
                protocol=mqtt.MQTTv311)
        except:
            logging.exception("MQTT Publish OFF Error")
except KeyboardInterrupt:
    logging.info("KEY INTERRUPT - STOPPING SERVER")
except:
    logging.exception("PIR SENSOR ERROR")
