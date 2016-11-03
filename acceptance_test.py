# Wake Accpetance Test
# Version: 2.0
# Date: 13 October 2016

import subprocess
import serial
import ftplib
import time
import sys
import textwrap

VERSION = 2.3

username = "my_use$"
passw  = "34FG98@S5^7#"

filename = "1kHzseg.wav"

filenames = [
"0004.wav",
"0005.wav",
"0006.wav",
"0007.wav",
"0008.wav",
"0009.wav",
"0010.wav",
"0011.wav",
"0012.wav",
"0013.wav",
"0014.wav",
"0015.wav",
"0016.wav",
"0017.wav",
"0018.wav",
"0019.wav",
"0020.wav",
"0021.wav",
"0022.wav",
"0023.wav"
]

filenames_short = [
"0004.wav",
"0005.wav",
"0006.wav",
"0007.wav",
"0008.wav",
"0009.wav",
"0012.wav",
"0013.wav",
"0014.wav",
"0015.wav",
"0016.wav",
"0018.wav",
"0020.wav",
"0022.wav"
]

def connectLuceraWifi():
    #input('Ensure file "devs.txt" is closed -- Please press enter once "devs.text" is closed\n\r')

    try:
        d = serial.Serial(comport, baudrate=9600, timeout=3)
        print ('connected, entering WiFi credentials\n\r')
    except:
        print ('\n\rserial connect FAIL - BAD')
        sys.exit()

    d.write("i".encode())
    devID = d.readline()
    print ('dev ID: %s' % devID)

    text_file = open("devs.txt", "w")
    text_file.write("ID: %s" % devID)
    text_file.close()

    input('open file devs.txt and record Wake Device ID into spreadsheet -- Please press Enter when done\n\r')

    d.write("w".encode())
    #while(d.readline() != "SSID "):
    #    pass
    print('entering wifi credentials 1...wait...')
    time.sleep(0.5)
    # clear read buffer
    d.readline()
    d.write("LuceraLabs\r\n".encode())
    print('entering wifi credentials 2...wait...')
    time.sleep(0.5)
    d.readline()
    # enter 3 for WPA2
    d.write("3\r\n".encode())
    print('entering wifi credentials 3...wait...')
    time.sleep(0.5)
    red = d.readline()
    if (red == "Security Cipher 1=AES, 2=TKIP, 3=AES+TKIP: "):
        print('adding security type')
        d.write("1\r\n".encode())
        time.sleep(0.5)
    #print 'readline: %s\n\r' % d.readline()
    d.write("rick_james_bitch!\r\n".encode())
    print ('Wake should now connect to WiFi...wait for status LED to breath cyan...\n\r')
    print ('if the status LED returns to blinking blue, or continues to blink green or blink cyan, hold CTRL, then press c, then put Wake Unit in the "Bad Wifi" bin')
    d.close()

def programFirmwareDFU():
    input("Press ENTER to program Wake unit with firmware...\n\r")
    try:
        e = serial.Serial(comport, baudrate=14400)
    except:
        print ('Wake unit status LED should blink yellow (DFU Mode)...\n\r')

    time.sleep(2);

    #dfu-util -d 2b04:d008 -a 0 -s 0x8020000 -D system-part1.bin

    subprocess.call(["dfu-util", "-d", "2b04:d008", "-a", "0", "-s", "0x8020000", "-D", "system-part1.bin"])

    time.sleep(1);
    #
    subprocess.call(["dfu-util", "-d", "2b04:d008", "-a", "0", "-s", "0x8060000", "-D", "system-part2.bin"])
    time.sleep(1);
    #
    subprocess.call(["dfu-util", "-d", "2b04:d008", "-a", "0", "-s", "0x80A0000:leave", "-D", "unitTestLocal.bin"])

def uploadWAV_FTP():

    p = input('\n\rOnce the Wake Unit status LED is breathing cyan (connected to WiFi + Particle Cloud), Press ENTER to upload WAV files...')

    try:
        s = serial.Serial(comport, baudrate=9600, timeout=20)
        print ('\n\rSerial connection Good!')
    except:
        print ('\n\rSerial Connection FAIL - BAD')
        sys.exit()

    print('starting Wake FTP server for file transfer to SD card\n\r')

    s.write('6'.encode())
    while  s.in_waiting == 0:
        pass
    line = s.readline()
    if(line == "Can't access SD card. Do not reformat."):
        print("SD CARD BAD - FAIL\n\r")
        sys.exit()
    else:
        print ('received data from Wake Unit: %s\n\r' % line)

    lt = input("Enter the number(s) after the last period of the of IP Address: ")

    if (lt == "i"):
        ipaddr = input("Enter IP: ")
    else:
        ipaddr = "192.168.1." + lt

    print ('writing WAV file to Wake SD card via FTP\n\r')

    #class ftplib.FTP(host='', user='', passwd='', acct='', timeout=None, source_address=None)
    ftp = ftplib.FTP(ipaddr, username, passw, "account", 40)
    #ftp.login(username, passw)
    ftp.set_debuglevel(2)

    for files in range(len(filenames_short)):
        ftp.storbinary("STOR " + filenames_short[files], open(filenames_short[files], 'rb'))
        print ('\n\rUploaded file: %s\n\r' % filenames_short[files])

    #ftp.storbinary("STOR " + filename, open(filename, 'rb'))

    while  s.in_waiting == 0:
        pass
    print ('received data from Wake Unit: %s\n\r' % s.readline())

    ftp.quit()
    # flush serial input buffer
    s.flushInput()
    s.close()

    print('Finished uploading WAV files to Wake Unit\n\r')

def unitTest():

    p = input('\n\rOnce the Wake Unit status LED is breathing cyan (connected to WiFi + Particle Clout), Press ENTER to begin Unit Test...')

    try:
        s = serial.Serial(comport, baudrate=9600, timeout=20)
        print ('Serial connection Good!\n\r')
    except:
        print ('Serial Connection FAIL - BAD, tried COM%s' % comport)
        sys.exit()

    # send command to beging unit test
    s.write('t'.encode())

    data = ""

    while (1):
        while  s.in_waiting == 0:
            pass
        # convert to ascii string for comparison
        data = str(s.readline(),'ascii')
        print ('received data from Wake Unit: %s\n\r' % data)

        if(data == "Unit Test Complete\r\n"):
            sys.exit()

################################################################################################################

print ('\n\rWelcome to Wake acceptance testing, Version %0.1f!\n\r' % VERSION)
print

#ent = input('Connect micro USB cable to Wake Unit, then press ENTER\n\r')

comport = "COM44"

# if ent =="":
#     comport = "COM3"
#     print('serial com port is %s\n\r' %comport)
# else:
#     comport = "COM" + ent
#     print('com port is %s\n\r' %comport)

print("Ensure micro USB cable and 9V power cable are connected to Wake unit\n\r")
print("Acceptance Test Options: \n\r")
print ("\tOption 1: If Wake unit does not have WiFi credentials and has not received firmware\n\r" +
       "\t(status LED is blinking blue), then Press 1 to add WiFi credentials, upload firmware, and perform Unit Test\n\r\n\r" +
       "\tOption 2: If the Wake unit is connected to WiFi and has firmware\n\r" +
       "\t(status LED is breathing cyan), then Press 2 to perform Unit Test\n\r\n\r" +
       "\tOption 3: If Wake unit has WiFi credentials and status LED blinked purple (cloud firmware upload)\n\r" +
       "\t, then press 3 to perform DFU firmware programming and Unit Test\n\r\n\r")

ut = input("Press 1, 2, or 3 for desired Option, then Press ENTER: ")

if ut == "1":
    connectLuceraWifi()
    programFirmwareDFU()
    unitTest()

elif ut == "2":
    unitTest()

elif ut == "3":
    programFirmwareDFU()
    unitTest()

elif ut == "":
    print('\n\rInvalid Input\n\r')
