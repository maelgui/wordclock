#!/usr/bin/env python3
# simple inquiry example
import bluetooth
import struct
import time
import messages_pb2

def send_message(sock, message):
    """ Send a serialized message (protobuf Message interface)
        to a socket, prepended by its length packed in 4
        bytes (big endian).
    """
    s = message.SerializeToString()
    packed_len = struct.pack('>B', len(s))
    sock.sendall(packed_len + s)

def get_message(sock):
    """ Read a message from a socket. msgtype is a subclass of
        of protobuf Message.
    """
    #type_buf = socket_read_n(sock, 1)
    #msg_type = struct.unpack('<B', type_buf)[0]
    len_buf = socket_read_n(sock, 1)
    msg_len = struct.unpack('<B', len_buf)[0]
    msg_buf = socket_read_n(sock, msg_len)

    #if (msg_type == 1):
    #    msgtype = message_pb2.Temperature
    #elif (msg_type == 2):
    #    msgtype = message_pb2.Status
    #else:
    #    raise Exception("Unknown message")
    msgtype = messages_pb2.Message
    msg = msgtype()
    msg.ParseFromString(msg_buf)
    return msg

def socket_read_n(sock, n):
    """ Read exactly n bytes from the socket.
        Raise RuntimeError if the connection closed before
        n bytes were read.
    """
    buf = b''
    while n > 0:
        data = sock.recv(n)
        if data == '':
            raise RuntimeError('unexpected connection close')
        buf += data
        n -= len(data)
    return buf

"""
nearby_devices = bluetooth.discover_devices(lookup_names=True)
print("Found {} devices.".format(len(nearby_devices)))

for i, (addr, name) in enumerate(nearby_devices):
    print(f"  {i} - {addr} - {name}")

while True:
    try:
        i = int(input("Choose device: "))
        if 0 <= i < len(nearby_devices):
            break
        else:
            raise ValueError()
    except ValueError:
        print(f"Please enter a number between 0 and {len(nearby_devices)}")
        i = -1
"""
#socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
#socket.connect(("98:D3:61:FD:60:E1", 1))
#socket.connect(("98:D3:61:F9:2B:FD", 1))

print('Connected')
#socket.settimeout(None)
time.sleep(3)
i = 0
while True :
    message = messages_pb2.Message()
    message.key = messages_pb2.Message.BRIGHTNESS
    message.value = i % 255
    s = message.SerializeToString()
    print(s)
    i += 1
    print(f"Send: Brightness {i}")
    #send_message(socket, message)
    #data = socket.recv(4096)
    #data = get_message(socket)
    #print(f'Received {data.key}')

socket.close()
