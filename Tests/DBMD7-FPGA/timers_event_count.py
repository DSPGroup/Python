
## Test ID:
USER_NAME = 'Bar'
FOLDER_PATH = r"C:\\Users\bar.kristal\Documents\GitHub\Python\Tests\DBMD7-FPGA\timers"
TEST_NAME = "timers_single_count"


#call the init.py module:
execfile(r"C:\Users\bar.kristal\Documents\GitHub\Python\init.py")
#######################################################################################



###### defines: ######

TIMER0_BASE = '50'
TIMER1_BASE = '58'
TIMER2_BASE = '90'
TIMER3_BASE = '98'

timer = 1   #set the TIMER to be tested
if timer == 0:
	BASE = TIMER0_BASE
	MASK = 0x10
else:
	if timer == 1:
		BASE = TIMER1_BASE
		MASK = 0x8
	else:
		if timer == 2:
			BASE = TIMER2_BASE
			MASK = 0x400
		else:
			BASE = TIMER3_BASE
			MASK = 0x800

D7 = UartDeviceD7FPGA('DBMD4', 'COM5', baudrate=912600, bytesize=8, parity='N', stopbits=1,timeout=1)





#enable TIMERS_LP_EN and TIMERS23_EN:
D7.setbits('3000024', '110')





## event count mode :
write_to_log("####event count mode test on TIMER%d:####"%timer)

#TIMER_OUT_R cleared by setting CT:
D7.write_register(BASE +'00000', '0c')
time.sleep(0.01)
D7.setbits(BASE + '00004', '4')

#clear TIMER0 interrupt at EICR
D7.write_register('200000c', 'ffff')
time.sleep(0.1)
#read interrupt status:
interrupt0 = int(D7.read_register('2000004'),16)


#COUNTER regiser is reflected at TIMER_CC:
D7.setbits(BASE + '00004', '8')
#set timer value:
D7.write_register(BASE + '0000c', "f")
time.sleep(1)
write_to_log( D7.read_register(BASE + '00010') )
#start counting down
D7.setbits(BASE + '00004', '1')
time.sleep(1)
timer_cc = D7.read_register(BASE + '00010')
while( timer_cc != '0'):
	# write 1 to EW: (click the event counter)
	D7.write_register(BASE + '00008', '1')
	write_to_log(timer_cc)
	timer_cc = D7.read_register(BASE + '00010')
time.sleep(0.01)

interrupt1 = int(D7.read_register('2000004'), 16)
write_to_log("interrupt0: %x"%(interrupt0))
write_to_log("interrupt1: %x"%(interrupt1))

if (interrupt0&MASK == 0 and interrupt1&MASK == MASK):

	write_to_log("timer0 on event count mode PASSED")
else:
	write_to_log("timer0 on event count mode FAILED")



