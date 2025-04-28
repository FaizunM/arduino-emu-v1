# import serial

# ser = serial.Serial('COM9', 115200, timeout=0.1)

# with open('capture.bin', 'wb') as f:
#     print('Capturing data')
#     while True:
#         data = ser.read(1024)
#         if data:
#             f.write(data)
#             print(data)

import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
for port in ports:
    print(port.device)