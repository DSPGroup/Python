## Test ID:
USER_NAME = 'Bar'
FOLDER_PATH = r"C:\\Users\bar.kristal\Documents\GitHub\Python\Tests\DBMA7."
TEST_NAME = "dbmA7._use_cases"

## Defines
#boot file path for the initialization of UartDeviceTC():
TC55B01_BOOT_FILE = r"C:\Users\bar.kristal\Documents\GitHub\Python\Tests\TC55B01\classd_boot_166.bin"
dbma7_boot_file = r"t:\art\TCIII\ram_boot.bin"

#call the init.py module:
import math
execfile(r"C:\Users\bar.kristal\Documents\GitHub\Python\init.py")
execfile(r"C:\Users\bar.kristal\Documents\GitHub\Python\Tests\TC55B01\TC55b_regs.py")
execfile(r"C:\Users\bar.kristal\Documents\GitHub\Python\Tests\TC55B01\TC55b_defs.py")
##################################################################################################

# defines:
CMU_BASE    =                      0x0000
AFE_BASE    =                      0x0100


SCU_CLK_PMOD    =           CMU_BASE + 0x20
AFE_BGREF_CFG   =           AFE_BASE + 0x24
AFE_OUTAMP_CFG0 =           AFE_BASE + 0x0c

def tx_noise_floor_config(A7):
	'''
	1. Open the band-gap, charge-pump block and LDO,
	and enable CLK_CP.
	2. Enable the output amplifier.
	3. Enable the digital path with no specific order
	4. Enable the DAC.'''

	# # pll_configurations:
	A7.write_register('4', '1002f00')
	A7.write_register('0', '1017')

	# # enable bad-gap:
	A7.tc_setbits(AFE_BGREF_CFG, 0x1)

	# # enable CLK_CP:
	A7.tc_setbits(SCU_CLK_PMOD, 0x40000)

	# #enable LDO
	#TBD

	# # enable OUTAMP0_EN:
	A7.tc_setbits(AFE_OUTAMP_CFG0, 0x1)

	# # enable GDAC0_CLK, GDAC1_CLK, GDAC_CLK_MOD:
	A7.tc_setbits(SCU_CLK_PMOD, 0xe0000000)

	# # enable I2S:
	A7.tc_setbits(SCU_CLK_PMOD, 0x1000)


process = 'TYP' #'FF' / 'SS'
oven = VotschVT4002(OVEN_ADDRESS)

procese_col = 1
temp_col = 2
gear_col = 3
qual_col = 4
result_col = 5

temp_list           =         ['-40', '25', '90']
gear_list           =         [1, 2, 3, 4]
qual_list           =         ['LP', 'HQ', 'BTL']
output_load_list    =         ['32k', '16k']

#inital Excel file:
wb1, full_path = create_excel_file(DIR_NAME, LOG_NAME_EXCEL)
ws1 = wb1.create_sheet("Noise_floor_test_{}".format(prosess))

ws1.cell(row=1, column=procese_col).value = process
ws1.cell(row=1, column=temp_col).value = temp
ws1.cell(row=1, column=gear_col).value = 'gear_number'
ws1.cell(row=1, column=qual_col).value = 'quality'
ws1.cell(row=1, column=result_col).value = 'result'


for temp in temp_list:
	oven.wait_for_temp(temp)

	for
	tx_noise_floor_config(A7, gear_num, quality)


