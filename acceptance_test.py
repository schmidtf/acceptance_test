
import subprocess
import serial
import ftplib
import time
import sys

username = "my_use$"
passw  = "34FG98@S5^7#"

filename = "1kHzseg.wav"

num_filenames = 10

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
    input('Ensure file "devs.txt" is closed -- Please press enter once "devs.text" is closed\n\r')

    try:
        d = serial.Serial(comport, baudrate=9600, timeout=3)
        print ('connected, entering WiFi credentials\n\r')
    except:
        print ('serial connect FAIL - BAD')
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
    time.sleep(0.5)
    #print 'readline: %s\n\r' % d.readline()
    d.write("LuceraLabs\r\n".encode())
    time.sleep(0.5)
    #print 'readline: %s\n\r' % d.readline()
    d.write("3\r\n".encode())
    time.sleep(0.5)
    #print 'readline: %s\n\r' % d.readline()
    d.write("rick_james_bitch!\r\n".encode())
    print ('Wake should now connect to WiFi...wait for status LED to breath cyan...\n\r')
    print ('if the status LED continues to blink green or blink cyan, hold CTRL, then press c, then put Wake Unit in the "Bad Wifi" bin')
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

    p = input('\n\rOnce the Wake Unit status LED is breathing cyan (connected to WiFi + Particle Clout), Press ENTER to upload WAV files...')

    try:
        s = serial.Serial(comport, baudrate=9600, timeout=20)
        print ('Serial connection Good!')
    except:
        print ('Serial Connection FAIL - BAD')
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

    ipaddr = "192.168.1." + lt

    print ('writing WAV file to Wake SD card via FTP\n\r')

    #class ftplib.FTP(host='', user='', passwd='', acct='', timeout=None, source_address=None)
    ftp = ftplib.FTP(ipaddr, username, passw, "account", 40)
    #ftp.login(username, passw)
    ftp.set_debuglevel(2)

    #for files in num_filenames:
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
    try:
        s = serial.Serial(comport, baudrate=9600, timeout=20)
        print ('Serial connection Good!\n\r')
    except:
        print ('Serial Connection FAIL - BAD')
        sys.exit()
    print('plug in 9V power plug to Wake Unit...\n\r')

    lt = input("Once Wake Unit is plugged in to 9V power, press ENTER\n\r")

    # send command to beging unit test
    s.write('t'.encode())

    data = ""

    while (data != "Unit Test Complete\r\n"):
        while  s.in_waiting == 0:
            pass
        # convert to ascii string for comparison
        data = str(s.readline(),'ascii')
        print ('received data from Wake Unit: %s\n\r' % data)

################################################################################################################

print ('\n\rWelcome to Wake acceptance testing!\n\r')

ent = input('Connect micro USB cable to Wake Unit, then press ENTER\n\r')

if ent =="":
    comport = "COM3"
else:
    comport = "COM" + ent
    print('com port is %s\n\r' %comport)

ut = input("If the Wake status LED is blinking blue, press 1, then press ENTER\n\r\n\r" +
            "If the Wake status LED is breathing cyan, press 2, then press ENTER\n\r"   +
            "Press 3 to only upload WAV files via FTP (Wake status LED must be breathing cyan)")

if ut == "1":
    connectLuceraWifi()
    programFirmwareDFU()
    uploadWAV_FTP()
    unitTest()

elif ut == "2":
    programFirmwareDFU()
    uploadWAV_FTP()
    unitTest()

elif ut == "3":
    uploadWAV_FTP()
