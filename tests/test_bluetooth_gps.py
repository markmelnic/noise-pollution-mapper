
import bluetooth

with open("android_device.txt", mode='r') as android_device:
    creds = android_device.read().splitlines()
target_name = creds[0]
target_address = creds[1]
port = 3

nearby_devices = bluetooth.discover_devices()

for bdaddr in nearby_devices:
    if target_name == bluetooth.lookup_name( bdaddr ):
        target_address = bdaddr
        break

if target_address is not None:
    print("Found", target_name, "bluetooth device with address", target_address)
else:
    print("Could not find target bluetooth device")

# find phone port
port = 0
socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
while True:
    try:
        socket.connect((target_address, port))
        print("Successfully connected!")
        break
    except:
        port += 1
        print(port)

print(socket)
data = ""
while True:
    data = socket.recv(1024)
    print(data)

socket.close()
