from bluetooth.ble import DiscoveryService

service = DiscoveryService()
devices = service.discover(5)

print(devices.items())

for address, name in devices.items():
    print("name: {}, address: {}".format(name, address))
