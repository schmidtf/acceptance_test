
import subprocess
import serial
import ftplib
import time

username = "my_use$"
passw  = "34FG98@S5^7#"

filename = "1kHzseg.wav"

# class serial.Serial
# __init__(port=None, baudrate=9600

print ('welcome to Wake acceptance testing: show me potato salad...')

try:
    d = serial.Serial("COM3", baudrate=9600, timeout=3)
    print ('connected, entering WiFi credentials')
except:
    print 'serial connect FAIL - BAD'
    sys.exit()

d.write("i".encode())
print ('dev ID: %s\n\r' % d.readline())
d.write("w".encode())
#while(d.readline() != "SSID "):
#    pass
time.sleep(0.5)
#print 'readline: %s\n\r' % d.readline()
d.write("LuceraLabs\r\n")
time.sleep(0.5)
#print 'readline: %s\n\r' % d.readline()
d.write("3\r\n")
time.sleep(0.5)
#print 'readline: %s\n\r' % d.readline()
d.write("rick_james_bitch!\r\n".encode())
print ('Wake should now connect to WiFi...wait for status LED to breath cyan...')
d.close()
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
subprocess.call(["dfu-util", "-d", "2b04:d008", "-a", "0", "-s", "0x80A0000:leave", "-D", "unitTestLocal.bin"])

p = input('Once Wake Unit has connected to WiFi...Press ENTER...')

try:
    s = serial.Serial("COM3", baudrate=9600)
    print ('Serial connection Good!')
except:
	print ('Serial Connection FAIL - BAD')

print('starting Wake FTP server for file transfer to SD card')

s.write('6'.encode())
while  s.in_waiting == 0:
    pass
line = s.readline()
if(line == "Can't access SD card. Do not reformat."):
    print("SD CARD BAD - FAIL")
    sys.exit()
else:
    print ('received data from Wake Unit: %s\n\r' % line)

lt = input("Enter last digits of IP Address: ")

ipaddr = "192.168.1." + lt

print ('writing WAV file to Wake SD card via FTP')

#class ftplib.FTP(host='', user='', passwd='', acct='', timeout=None, source_address=None)
ftp = ftplib.FTP(ipaddr, username, passw, "account", 40)
#ftp.login(username, passw)
ftp.set_debuglevel(2)
ftp.storbinary("STOR " + filename, open(filename, 'rb'))

while  s.in_waiting == 0:
    pass
print ('received data from Wake Unit: %s\n\r' % s.readline())

ftp.quit()

print('plug in 9V power to Wake now...\n\r')

lt = input("Press ENTER was Wake is plugged in to 9V power...")

# send command to beging unit test
s.write('t'.encode())

data = ""

while (data != "Unit Test Complete\r\n"):
    while  s.in_waiting == 0:
        pass
    # convert to ascii string for comparison
    data = str(s.readline(),'ascii')
    print ('received data from Wake Unit: %s\n\r' % data)



# # expected message: Unit Test begin: scan for target...
# print ('received data from Wake Unit: %s\n\r' % s.readline())
#
# #expected message: found target - targetStepLocation: XY
# while  s.in_waiting == 0:
#     pass
# print ('received data from Wake Unit: %s\n\r' % s.readline())
#
# # expected message: File open success, playing WAV file
# while  s.in_waiting == 0:
#     pass
# print ('received data from Wake Unit: %s\n\r' % s.readline())
#
# # wait for wav file play complete
# while  s.in_waiting == 0:
#     pass
# print ('received data from Wake Unit: %s\n\r' % s.readline())
#
# # wait for wav file play complete
# while  s.in_waiting == 0:
#     pass
# print ('received data from Wake Unit: %s\n\r' % s.readline())


#
# print "hello\n\r"
# available = []
# for i in range(50):
# 	try:
# 		s = serial.Serial(i)
# 		print 'Connection successful on COM'+str(i+1)
# 		available.append('COM'+str(i+1))
# 		s.close()
# 	except:
# 		print 'Connection fail on COM'+str(i+1)
# 		pass
# print available
# for q in available:
# 	print '%s is available\n\r' % q
