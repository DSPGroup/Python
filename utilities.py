##############################################################################################
## This module contains basic functions for the python environment                          ##                         
## Author: Bar Kristal                                                                      ##
## Date: 15/11/16                                                                           ##
## Edited by:                                                                               ##
##############################################################################################



class Error_file_already_exists():
    def __init__(self, file_type):
        self.type=file_type
        write_to_log("Error: %s file is already exists" %(self.type))
        
class Error_file_doesnt_exists():
    def __init__(self, file_type):
        self.type=file_type
        write_to_log("Error: %s file doesn't exists" %(self.type))


#opens a new log file, and put it into a global variable: 'CURRENT_FILE_NAME'.
#This log file is being written every time you use the function write_to_log
def open_log(dir_name,log_name):
    make_dir(dir_name) # call to the make dir function
    global CURRENT_FILE_NAME
    CURRENT_FILE_NAME = dir_name + "\\" + log_name
    print CURRENT_FILE_NAME
    openfile = open(CURRENT_FILE_NAME , 'a')
    openfile.write(log_name)
    openfile.write("\n")
    openfile.close()

#this function is being used by open_log. opens a new directory, only if it doesn't alreadt exists.
def make_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

#writes both to screen and into the log file.
def write_to_log(user_input):
	time = datetime.datetime.today().strftime('%d/%m/%Y %H:%M:%S:%f')
	print time,'\t',user_input
	write_to_file(time, user_input)

#writes to file. being used by the write_to_log function.    
def write_to_file(time, user_input):
	log_file = open(CURRENT_FILE_NAME, "a")
	log_file.write("%s\t" %time)
	log_file.write("%s\n" %user_input)
	log_file.close()

  
def baud_rate_calculation(integer, frac ,APB_clock):
    baud_rate = (1.0/16.0 * (APB_clock/(integer + frac/16)))
    return int (baud_rate)



# Create a new Excel file, returns an instance of Excel workbook(wb) and its' full path.
# The full path is for saving the workbook after changing, by typing wb.save(path)
# After creating a new file, you need to create a new sheet by typing: ws=wb.active, or ws=wb.create_sheet(sheet_name),
# and then you can insert values to the worksheet by typing:
# ws.cell(row=row_num, column=col_num).value=value
# For full documentation see openpyxl
def create_excel_file(dir_name, log_name_excel):
    make_dir(dir_name) # call to the make dir function
    full_path = dir_name + r"\\" + log_name_excel
    if os.path.exists(full_path):
        raise Error_file_already_exists('excel')
    else:
        write_to_log("New excel file opened: " + full_path)
        wb = openpyxl.Workbook()
        wb.save(full_path)
        return wb, full_path


#opens an existing excel file and returns a workbook variable 
def open_excel_file(full_path):
    if not os.path.exists(full_path):
        raise Error_file_doesnt_exists('excel')
    else:
        return openpyxl.load_workbook(full_path)
    

def play_audio_file(audio_file_name):
    winsound.PlaySound(audio_file_name, winsound.SND_FILENAME)
    write_to_log("playing audio file: " + audio_file_name)
