
####################################################################################################
#   This test is an example of how to write a test, and contains a few code lines                  #
#   for every module.                                                                              #
#   Notice that every test shoulld contain the next defines:                                       #
#   #Test ID:                                                                                      #
#    USER_NAME   - this variable is being used in the init.py file, to choose the right address.   #
#    FOLDER_PATH - the path for the test's log to be saved.                                        #
#    TEST_NAME   - the test's name.                                                                #
#                                                                                                  #
#   #defines:                                                                                      #
#    T32_APP_CMM_PATH of every define that is specific to this test.                               #
#                                                                                                  #
#   #call the init.py module:                                                                      #
#    execfile(r"C:\Users\bar.kristal\Documents\GitHub\Python\init.py")                             #
####################################################################################################

## Test ID:
USER_NAME = 'Bar'
FOLDER_PATH = r"C:\\Users\bar.kristal\Documents\GitHub\Python\Tests\functionality_test"
TEST_NAME = "uart_in_new_tread"


#call the init.py module:
execfile(r"C:\Users\bar.kristal\Documents\GitHub\Python\init.py")

import threading
#######################################################################################

dvf101 = UartDevice('DVF101', com='COM3', baudrate=115200, bytesize=8, parity='N', stopbits=1,timeout=1)
string = 'dvf101 login:'
i = 0
while (True):

    if (dvf101.ser.inWaiting() > 0):  # if incoming bytes are waiting to be read from the serial input buffer
        try:
            #data_str = dvf101.ser.read(dvf101.ser.inWaiting()).decode('UTF-8')  # read the bytes and convert from binary array to ASCII
            data_str = dvf101.ser.read(1).decode('UTF-8')
            print data_str,  # print the incoming string without putting a new-line ('\n') automatically after every print()
        except:
            pass

        if data_str == string[i]:
            i += 1
        elif data_str == ' ' or data_str == '\n':
            pass
        else:
            i = 0

        if i == len(string):
            print "found"
            time.sleep(4)
            dvf101.ser.write('root\n'.encode())
            time.sleep(0.1)
            while (dvf101.ser.inWaiting() > 0):
                print dvf101.ser.read(dvf101.ser.inWaiting()).decode('UTF-8')
            time.sleep(0.1)
            dvf101.ser.write('./stress-ng --cpu 1 --cpu-load 100\n'.encode())
            time.sleep(1)
            print dvf101.ser.read(dvf101.ser.inWaiting()).decode('UTF-8')
            # for i in range(10):
            #     n = (i + 1) * 10  # n will be 10,20,30,...,100
            #     # write the command here:
            #     #
            #     #
            break

