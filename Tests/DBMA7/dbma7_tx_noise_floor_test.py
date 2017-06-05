## Test ID:
USER_NAME = 'Bar'
FOLDER_PATH = r"C:\\Users\bar.kristal\Documents\GitHub\Python\Tests\DBMA7."
TEST_NAME = "dbmA7_tx_noise_floor"

## Defines
#boot file path for the initialization of UartDeviceTC():
TC55B01_BOOT_FILE = r"C:\Users\bar.kristal\Documents\GitHub\Python\Tests\TC55B01\classd_boot_166.bin"

#call the init.py module:
import math
execfile(r"C:\Users\bar.kristal\Documents\GitHub\Python\init.py")
execfile(r"C:\Users\bar.kristal\Documents\GitHub\Python\Tests\TC55B01\TC55b_regs.py")
execfile(r"C:\Users\bar.kristal\Documents\GitHub\Python\Tests\TC55B01\TC55b_defs.py")
execfile(r"C:\Users\bar.kristal\Documents\GitHub\Python\apx525_functions.py")

##################################################################################################

# defines:

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
# oven = VotschVT4002(OVEN_ADDRESS)
# A7 = UartDeviceTC(name="TC", com="COM6", baudrate=115200, parity='E', stopbits=1, boot_file=TC55B01_BOOT_FILE)

#inital Excel file:
wb1, full_path = create_excel_file(DIR_NAME, LOG_NAME_EXCEL)
ws1 = wb1.create_sheet("Noise_floor_test_{}".format(process))

#define the values for this test:
colomns_dict = {}
colomns_list = ['process',
                'temp[C]',
                'VCCA[V]',
                'gear_number',
                'quality',
                'Noise level result',
                'result_units']
#define a colomn number for every value:
for col, value in enumerate(colomns_list):
	colomns_dict[value] = col
	# insert healines into Excel:
	ws1.cell(row=1, column=col).value = value
wb1.save(full_path)


temp_list           =         ['-40', '25', '90']
gear_list           =         [1, 2, 3, 4]
qual_list           =         ['LP', 'HQ', 'BTL']
output_load_list    =         ['32000', '16000']    #ohm
vcca_list           =         ['1.8']



#initial the row number
current_row = 1


for temp in temp_list:
	# oven.wait_for_temp(temp)

	for load in output_load_list:
		electronic_load = KikusuiPLZ70UA(ELECTRONIC_LOAD_ADDRESS)
		electronic_load.set_resistance(load)

		for vcca in vcca_list:

			for gear in gear_list:
				for qual in qual_list:

					if gear == 4 and qual == 'HQ':
						break
					elif qual == 'BTL' and gear != 4:
						break

					else:
						current_row += 1

						#config TX PATH
						# tx_noise_floor_config(A7, gear, qual)

						#measure noise level with APX525;
						# Noise_RMS_resutls, units = SequenceMode_NoiseLevel_from_project(Noise_Level_project)

						#insert values into Excel
						ws1.cell(row=current_row, column=colomns_dict['process']).value = process
						ws1.cell(row=current_row, column=colomns_dict['temp[C]']).value = temp
						ws1.cell(row=current_row, column=colomns_dict['VCCA[V]']).value = vcca
						ws1.cell(row=current_row, column=colomns_dict['gear_number']).value = gear
						ws1.cell(row=current_row, column=colomns_dict['quality']).value = qual
						# ws1.cell(row=current_row, column=colomns_dict['Noise level result']).value = Noise_RMS_resutls
						# ws1.cell(row=current_row, column=colomns_dict['result_units']).value = units

						wb1.save(full_path)