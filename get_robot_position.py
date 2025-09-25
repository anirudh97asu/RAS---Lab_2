from serial.tools import list_ports
from pydobot import Dobot
import time

#Pick the first port automatically (or manually select from printed list)

# Connect Dobot
device = Dobot(port="/dev/ttyACM0")

if device:

    try:
        print("Dobot connected successfully!")

        # Get pose
        pose, joints = device.get_pose()
        print("Pose:", pose)

        # Move test
        # device.move_to(x + 20, y, z, r)
        # time.sleep(2)
        # device.move_to(x, y, z, r)

        device.close()

    except Exception as e:
        print(e)
        device.close()

    # finally:
    #      device.close()

else:
    print("Could not connect to Dobot")