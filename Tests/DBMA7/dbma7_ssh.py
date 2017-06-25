## Test ID:
USER_NAME = 'Bar'
FOLDER_PATH = r"C:\Users\bar.kristal\Documents\GitHub\Python\Tests\DBMA7."
TEST_NAME = "dbmA7_ssh"

## Defines
#boot file path for the initialization of UartDeviceTC():
TC55B01_BOOT_FILE = r"C:\Users\bar.kristal\Documents\GitHub\Python\Tests\TC55B01\classd_boot_166.bin"
dbma7_boot_file = r"t:\art\TCIII\script\ram_boot.bin"

#call the init.py module:
import paramiko
execfile(r"C:\Users\bar.kristal\Documents\GitHub\Python\init.py")


##################################################################################################
rpi_address = "172.19.66.17"
rpi_username = "pi"
rpi_password = "Validation23"


RPI = RaspberryPi(rpi_address, rpi_username, rpi_password)


print RPI.read_register_A7('0x0')
RPI.write_register_A7('0x0', '0x0004')
print RPI.read_register_A7('0x0')

print RPI.send("sudo python host_valab.py det_internal")
print RPI.send("sudo python host_valab.py atc3 reset")
print RPI.send("sudo python host_valab.py det_internal")

RPI.close()