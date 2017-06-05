## Test ID:
USER_NAME = 'Bar'
FOLDER_PATH = r"C:\\Users\bar.kristal\Documents\GitHub\Python\Tests\TC55B01\TC_functionality_test"
TEST_NAME = "TC_test"

## Defines
#boot file path for the initialization of UartDeviceTC():
TC55B01_BOOT_FILE = r"C:\Users\bar.kristal\Documents\GitHub\Python\Tests\TC55B01\classd_boot_166.bin"

#call the init.py module:
import math
execfile(r"C:\Users\bar.kristal\Documents\GitHub\Python\init.py")
execfile(r"C:\Users\bar.kristal\Documents\GitHub\Python\Tests\TC55B01\TC55b_regs.py")
execfile(r"C:\Users\bar.kristal\Documents\GitHub\Python\Tests\TC55B01\TC55b_defs.py")
##################################################################################################





def Temp_Sense(tc):
	# Driver.WriteRegister(atc3, 0x128, 0x13131)
	# tc.write_register('128', '13131')
	tc.write_register('128', '0f0f1')
	# Driver.WriteRegister(atc3, 0x13C, 0x40488841)
	tc.write_register('13c', '40488841')
	# Driver.WriteRegister(atc3, 0x144, 0x5A10800)
	tc.write_register('144', '5a10800')

	# Driver.WriteRegister(atc3, 0x4, 0x1002F00)
	tc.write_register('0004', '1002f00')
	# Driver.WriteRegister(atc3, 0x0, 0x1018)
	tc.write_register('0000', '1018')
	# ModifyRegister(SCU_CLK_DIV1, 0x100, 0x100)
	tc.tc_setbits('000c', '100')
	# ModifyRegister(SCU_CLK_DIV6, 0x12500000, 0xFFF00000)
	tc.tc_setbits('0058', '12500000')
	tc.tc_clrbits('0058', 'eda00000')
	# ModifyRegister(SCU_CLK_PMOD, 0x08000000, 0x08000000)
	tc.tc_setbits('20', '08000000')
	# Driver.WriteRegister(atc3, TEMP_SENSE_CFG1, 0x00000000)
	tc.write_register('0ec0', '0')
	# Driver.WriteRegister(atc3, TEMP_SENSE_CFG1, 0x37)
	tc.write_register('0ec0', '37')

	time.sleep(4)

	# Driver.WriteRegister(atc3, 0x0EC4, 0xFFF)
	tc.write_register('0ec4', 'fff')
	# Driver.WriteRegister(atc3, 0x0EC4, 0x0)
	tc.write_register('0ec4', '0')
	# Driver.WriteRegister(atc3, 0x0EC4, 0x80000000)
	tc.write_register('0ec4', '80000000')
	time.sleep(4)
	RegVal1 = tc.read_register('ec4')
	print "regVal1: %s" %RegVal1

	# Driver.WriteRegister(atc3, 0x144, 0x5A90800)
	tc.write_register('144', '5a90800')
	time.sleep(4)
	# Driver.WriteRegister(atc3, 0x0EC4, 0xFFF)
	tc.write_register('0ec4', 'fff')
	# Driver.WriteRegister(atc3, 0x0EC4, 0x0)
	tc.write_register('0ec4', '0')
	# Driver.WriteRegister(atc3, 0x0EC4, 0x80000000)
	tc.write_register('0ec4', '80000000')
	time.sleep(4)
	RegVal2 = tc.read_register('ec4')

	print "regVal2: %s" % RegVal2

	vbe1 = 1.8 * int(RegVal1, 16) / 32764
	vbe2 = 1.8 * int(RegVal2, 16) / 32764
	print "\n vbe1 " + str(vbe1)
	print "\n vbe2 " + str(vbe2)
	q = 1.6E-19
	k = 1.38E-23
	N = 4000
	offset = 0.0038
	temp = (vbe2 - vbe1 - offset) * q / (k * math.log(N)) - 273
	print "\n Measured Temperature:" + str(temp)



def vt_adc(tc):
	## config PLL:
	tc.write_register('4', '1002f00')
	tc.write_register('0', '1017')
	tc.tc_modify_register(SCU_CLK_DIV1, '100', '100')

	## config i2s0 to master, 16bit word:
	tc.write_register(SCU_I2S_CFG, '17cf')

	tc.tc_modify_register(SCU_IOIE, '00', '80')
	tc.write_register('015c', 'ff00010c')
	tc.write_register(AFE_INAMP_CFG,0x00103434)
	tc.write_register(VT_CTL_CFG2,0x80000000)
	tc.write_register(VT_CTL_CFG3,0xc0000000)
	tc.write_register(VT_CTL_CFG4,0xc0000000)
	tc.write_register(VT_CTL_CFG5,0x0024007c)
	tc.write_register(VT_CTL_CFG1,0x800000bf)
	tc.write_register(SCU_CLK_DIV5,0x00470047)
	tc.tc_modify_register(SCU_CLK_DIV7,0x0b00300,0xfff00000)
	tc.tc_modify_register(SCU_TEST_CTL1,0x02010000,0x02010000)
	tc.write_register(AFE_BGREF_CFG,0x000f0f1)

	#enable GDAC_MOD_CLK:
	tc.tc_modify_register(SCU_CLK_PMOD,0x10000000,0x10000000)

	tc.write_register(AFE_INAMP_CFG,0x010b434)
	tc.write_register(AFE_ADC_CFG,0x8cc9080e)

	#enable I2S0_CLK, VT_CLK, ADC_CLK:
	tc.tc_modify_register(SCU_CLK_PMOD,0x10011000,0x10011000)

	tc.write_register(0x12c,0x8)

tc = Uar\tDeviceTC(name="TC", com="COM4", baudrate=115200, parity='E', stopbits=1, boot_file=TC55B01_BOOT_FILE)
# Temp_Sense(tc)
vt_adc(tc)
