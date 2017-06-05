## Test ID:
USER_NAME = 'Bar'
FOLDER_PATH = r"C:\\Users\bar.kristal\Documents\GitHub\Python\Tests\DBMD4"
TEST_NAME = "dbmd4_leakage_test"

## Defines
#boot file path for the initialization of UartDeviceTC():
TC55B01_BOOT_FILE = r"C:\Users\bar.kristal\Documents\GitHub\Python\Tests\TC55B01\classd_boot_166.bin"

#call the init.py module:
import math
execfile(r"C:\Users\bar.kristal\Documents\GitHub\Python\init.py")
execfile(r"C:\Users\bar.kristal\Documents\GitHub\Python\Tests\TC55B01\TC55b_regs.py")
execfile(r"C:\Users\bar.kristal\Documents\GitHub\Python\Tests\TC55B01\TC55b_defs.py")
##################################################################################################

# defines:
num_of_repeat = 4

process_col         = 1
temp_col            = 2
core_voltage_col    = 3


process = 'TYP' #'TYP' / 'FF' / 'SS'

oven = VotschVT4002(OVEN_ADDRESS)
power_supply = QL355TPPwrSply(POWER_SUPLLY_ADDRESS)
dmm = Agillent34401A(DMM_ADDRESS)

power_supply.channel_off(2)
power_supply.set_volt(2, 0)
power_supply.sense(2, 0)


temp_list = ['80']
core_voltage_list = ['1.2']

#inital Excel file:
wb1, full_path = create_excel_file(DIR_NAME, LOG_NAME_EXCEL)
ws1 = wb1.create_sheet("DBMD4_leakage_test {}".format(process))

#define the values for this test:
colomns_dict = {}
colomns_list = ['process',
                'temp[C]',
                'core_voltage[V]',
				'leakage current w/o core power',
				'leakage current with core power']

#define a colomn number for every value:
for col, value in enumerate(colomns_list, 1):
	colomns_dict[value] = col
	# insert healines into Excel:
	ws1.cell(row=1, column=col).value = value
wb1.save(full_path)

current_row = 1  #initialize the row counter

for temp in temp_list:
	# oven.wait_for_temp(temp)
	oven.set_temp(temp)
	for voltage in core_voltage_list:

		for i in range(num_of_repeat):
			power_supply.set_volt(2, 0)
			power_supply.channel_on(2)
			time.sleep(0.1)
			result1 = dmm.meas('DCV')

			time.sleep(0.1)
			power_supply.set_volt(2, voltage)
			time.sleep(0.1)
			result2 = dmm.meas('DCV')

			current_row += 1

			# insert values into Excel
			ws1.cell(row=current_row, column=colomns_dict['process']).value = process
			ws1.cell(row=current_row, column=colomns_dict['temp[C]']).value = temp
			ws1.cell(row=current_row, column=colomns_dict['core_voltage[V]']).value = voltage
			ws1.cell(row=current_row, column=colomns_dict['leakage current w/o core power']).value = result1
			ws1.cell(row=current_row, column=colomns_dict['leakage current with core power']).value = result2

			wb1.save(full_path)


