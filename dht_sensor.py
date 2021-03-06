import adafruit_dht
import logging
import logging.handlers as handlers
from board import *
pin = D4
sensor = adafruit_dht.DHT22(pin, use_pulseio=False)


MSG_SND = '{{"temperature": {temperature},"humidity": {humidity}}}'


logger = logging.getLogger('dht22_sensor')
logger.setLevel(logging.INFO)
logHandler = handlers.RotatingFileHandler('dht22-sensor.log',encoding='utf-8', maxBytes=50000, backupCount=2)
logHandler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

try:
    humidity=temperature=None
    while None in (humidity, temperature):
        try:
            humidity = sensor.humidity
            temperature = sensor.temperature
        except RuntimeError:
            humidity=temperature=None
            continue
    
    msg_txt_formatted = MSG_SND.format(temperature=round(temperature,2), humidity=round(humidity,2))
    logger.info(msg_txt_formatted)
except Exception as e:
    logger.error(e)