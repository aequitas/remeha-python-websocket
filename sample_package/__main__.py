import asyncio
import struct
from websockets.sync.client import connect

def hello():
    with connect("ws://10.254.127.127:80/canopen", origin="http://10.254.127.127:80") as websocket:
        # websocket.send(b"\x00\x00\x00\x04 \x04\x00")
        # websocket.send(b"\x00\x00\x00\x03P,\x00")
        # websocket.send(b"\x00\x00\x08\x13\x00\x01 \x04\x01\x00\x01 \x04\x02\x00\x01 \x04\x03\x00\x01 \x04\x04\x00\x01 \x04\x05\x00\x01 \x04\x06\x00\x01 \x04\x07\x00\x01 \x04\x08\x00\x01 \x04\x09\x00\x01 \x04\x0a\x00\x01 \x04\x0b\x00\x01 \x04\x0c\x00\x01 \x04\x0d\x00\x01 \x04\x0e\x00\x01 \x04\x0f\x00\x01 \x04\x10\x00\x01 \x04\x11\x00\x01 \x04\x12\x00\x01 \x04\x13")
        # websocket.send(b"\x82\x87\x124Vx\x124VyB)V")
        # "\x82`\x00\x00\x01\xfeP\x1d\x00\x06<\xff\xff\xff\xff\xff\xff\xff\xff\x1e\x0a\x83\x09\x00\x00\x00\x00\x06\xff\xbc\x02\xbc\x02\xbc\x027\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x01,\x01\xff\xff\x114\x01\x00\x00\x00\x00\x80\xff\xffD\x0c2\x0a\x00\x00O\x0e\xbc\x02\x00\x00\xc9\x00\x00\x80\xd2\x00\x00\x80X\x02\x00\x80\x02\x00\x00\x00\x01\x14\x04"

        # sample = b"\x82\x87\x12\x34\x56\x78\x12\x34\x56\x79\x42\x29\x56"
        sample = b"\x00\x00\x00\x01P\x1d\x00"
        websocket.send(sample)

        # response = b"\x00\x00\x01\xfeP\x1d\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\x00\x0a\xb5\x09\x00\x00\x00\x00\x06\xff\xbc\x02\xbc\x02\xbc\x028\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x01\x00\x00\xff\xff\x110\x05\x00\x00\x00\x00\x80\xff\xff\xa6\x09\xec\x09\x00\x00O\x0e\xbc\x02\x00\x00\xc9\x00\x00\x80\xd2\x00\x00\x80X\x02\x00\x80\x02\x00\x00\x00\x01\x16\x04"
        # a6 09

        # 2024-03-17 22:13:08.6592|DEBUG|ServiceTool.IntegratedServiceTool|Response received: {"data":{"common":{"protocol.nr":6},"devices":{"1":{"boilercode":8,"dF":1,"dU":11,"manufacturer.nr":11,"name":"CU-GH08","parameter.nr":17,"serial.number":1493515309}}},"metadata":{"common":{"protocol.nr":"Ok"},"devices":{"1":{"boilercode":"Ok","dF":"Ok","dU":"Ok","manufacturer.nr":"Ok","name":"Ok","parameter.nr":"Ok","serial.number":"Ok"}}},"result":0}

        message = websocket.recv()
        print(f"Received: {message}, {len(message)}")
        # < little-endian, > big-endian
        # b signed char, B unsigned char, h short (2), H unsigned short (2)
        unpacked = struct.unpack('<17b' + 'hh37hb', message)
        print(unpacked)
        print(struct.unpack('<18b' + 'hh37h', message))
        print(struct.unpack('<17b' + '79b', message))
        # print(struct.unpack('<bhbbh'+'13hbh7b4B11bhh9b'+'hb22b', message))
        datamap = struct.unpack('<bhbbh'+'13hbh7b4B11bhh9b'+'hb22b', message)

        # bytemap = struct.unpack('<7b' + '89b', message)
        # for n, v in enumerate(bytemap):
        #     if v == 17:
        #         print(n)

        # 0 status
        # 1 substate
        print(f"Status: {struct.unpack('<B', bytes(message[7:][0:1]))[0]}")
        print(f"Substatus: {struct.unpack('<B', bytes(message[7:][1:2]))[0]}")


        print(f"Flow temp: {unpacked[17] * 0.01:0.2f} °C") # 14
        print(f"Return temp: {unpacked[18] * 0.01:0.2f} °C") #16
        print(f"Flue gas: {unpacked[21] * 0.1:0.2f} °C") # 18
        print(f"Control: {unpacked[22] * 0.01:0.2f} °C")
        print(f"Control: {unpacked[23] * 0.01:0.2f} °C")
        print(f"Control: {unpacked[24] * 0.01:0.2f} °C")
        print(f"Outside: {unpacked[25] * 0.01:0.2f} °C") # 26

        print(f"Outside: {struct.unpack('<h', bytes(message[7:][26:28]))[0]*0.01} °C")

        print(f"Fan RPM: {struct.unpack('<h', bytes(message[7:][29:31]))[0]} rpm")
        print(f"Fan RPM: {struct.unpack('<h', bytes(message[7:][31:33]))[0]} rpm")

        # print(f"Fan RPM: {struct.unpack('<h', message[36:38])[0]}")
        # print(f"Fan RPM: {struct.unpack('<h', message[38:40])[0]}")
        # 29 fan rpm
        # 31 fan setpoint
        # 44 pump speed

        #print(f"Water pressure: {bytemap[55] * 0.1:0.1f} bar") # 48
        print(f"Water pressure: {struct.unpack('<b', bytes(message[7:][48:49]))[0]*0.1:0.1f} bar")
        # for i in range(0, 95):
        #     print(f"Water pressure: {i} {struct.unpack('<b', bytes(message[i:i+1]))[0]*0.1:0.1f}")
        # 62 dhw flow rate 0.1
        # 70 room temp

if __name__ == "__main__":
    hello()


# 82 87 12 34 56 78 12 34 56 79 42 29 56
# 82 60 00 00 01 FE 50 1D 00 00 00 FF FF FF FF FF FF FF FF 1E 0A A6 09 00 00 00 00 06 FF BC 02 BC 02 BC 02 24 04 00 00 00 00 00 00 00 00 00 00 00 00 00 00 FF 01 00 00 FF FF 11 30 05 00 00 00 00 80 FF FF 64 0A 14 0A 00 00 63 0E BC 02 00 00 C8 00 00 80 D2 00 00 80 58 02 00 80 02 00 00 00 01 14 04
# treturn A6 09