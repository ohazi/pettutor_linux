#!/usr/bin/env python3

import gatt
import sys

from argparse import ArgumentParser




def done():
    print("Disconnecting...")
    device.disconnect()
    print("Stopping manager...")
    manager.stop()
    sys.exit(0)




class PetTutorDevice(gatt.Device):
    def connect_succeeded(self):
        super().connect_succeeded()
        print("[%s] Connected" % (self.mac_address))

    def connect_failed(self, error):
        super().connect_failed(error)
        print("[%s] Connection failed: %s" % (self.mac_address, str(error)))

    def disconnect_succeeded(self):
        super().disconnect_succeeded()
        print("[%s] Disconnected" % (self.mac_address))

    def characteristic_enable_notifications_succeeded(self, characteristic):
        super().characteristic_enable_notifications_succeeded(characteristic)
        print("[%s/%s] Enable notifications succeeded" % (self.mac_address, characteristic.uuid))

    def characteristic_enable_notifications_failed(self, characteristic, error):
        super().characteristic_enable_notifications_failed(characteristic, error)
        print("[%s/%s] Enable notifications failed: %s" % (self.mac_address, characteristic.uuid, str(error)))

    def characteristic_value_updated(self, characteristic, value):
        print("[%s/%s] %s" % (self.mac_address, characteristic.uuid, value.hex()))

    def characteristic_write_value_succeeded(self, characteristic):
        super().characteristic_write_value_succeeded(characteristic)
        print("[%s/%s] Write succeeded!" % (self.mac_address, characteristic.uuid))
        done()

    def characteristic_write_value_failed(self, characteristic, error):
        super().characteristic_write_value_failed(characteristic, error)
        print("[%s/%s] Write failed: %s" % (self.mac_address, characteristic.uuid, str(error)))
        done()


    def services_resolved(self):
        super().services_resolved()

        #print("[%s] Resolved services" % (self.mac_address))
        #for service in self.services:
        #    print("[%s]  Service [%s]" % (self.mac_address, service.uuid))
        #    for characteristic in service.characteristics:
        #        print("[%s]    Characteristic [%s]" % (self.mac_address, characteristic.uuid))

        pettutor_service = next(
            s for s in self.services
            if s.uuid == 'b0e6a4bf-cccc-ffff-330c-0000000000f0')

        pettutor_feed_characteristic = next(
            c for c in pettutor_service.characteristics
            if c.uuid == 'b0e6a4bf-cccc-ffff-330c-0000000000f1')

        print("[%s/%s] Attempting to write..." % (self.mac_address, pettutor_feed_characteristic.uuid))
        pettutor_feed_characteristic.write_value([])




arg_parser = ArgumentParser(description="PetTutor PC Client")
arg_parser.add_argument('-a', '--address', default="00:05:C6:28:B5:D5", help="MAC address of device to connect")
args = arg_parser.parse_args()




print("Connecting...")
manager = gatt.DeviceManager(adapter_name='hci0')
device = PetTutorDevice(manager=manager, mac_address=args.address)
device.connect()

try:
    manager.run()
except KeyboardInterrupt:
    print("Interrupted.")
    done()



