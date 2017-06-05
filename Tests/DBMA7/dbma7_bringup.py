## Test ID:
USER_NAME = 'Bar'
FOLDER_PATH = r"C:\\Users\bar.kristal\Documents\GitHub\Python\Tests\DBMA7."
TEST_NAME = "dbmA7_bringup"

## Defines
#boot file path for the initialization of UartDeviceTC():
TC55B01_BOOT_FILE = r"C:\Users\bar.kristal\Documents\GitHub\Python\Tests\TC55B01\classd_boot_166.bin"
dbma7_boot_file = r"t:\art\TCIII\script\ram_boot.bin"

#call the init.py module:
import math
execfile(r"C:\Users\bar.kristal\Documents\GitHub\Python\init.py")
execfile(r"C:\Users\bar.kristal\Documents\GitHub\Python\Tests\TC55B01\TC55b_regs.py")
execfile(r"C:\Users\bar.kristal\Documents\GitHub\Python\Tests\TC55B01\TC55b_defs.py")
##################################################################################################

A7 = UartDeviceTC(name="A7", com="COM22", baudrate=921600, parity='E', stopbits=2, boot_file=dbma7_boot_file)
# A7.change_baudrate(3000000)

# A7.write_register('3000000', 'ffffaaaa')
chk = A7.read_register('3000000')
print chk
