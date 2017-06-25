## Test ID:
USER_NAME = 'Bar'
FOLDER_PATH = r"C:\Users\bar.kristal\Documents\GitHub\Python\Tests\DBMA7."
TEST_NAME = "test_template"

## Defines
rpi_address = "172.19.66.17"
rpi_username = "pi"
rpi_password = "pi"
apx_project_path = r"C:\Users\bar.kristal\Documents\GitHub\Python\Tests\apx500_functionality_test\SNR_test2.approjx"
apx_results_path = r"C:\Users\bar.kristal\Documents\GitHub\Python\apx500_functionality_test\full_sequence"

#call the init.py module:
import paramiko
execfile(r"C:\Users\bar.kristal\Documents\GitHub\Python\init.py")
execfile(r"C:\Users\bar.kristal\Documents\GitHub\Python\apx525_functions.py")

##################################################################################################
## test start:

#initial RPI connection
RPI = RaspberryPi(rpi_address, rpi_username, rpi_password)
#reset both D2 and A7
RPI.reset_A7()
RPI.reset_D2()
RPI.init_D2()

#call FW functions (configuration and set-ups that written in the RPI's python code):
print RPI.send("sudo python host_valab.py det_internal")

#read and write to registers
print RPI.read_register_A7('0x0')
RPI.write_register_A7('0x0', '0x0004')
print RPI.read_register_A7('0x0')

#run measurements with AudioPrecision, result saved at apx_results_path
SequenceMode_full_sequence_from_project(apx_project_path, apx_results_path)

#close connection with RPI:
RPI.close()

