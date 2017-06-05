
## Test ID:
USER_NAME = 'Bar'
FOLDER_PATH = r"C:\\Users\bar.kristal\Documents\GitHub\Python\Tests\DBMD7-FPGA\timers"
TEST_NAME = "timers_watchdog"


#call the init.py module:
execfile(r"C:\Users\bar.kristal\Documents\GitHub\Python\init.py")
#######################################################################################



###### defines: ######

TIMER0_BASE = '50'


timer = 0   #set the TIMER to be tested
ITERATIONS = 3

BASE = TIMER0_BASE
MASK = 0x10


D7 = UartDeviceD7FPGA('DBMD4', 'COM9', baudrate=912600, bytesize=8, parity='N', stopbits=1,timeout=1)





#enable TIMERS_LP_EN and TIMERS23_EN:
D7.setbits('3000024', '110')




## watchdog mode :
write_to_log("####watchdog test on TIMER%d:####"%timer)


#set timer value:
D7.write_register(BASE +'0000c', "8000000")
time.sleep(1)
write_to_log( D7.read_register(BASE +'00010') )


#TIMER_OUT_R cleared by setting CT,watchdog mode:
D7.setbits(BASE +'00004', '8')
D7.write_register(BASE +'00000', '14')  #sub-mode 2 (NMI)


#clear TC:
# D7.setbits(BASE + '00004', '4')
#clear TIMER0 interrupt at EICR
D7.write_register('200000c', 'ffff')
time.sleep(0.01)
interrupt0 = int(D7.read_register('2000004'),16)


#start counting down
D7.setbits(BASE +'00008', '1')
time.sleep(0.1)


timer_cc = D7.read_register(BASE +'00010')
timer_cc_prev = timer_cc
while( timer_cc != '0'):
	time.sleep(1)
	write_to_log(timer_cc)
	timer_cc = D7.read_register(BASE + '00010')
time.sleep(0.01)

interrupt1 = int(D7.read_register('2000004'), 16)
write_to_log("interrupt0: %x"%(interrupt0))
write_to_log("interrupt1: %x"%(interrupt1))

if (interrupt0&MASK == 0 and interrupt1&MASK == MASK):

	write_to_log("timer0 on single count mode PASSED")
else:
	write_to_log("timer0 on single count mode FAILED")






