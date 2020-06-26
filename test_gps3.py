
def gps_default():
    from gps3 import gps3

    gps_socket = gps3.GPSDSocket()
    data_stream = gps3.DataStream()
    gps_socket.connect()
    gps_socket.watch()
    for new_data in gps_socket:
        if new_data:
            data_stream.unpack(new_data)
            print('Altitude = ', data_stream.TPV['alt'])
            print('Latitude = ', data_stream.TPV['lat'])

def gps_attributes():
    from gps3 import agps3

    gps_socket = agps3.GPSDSocket()
    data_stream = agps3.DataStream()
    gps_socket.connect()
    gps_socket.watch()
    for new_data in gps_socket:
        if new_data:
            data_stream.unpack(new_data)
            print('Altitude = ', data_stream.alt)
            print('Latitude = ', data_stream.lat)