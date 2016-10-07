
import subprocess
import serial
import ftplib
import time

ut = input("Press enter to program Wake...")

try:
    e = serial.Serial("COM3", baudrate=14400)
except:
    print ('Went into DFU Mode -- Good!')

time.sleep(2);

#dfu-util -d 2b04:d008 -a 0 -s 0x8020000 -D system-part1.bin

subprocess.call(["dfu-util", "-d", "2b04:d008", "-a", "0", "-s", "0x8020000", "-D", "system-part1.bin"])

time.sleep(1);
#
subprocess.call(["dfu-util", "-d", "2b04:d008", "-a", "0", "-s", "0x8060000", "-D", "system-part2.bin"])
time.sleep(1);
#
subprocess.call(["dfu-util", "-d", "2b04:d008", "-a", "0", "-s", "0x80A0000:leave", "-D", "DAC.bin"])

print ('\n\rWake programmed...reconnect with serial terminal and type "h" for menu')
