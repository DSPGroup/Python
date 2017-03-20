
## Test ID:
USER_NAME = 'Bar'
FOLDER_PATH = r"C:\\Users\bar.kristal\Documents\GitHub\Python\Tests\functionality_test"
TEST_NAME = "excel_test"

#call the init.py module:
execfile(r"C:\Users\bar.kristal\Documents\GitHub\Python\init.py")

#defines:
headlines = ["Block", "Temp", "Voltage", "Result"]
temps = ["-40C", "25C", "80C"]
voltages = ["0.9", "1.1", "1.2"]
blocks = ["PTCM", "RAM", "DTCM"]

block_col = 1
temp_col = 2
volt_col = 3
result_col = 4

#######################################################################################

wb1, full_path = create_excel_file(DIR_NAME, LOG_NAME_EXCEL)
ws1 = wb1.create_sheet("BIST results")

# thermotron = Termotron3800(TERMOTRON_TCP_IP)
# pwr_sply = QL355TPPwrSply(POWER_SUPLLY_ADDRESS)
# dmm = Agillent34401A(DMM_ADDRESS)


#write headlines to excel
for i in range(len(headlines)):
    ws1.cell(row=1, column=i+1).value = headlines[i]
wb1.save(full_path)

current_row = 2

#start test and write results to excel
for temp in temps:
    # thermotron.set_temp(temp)

    for volt in voltages:
        # pwr_sply.set_volt(volt)

        for block in blocks:

            '''run test on the block'''

            #result:
            if len(block) % 2 == 0:
                result = "Pass"
            else:
                result = "Fail"

            #write results:
            ws1.cell(row=current_row, column=block_col).value = block
            ws1.cell(row=current_row, column=temp_col).value = temp
            ws1.cell(row=current_row, column=volt_col).value = volt
            ws1.cell(row=current_row, column=result_col).value = result

            #upgarde row number
            current_row += 1

            #save excel file
            wb1.save(full_path)



