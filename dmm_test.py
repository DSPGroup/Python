################################################################
## Test ID:
FOLDER_PATH = r"C:\GitHub\Python\functionality_test"
FOLDER_NAME = "Log"
TEST_NAME = "dmm_test"

#################################################################

execfile(r"C:\GitHub\Python\init.py")


########################
## Power Supply:

# pwr_sply = QL355TPPwrSply(POWER_SUPLLY_ADDRESS, RESOURCE_MANAGER)   #init power supply
# DMM = Agillent34401A(DMM_ADDRESS, RESOURCE_MANAGER)                 #init DMM
# print pwr_sply.name
# pwr_sply.channel_on('1')
# volt_list=[0.5, 1, 2, 3.5]
# for voltage in volt_list:
#     pwr_sply.set_volt(1,voltage)
#     time.sleep(0.5)
#     DMM.meas("DCV")
#     print pwr_sply.read_current(1)
#     print voltage









# print pwr_sply.name
# pwr_sply.channel_on('1')
# volt_list=[0.5, 1, 2, 1.5]
# for voltage in volt_list:
#     pwr_sply.set_volt(1,voltage)
#     time.sleep(0.1)
#     print pwr_sply.read_current(1)
# pwr_sply.sense(1,1)
# pwr_sply.set_current_lim(1,1.32)
# pwr_sply.close()


##HEWLETT PACKARD 34401A


# print DMM.name
# DMM.meas("DCV")
# a= dmm_multimeter.meas("volt_min_peak")
# dmm_multimeter.meas("phase")