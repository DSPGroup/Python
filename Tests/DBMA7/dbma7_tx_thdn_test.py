## Test ID:
USER_NAME = 'Bar'
FOLDER_PATH = r"C:\\Users\bar.kristal\Documents\GitHub\Python\Tests\DBMA7."
TEST_NAME = "dbmA7_tx_thdn_test

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


def tx_thdn_config(A7):
	'''configure TX path for the test'''




process = 'TYP' #'FF' / 'SS'
oven = VotschVT4002(OVEN_ADDRESS)
A7 = UartDeviceTC(name="TC", com="COM6", baudrate=115200, parity='E', stopbits=1, boot_file=TC55B01_BOOT_FILE)


temp_list           = ['-40', '25', '90']
gear_list           = ['auto']
qual_list           = ['auto']
noise_gating_list   = ['off']
output_load_list    = ['32000', '16000']
vcca_list           = ['1.7, 1.8', '2']

#inital Excel file:
wb1, full_path = create_excel_file(DIR_NAME, LOG_NAME_EXCEL)
ws1 = wb1.create_sheet("thd+n_test_{}".format(prosess))


#define the values for this test:
colomns_dict = {}
colomns_list = ['process',
                'temp[C]',
                'VCCA[V]',
                'gear_number',
                'quality',
				'noise gating',
                'THD result',
                'THD result_units',
                'THD+N result',
                'THD+N result_units']

#define a colomn number for every value:
for col, value in enumerate(colomns_list):
	colomns_dict[value] = col
	# insert healines into Excel:
	ws1.cell(row=1, column=col).value = value
wb1.save(full_path)

#initial the row number
current_row = 1


for temp in temp_list:
	oven.wait_for_temp(temp)

	for load in output_load_list:
		electronic_load = KikusuiPLZ70UA(ELECTRONIC_LOAD_ADDRESS)
		electronic_load.set_resistance(load)

		for vcca in vcca_list:
			for gear in gear_list:
				for qual in qual_list:
						for noise_gating in noise_gating_list:
							current_row += 1

							#config TX PATH
							tx_thdn_config(A7)

							#measure noise level with APX525;
							# THD_resutls, thd_units = SequenceMode_THD_from_project(THD_project)
							# THDN_resutls, thdn_units = SequenceMode_THDN_Ratio_from_project(THDN_project)

							#insert values into Excel
							ws1.cell(row=current_row, column=colomns_dict['process']).value = process
							ws1.cell(row=current_row, column=colomns_dict['temp[C]']).value = temp
							ws1.cell(row=current_row, column=colomns_dict['VCCA[V]']).value = vcca
							ws1.cell(row=current_row, column=colomns_dict['gear_number']).value = gear
							ws1.cell(row=current_row, column=colomns_dict['quality']).value = qual
							ws1.cell(row=current_row, column=colomns_dict['noise_gating']).value = noise_gating
							ws1.cell(row=current_row, column=colomns_dict['THD result']).value = THD_resutls
							ws1.cell(row=current_row, column=colomns_dict['THD result_units']).value = thd_units
							ws1.cell(row=current_row, column=colomns_dict['THD+N result']).value = THDN_resutls
							ws1.cell(row=current_row, column=colomns_dict['THD+N result_units']).value = thdn_units


							wb1.save(full_path)