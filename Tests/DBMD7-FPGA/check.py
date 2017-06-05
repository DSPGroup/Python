
## Test ID:
USER_NAME = 'Bar'
FOLDER_PATH = r"C:\\Users\bar.kristal\Documents\GitHub\Python\Tests\DBMD7-FPGA\check"
TEST_NAME = "check"

#defines:
T32_APP_CMM_PATH = r"T:\\barkristal\DVF101\SPI\scripts\dvf101_app.cmm"

#call the init.py module:
execfile(r"C:\Users\bar.kristal\Documents\GitHub\Python\init.py")
#######################################################################################



## Uart_Device:

# D6 = UartDevice('DBMD6', 'COM13', baudrate=912600, bytesize=8, parity='N', stopbits=1,timeout=1)
# D6.change_baudrate(115200)
# print D6.ser.baudrate
# D6.sync(10)
# D6.load_boot_file(r'T:\Barkristal\VT_D6_ver_293_Sen333.bin')
# print D6.read_IO_port('3000000')

D7 = UartDeviceD7FPGA('DBMD4', 'COM9', baudrate=912600, bytesize=8, parity='N', stopbits=1,timeout=1)
# D4.sync(10)
# D6.load_boot_file(r'T:\Barkristal\VT_D6_ver_293_Sen333.bin')
print D7.read_register('3000000')
print D7.read_register('3000008')
print D7.read_register('3000040')
print D7.read_register('3000024')