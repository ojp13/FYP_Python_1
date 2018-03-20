import serial

ser = serial.Serial('/dev/rfcomm0')
print(ser.name)
ser.write(b"0x07 0x4d 0x34 0x64 0x67 0x0B")

s = ser.read(10)

print(s)
