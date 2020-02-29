#!/usr/bin/env python
import time

from ant.core import driver, node
from ant.core.constants import *

from PowerMeterTx import PowerMeterTx
from SpeedCadenceSensorRx import SpeedCadenceSensorRx
from config import DEBUG, LOG, NETKEY, POWER_CALCULATOR, POWER_SENSOR_ID, SENSOR_TYPE, SPEED_SENSOR_ID

antnode = None
speed_sensor = None
power_meter = None

try:
    print "Using " + POWER_CALCULATOR.__class__.__name__

    stick = driver.USB2Driver(None)
    antnode = node.Node(stick)
    print "Starting ANT node"
    antnode.start()
    network = node.NetworkKey(name='N:ANT+', key=NETKEY)
    antnode.setNetworkKey(0, network)

    print "Starting speed sensor"
    try:
        # Create the speed sensor object and open it
        speed_sensor = SpeedCadenceSensorRx(antnode, SENSOR_TYPE, SPEED_SENSOR_ID)
        speed_sensor.open()
        # Notify the power calculator every time we get a speed event
        speed_sensor.notify_change(POWER_CALCULATOR)
    except Exception as e:
        print"speed_sensor  error: " + e.message
        speed_sensor = None

    print "Starting power meter with ANT+ ID " + repr(POWER_SENSOR_ID)
    try:
        # Create the power meter object and open it
        power_meter = PowerMeterTx(antnode, POWER_SENSOR_ID)
        power_meter.open()
    except Exception as e:
        print "power_meter error: " + e.message
        power_meter = None

    # Notify the power meter every time we get a calculated power value
    POWER_CALCULATOR.notify_change(power_meter)

    print "Main wait loop"
    while True:
        try:
            time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            break

except Exception as e:
    print "Exception: "+repr(e)
    
finally:
    if speed_sensor:
        print "Closing speed sensor"
        speed_sensor.close()
        speed_sensor.unassign()
    if power_meter:
        print "Closing power meter"
        power_meter.close()
        power_meter.unassign()
    if antnode:
        print "Stopping ANT node"
        antnode.stop()
