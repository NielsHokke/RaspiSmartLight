# Room control

## Project Description

Raspberry Pi based room control system, light control, addressable led strip control, fan control, Button listener, and more.

### Hardware
* Raspberry Pi 2 or 3
* Power supply for Raspberry, 5V
* Power supply for LED-strips, 12V
* [Relay shield](https://www.aliexpress.com/item/32760607353.html)
* [White LED-stip](https://www.aliexpress.com/item/32865928526.html)
* [RGB LED-strip](https://www.aliexpress.com/item/32682015405.html)
* Mosfets
* pullup resisors
* Prototype PCB

[How to connect](//TODO_make_schematic_of_hardware)

### Software

* Python3

## Getting Started

### Raspberry Pi Setup
Install [Raspbian Lite](https://www.raspberrypi.org/downloads/raspbian/) using [these instructions](https://www.raspberrypi.org/documentation/installation/installing-images/README.md)

login using 
user: pi
Pass: raspberry

Enter the following line in the terminal window
```
sudo raspi-config   
```
Change the default user password 

under Localistaion options set time-zone
Set keyboard layout to English (US)

Select Interfacing Options and enable:
* SSH

Give Pi static ip
```
sudo nano /etc/dhcpcd.conf
```

uncomment and edit the following lines at the bottom of the file and save the file

```
static ip_address=192.168.178.202/24
static routers=192.168.178.1
static domain_name_servers=8.8.8.8 fd51:42f8:caae:d92e::1
```

crtl-x, y, enter, to save the file

Reboot Pi

```
sudo reboot now
```

Connect to the Pi using SSH (Putty) 

```
sudo nano /etc/apt/sources.list
```

Comment out first line  
add:
```
deb http://mirror.transip.net/raspbian/raspbian/ stretch main contrib non-free rpi
```
to get: 
```
deb http://mirror.transip.net/raspbian/raspbian/ stretch main contrib non-free rpi
#deb http://raspbian.raspberrypi.org/raspbian/ stretch main contrib non-free rpi
# Uncomment line below then 'apt-get update' to enable 'apt-get source'
#deb-src http://raspbian.raspberrypi.org/raspbian/ stretch main contrib non-free rpi
```
crtl-x, y, enter, to save the file 

Update and upgrade system
```
sudo apt-get update
sudo apt-get dist-upgrade
```

### Python development setup
Install python3 and pip and pip3 on Pi
python2.x only used for zbat/qr-code reader. if not running QRcode.py not needed.
```
sudo apt-get install python3
sudo apt-get install python3-pip
sudo apt-get install python-pip
```

#### Pycharm project
Install [Pycharm](https://www.jetbrains.com/pycharm/) professional (community edition does not have remote development, professional is free for students)  

Clone this repository on your Windows computer
```
//TODO this repo
```

PyCharm -> File->Open->Select the [THIS PROJECT] folder you just cloned

#### Pycharm Deployment
PyCharm -> Tools -> Deployment-> Configuration

Name: Frontdoor  

**Tab Connection**  
* Type: SFTP
* SFTP host: ip of Pi
* port: 22
* Root path: /  
* Username: pi  
* Password: {Your password}
* Check Save password 
* leave Web server root as is

**Tab Mappings**  
click on add another mapping and add:

| Local Path                           | Deployment Path    | Web Path  |
| ------------------------------------ | ------------------ | -         |
| [your path]/SmartFrontdoor/Frontdoor | /home/pi/Frontdoor | /         |
| [your path]/SmartFrontdoor/www       | /home/pi/www       | /         |

click OK

#### Pycharm interpreter
Next we need to configure the remote interpreter in PyCharm.  
PyCharm -> File -> Settings -> Project -> Project Interpreter -> Gearwheel -> Add Remote.
Select Deployment configuration,and select Frontdoor. Then as the Python interpreter path set:
```
/usr/bin/python3
```
Click OK

#### Uploading scripts
Now we need to upload the scripts from our local machine to the Pi.  
This can be done by right clicking each python file in pycharms project viewer en selecting Upload to Frontdoor  

They should appear in the Remote Host tab in /home/pi/Frontdoor and /home/pi/www

To get the www script on the right place run the following command for each script in the www folder
```
sudo cp /home/pi/www/[script].py /var/www/html/dgi-bin/[script].py
```
This must be done every time one of these scripts is modified, As only from /var/www/html/dgi-bin/ can the scripts be accesed over the internet

#### Install Python libraries

Using Putty or PyCharm -> Tools -> Start SSH Sesion... -> Frontdoor, connect to the Pi using SSH

```
sudo pip3 install RPi.GPIO pyzmq requests cloudinary Adafruit_PN532

sudo apt-get install libjpeg62-dev zlib1g-dev libfreetype6-dev liblcms1-dev
sudo pip install pillow zmq requests
```

```
sudo apt-get install zbar-tools
sudo apt-get install python-zbar
sudo apt-get install libzbar0
```

### Install lighttpd
```
sudo apt-get install lighttpd
```

```
sudo nano /etc/lighttpd/lighttpd.conf
```
add the following line to ser.modules
```
server.modules = (
        "mod_access",
        "mod_alias",
        "mod_compress",
        "mod_redirect",
        "mod_cgi",      # add this line
)

``` 
And add the following lines to the bottom of the file
```
$HTTP["url"] =~ "^/cgi-bin/" {
        cgi.assign = ( ".py" => "/usr/bin/python" )
}
cgi.assign = (".cgi" => "")
```

### Install mjpg-streamer

Setup [streamer](https://github.com/jacksonliam/mjpg-streamer)
```
# Update & Install Tools
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install build-essential libjpeg8-dev imagemagick libv4l-dev cmake -y

# Clone Repo in /tmp
cd /tmp
git clone https://github.com/jacksonliam/mjpg-streamer.git
cd mjpg-streamer/mjpg-streamer-experimental

# Make
make
sudo make install
```

modifi stream_simple.html for Frontdoor app
```
sudo nano /usr/local/share/mjpg-streamer/www/stream_simple.html
```
change to
```
<html>
  <head>
    <title>MJPG-Streamer - Stream Example</title>
  </head>
  <body style="margin: 0 0 0 0;">
    <center>
      <img src="./?action=stream" />
    </center>
  </body>
</html>
```

To manualy start and test run
```
sudo modprobe bcm2835-v4l2
sudo /usr/local/bin/mjpg_streamer -i "input_uvc.so -d /dev/video0 -f 30 -q 80" -o "output_http.so -p 8080 -w /usr/local/share/mjpg-streamer/www"
```

### Start automatically on boot
To make all scripts start on boot eddit /etc/rc.local
```
sudo nano /etc/rc.local
```
Add the following
```
# Load PiCamera
modprobe bcm2835-v4l2

# Start video stream
/usr/local/bin/mjpg_streamer -i "input_uvc.so -d /dev/video0 -f 15 -q 80" -o "output_http.so -p 8080 -w /usr/local/share/mjpg-streamer/www" -b

# Frontdoor python scripts
python3 /home/pi/Frontdoor/Doorbell.py &
python3 /home/pi/Frontdoor/DoorButtonSender.py &
python3 /home/pi/Frontdoor/DoorLEDListener.py &
python3 /home/pi/Frontdoor/DoorLockListener.py &
python3 /home/pi/Frontdoor/DoorLockRemote.py &
python3 /home/pi/Frontdoor/DoorNFCSender.py &
python /home/pi/Frontdoor/QRcode.py &
python3 /home/pi/Frontdoor/TempHumid.py &

```
Then save using crtl-x and confirm.  
Reboot to start scripts
```
sudo reboot
```

To kill and restart one of the python processes run:
```
sudo pkill -f [name of script].py
sudo python3 [name of script].py & (& is optinal to run in background)
```

## Contributors 
* Niels Hokke
* Mark Röling