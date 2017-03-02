################################################################
## Test ID:
FOLDER_PATH = r"C:\GitHub\Python\DVF101"
FOLDER_NAME = "Log"
TEST_NAME = "DVF101_MIPS_test"

#################################################################

execfile(r"C:\GitHub\Python\init.py")


########################
DMM = Agillent34401A(DMM_ADDRESS, RESOURCE_MANAGER) #init DMM
dvf101 = Lauterbach("DVF101")                       #from test1.py
address = '5301000'



cmm_path = r"G:\Chip_Validation\sasone\DVF101\MIPS\DVF101_PLL1_Configuration.cmm" #changing frequency and measure the current on VDD_1V1
dvf101.execute_cmm_file(cmm_path)

configuration_list = ['b03c083', '903c083',
                      '1200c083', '1100c083',
                      '1000c083', 'f00c083',
                      'e00c083', 'd00c083',
                      'c00c083', 'b00c083',
                      'a00c083', '900c083',
                      '800c083', '700c083',
                      '600c083', '500c083',
                      '400c083', '300c083',
                      '200c083', '100c083',
                      'C083']


wb1, excel_full_path = create_excel_file(DIR_NAME, LOG_NAME_EXCEL)
ws1 = wb1.create_sheet("DVF101")
row_idx = 3

for config in configuration_list:
    dvf101.write_register(address, config)
    time.sleep(0.5)
    dmm_value = DMM.meas("DCV")
    ws1.cell(row=row_idx, column=3).value = dmm_value
    row_idx = row_idx+1

ws1.cell(row=2,column=3).value="DVF101_MIPS_test"
wb1.save(excel_full_path)

## Excel:


# wb1, full_path = create_excel_file(DIR_NAME, LOG_NAME_EXCEL)
# ws1 = wb1.create_sheet("new sheet is the new shit!")
# ws1.cell(row=3,column=3).value="write something"
# wb1.save(full_path)
# wb = open_excel_file(full_path)
# print wb.get_sheet_names()

    ## Lauterbach:

    # DVF101 = Lauterbach("DVF101")
    # DVF101.write_register("5300000", "5555")
    # DVF101.set_bits("5300000", "410", "40")
    # print DVF101.read_register("5300000")
    # DVF101.execute_cmm_file(br"T:\barkristal\DVF101\SPI\clkout.cmm")
    # DVF101.close()

########################
## Excel:

# wb1, full_path = create_excel_file(DIR_NAME, LOG_NAME_EXCEL)
# ws1 = wb1.create_sheet("new sheet is the new shit!")
# ws1.cell(row=1,column=1).value="write something"
# wb1.save(full_path)
# wb=open_excel_file(full_path)
# print wb.get_sheet_names()
