##############################################################################################
## This module contains classes for working with DSPG chips.                                ##
## Uart device is a class for working with the DBM series, or any other chip that can       ##
## communicate through serial connection.                                                   ##
## Lauterbach is a class for working with the DVF series.                                   ##   
## In order to work with the Lauterbach class, one should have the python-api files saved in##
##'c:\\T32' directory. The files can be found at G:\chip_validation\T32_python_api.         ##                                                           
## Author: Bar Kristal                                                                      ##
## Date: 15/11/16                                                                           ##
## Edited by:                                                                               ##
##############################################################################################

#Note:  in this module there is a use of a syntax that belong to string type: " 'some string with {} inside'.format(word) ".
# This syntax is very similar to the printing syntax: "%s %d" %(word,int), and the reason for using the first one in this module 
# is the command syntax of the Lauterbach, which also contains a lot of % within itself.


class UartDevice():
	def __init__(self, name, com, baudrate=115200, bytesize=8, parity='N', stopbits=1,timeout=1):
		self.name=name
		self.ser=serial.Serial()
		self.ser.close()
		self.ser.port = com
		self.ser.baudrate = baudrate
		self.ser.bytesize = bytesize
		self.ser.parity = parity
		self.ser.stopbits = stopbits
		self.ser.timeout = timeout
		self.ser.open()

	#Close the serial connection with the device
	def close(self):
		self.ser.close()

	#Changing the serial connection's parameters:
	def change_port(self, com):
		self.ser.port = com
		write_to_log("{} port changed to {}".format(self.name, com))
	def change_baudrate(self, baudrate):
		self.ser.baudrate = baudrate
		write_to_log("{} baudrate changed to {}".format(self.name, baudrate))
	def change_bytesize(self, bytesize):
		self.ser.bytesize= bytesize
		write_to_log("{} bytesize changed to {}".format(self.name, bytesize))
	def change_parity(self, parity):
		self.ser.parity= parity
		write_to_log("{} parity changed to {}".format(self.name, parity))
	def change_stopbits(self, stopbits):
		self.ser.stopbits= stopbits
		write_to_log("{} stopbits changed to {}".format(self.name, stopbits))
	def change_timeout(self, timeout):
		self.ser.timeout= timeout
		write_to_log("{} timeout changed to {}".format(self.name, timeout))


	#Write data to the serial port
	def write_data(self, data):
		self.ser.write(data)

	#Read data from serial port
	def read_data(self):
		data = ""
		c = self.ser.read(1)
		while c != "\r" and c != "\n":
			print c
			data += c
			c = self.ser.read(1)
		return data



	#Sync with the device, up to n attempts.
	def sync (self, n):
		data_in = ''
		i=0
		if (self.name in ['DBMD2','TC', 'A7']):
			sync_seq = ('AcAcA'+chr(255))*30
		elif (self.name in ['DBMD4','DBMD6','DBMD7']):
			sync_seq = chr(0x0)*20
		else:
			write_to_log('No sync method for this type of chip. Please make sure that you enterd the right name')
			write_to_log("Sync failed")
			return
		while (i < n):
			self.ser.write(sync_seq)
			time.sleep(0.3)
			data_in = self.ser.read(2)
			if data_in == "OK":
				time.sleep(0.1)
				write_to_log("Synced!")
				break

			else:
				write_to_log("Sync failed")
				write_to_log("Startover Sync function, loop number: "+str(i))
				write_to_log("Please restart %s" % self.name)
				i=i+1


	def load_boot_file(self, file_name):
		if self.name in ['TC']:
			self.load_file(file_name, 4)
			self.exeBootFile()
		else:
			self.load_file(file_name, 0)
			self.exeBootFile()

	def load_file(self, file_name, unsent_bytes):
		infile = open(file_name, "rb")
		bytes_to_send = infile.read()
		# wakeup()
		if (unsent_bytes == 0):
			self.ser.write(str(bytes_to_send))
		else:
			self.ser.write((str(bytes_to_send))[:-unsent_bytes])
		time.sleep(1)
		self.ser.flushInput()

	def exeBootFile(self):
		self.ser.write(chr(0x5A))
		self.ser.write(chr(0x0B))
		time.sleep(0.5)
		if (self.name == 'TC'):
			self.change_baudrate(1843200)
			self.change_parity('N')
			time.sleep(0.1)
			version = self.read_version()
			write_to_log("Version check returned: %s" % version)
			time.sleep(0.1)
			if (version == '15'):
				write_to_log("Boot Succeeded")
			else:
				write_to_log("Boot Failed")

		elif (self.name == 'A7'):
			self.change_baudrate(3000000)
			self.change_parity('N')
			self.change_stopbits(1)
			# version = self.read_version()
			# write_to_log("Version check returned: %s" % version)
			# time.sleep(0.1)
			# if (version == '0'):
			# 	write_to_log("Boot Succeeded")
			# else:
			# 	write_to_log("Boot Failed")
		else:
			self.ser.write("19r")
			time.sleep(0.5)
			version = self.ser.read(5)
			print version
			write_to_log("Chip type check return: " + str(version)[:4])
			time.sleep(0.1)
			if (version[:3] == 'dbd'):
				write_to_log("Boot Succeeded")
			else:
				write_to_log("Boot Failed")



	########## BEFORE BOOT FILE HAS BEEN LODED: ############

	#Read from apb registers after boot file loaded:
	def read_apb_reg(self, address):
		# fill with zero for 8 bit word
		address = address.zfill(8)
		# convert hexa value to ascii and divide to little indian
		addr6 = binascii.unhexlify(address[6]+address[7])
		addr4 = binascii.unhexlify(address[4]+address[5])
		addr2 = binascii.unhexlify(address[2]+address[3])
		addr0 = binascii.unhexlify(address[0]+address[1])

		self.ser.write(chr(0x5A)+chr(0x07)+addr6+addr4+addr2+addr0)
		time.sleep(0.1)
		reg = self.ser.read(20)
		reg = reg.zfill(8)
		# convert ascii to hex value
		# apb_reg = binascii.hexlify(reg[5])+binascii.hexlify(reg[4])+binascii.hexlify(reg[3])+binascii.hexlify(reg[2])
		apb_reg = binascii.hexlify(reg[7]) + binascii.hexlify(reg[6]) + binascii.hexlify(reg[5]) + binascii.hexlify(
			reg[4])   #change by Bar, 18.4.17
		return apb_reg

	#Write to apb registers after boot file loaded:
	def write_apb_reg(self, address, value):
		# fill with zero for 8 bit word
		value = value.zfill(8)
		address = address.zfill(8)
		# convert hexa value to ascii and divide to little indian
		val6 = binascii.unhexlify(value[6]+value[7])
		val4 = binascii.unhexlify(value[4]+value[5])
		val2 = binascii.unhexlify(value[2]+value[3])
		val0 = binascii.unhexlify(value[0]+value[1])

		# convert hexa value to ascii and divide to little indian
		addr6 = binascii.unhexlify(address[6]+address[7])
		addr4 = binascii.unhexlify(address[4]+address[5])
		addr2 = binascii.unhexlify(address[2]+address[3])
		addr0 = binascii.unhexlify(address[0]+address[1])

		# write apb register- command to D4
		self.ser.write(chr(0x5A)+chr(0x04)
						+addr6+addr4
						+addr2+addr0
						+val6+val4
						+val2+val0)

	#Clear bits from apb register's value. This function can be used after loading boot file.
	def apb_clear_bits(self, address, bits_to_clr):
		bits_to_clr = int(bits_to_clr, 16)  # convert to number
		current_value = self.read_apb_reg(address)
		current_value = int(current_value, 16)  # convert to number
		new_value = current_value & (~bits_to_clr)  # zero the bits wanted
		new_value = hex(new_value)[2:]  # convert to hex (string) and cut the 0x-prefix
		self.write_apb_reg(address, new_value)

	#Set bits is apb register's value. This function can be used after loading boot file.
	def apb_set_bits(self, address, bits_to_set):
		bits_to_set = int(bits_to_set,16) # convert to number
		current_value = self.read_apb_reg(address)
		current_value = int(current_value,16)  # convert to number
		new_value = current_value | bits_to_set  # set the bits wanted
		new_value = hex(new_value)[2:]  # convert to hex (string) and cut the 0x-prefix
		self.write_apb_reg(address, new_value)


	######## AFTER LOADING BOOT FILE: #############

	#Write to a FW register. The function doesn't read the register after the writing.
	def write_register(self, register_num, value):
		self.ser.flushInput()
		time.sleep(0.01)
		#wakeup
		value = (str(value)).zfill(4)
		register_num = (str(register_num)).zfill(3)
		self.ser.write(register_num + "w" + value)

	#Read a FW register
	def read_register(self, register_num):
		self.ser.flushInput()
		time.sleep(0.01)
		#wakeup()
		register_num = (str(register_num)).zfill(3)
		self.ser.write(register_num + "r")
		time.sleep(0.01)
		value = self.ser.read(5)[:4]
		write_to_log("reg: 0x" + register_num + " ; value: 0x" + str(value))
		return str(value)

	# Write to an APB register
	def write_IO_port (self, address, value):
		self.ser.flushInput()
		address = (str(address)).zfill(8)
		address_msb = address [:4]
		address_lsb = address [4:8]
		value = (str(value)).zfill(8)
		value_msb = value [:4]
		value_lsb = value [4:8]
		#wakeup()
		self.ser.write("006w" + address_msb)
		time.sleep (0.001)
		self.ser.write("005w" + address_lsb)
		time.sleep (0.001)
		self.ser.write("007w" + value_lsb)
		time.sleep (0.001)
		self.ser.write("008w" + value_msb)

	# Read an APB register
	def read_IO_port (self, address):
		self.ser.flushInput()
		time.sleep (0.001)
		address = (str(address)).zfill(8)
		address_msb = address [:4]
		address_lsb = address [4:8]
		#wakeup()
		self.ser.write("006w" + address_msb)
		time.sleep (0.001)
		self.ser.write("005w" + address_lsb)
		time.sleep (0.001)
		self.ser.write("007r")
		self.ser.reset_input_buffer()
		time.sleep(0.5)
		value_lsb = self.ser.read(5)[:4]
		self.ser.write("008r")
		value_msb = self.ser.read(5)[:4]
		return str(value_msb)+str(value_lsb)

	def IO_port_set_bits(self, address, bits_to_set):
		current_val = self.read_IO_port(address)
		new_val = hex(int(current_val, 16) | int(bits_to_set, 16)).lstrip('0x')
		self.write_IO_port(address, new_val)

	def IO_port_clear_bits(self, address, bits_to_clear):
		current_val = self.read_IO_port(address)
		new_val = hex(int(current_val, 16) & ~int(bits_to_clear, 16)).lstrip('0x')
		self.write_IO_port(address, new_val)



##########################################################################################################

T32_OK = 0
T32_DEV = 1
# NOTE: every script that using the LAUTERBACH should close the connection
# with the device at the end by calling the function ".close()"
class Lauterbach():
	def __init__(self, name):
		self.name = name
		# Start TRACE32 instance
		exception_1_raised=1
		exception_2_raised=1
		num_of_attempts=2 #attempts to connect to LAUTERBACH
		count=0
		T32_is_open=0
		while (exception_2_raised and count < num_of_attempts):
			exception_2_raised=0
			count += 1
			while (exception_1_raised):
				exception_1_raised=0
				try:
					for i in psutil.pids():
					  if (psutil.Process(i).name()== "t32marm.exe"):
						T32_is_open=1
				except:
					write_to_log("error raised while initializing LAUTERBACH")
					exception_1_raised=1
			if (not T32_is_open):
				t32_exe = os.path.join('C:\\','T32','t32marm.exe')
				config_file = os.path.join('C:\\' ,'T32', 'config.t32')
				start_up = os.path.join('C:\\','T32','demo', 'arm', 'compiler', 'arm', 'cortexm.cmm')
				command = [t32_exe, '-c', config_file, '-s', start_up]
				process = subprocess.Popen(command)
				# Wait until the TRACE32 instance is started
				time.sleep(5)

			# Load TRACE32 Remote API
			if platform.architecture()[0] == '32bit':   # check the system's architecture
				self.t32api = ctypes.cdll.LoadLibrary(r'C:\T32\t32api.dll')   #32bit
			elif platform.architecture()[0] == '64bit':
				self.t32api = ctypes.cdll.LoadLibrary(r'C:\T32\t32api64.dll') #64bit
			else:
				write_to_log(r"Error- can't determine the system's architecture")
			# Configure communication channel:
			self.t32api.T32_Config(b"NODE=",b"localhost")
			self.t32api.T32_Config(b"PORT=",b"20000")
			self.t32api.T32_Config(b"PACKLEN=",b"1024")
			# Establish communication channel:
			rc1 = self.t32api.T32_Init()
			rc2 = self.t32api.T32_Attach(T32_DEV)
			rc3 = self.t32api.T32_Ping()
			if (rc2 != T32_OK or rc3 != T32_OK):
				exception_2_raised=1
				self.close()
		if count == num_of_attempts:
			write_to_log("Error- failed to connect to Lautebach after {} attempts".format(count+1))
		# Start PRACTICE script - run dvf101_app.cmm
		self.t32api.T32_Cmd(b"CD.DO {}".format(T32_APP_CMM_PATH))
		time.sleep(2)


	def close(self):
		self.t32api.T32_Exit()

	def write_register(self, address, value, length="LONG"):
		command= "DATA.SET 0x{} %LE %{} 0x{}".format(address, length, value)
		if (self.t32api.T32_Cmd(command) != T32_OK):
			write_to_log("error while writing to 0x{}".format(address))

	def read_register(self, address, length="LONG"):
		self.t32api.T32_Cmd("PRINT")
		command = "print data.{}(A:0x{})".format(length ,address)
		if (self.t32api.T32_Cmd(command) != T32_OK):
			write_to_log("Error while reading from 0x{}".format(address))
			return ""
		else:
			status = ctypes.c_uint16(-1)
			message = ctypes.create_string_buffer(256)
			mrc = self.t32api.T32_GetMessage(ctypes.byref(message), ctypes.byref(status))
			return message.value.decode("utf-8")

	#set only the specified bits_to_set with value_to_set
	def set_bits(self, address, bits_to_set, value_to_set, length="LONG"):
		command = "PER.Set.Field A:{} %{} 0x{} {}".format(address, length ,str(bits_to_set), str(value_to_set))
		if (self.t32api.T32_Cmd(command) != T32_OK):
			write_to_log("error while writing to 0x{}".format(address))


	#set to 0 only the specified bits
	def clear_bits(self, address, bits_to_clear, length="LONG"):
			command = "PER.Set.Field A:{} %{} 0x{} {}".format(address, length ,str(bits_to_set), '0')
			if (self.t32api.T32_Cmd(command) != T32_OK):
				write_to_log("error while writing to 0x{}".format(address))


	#Execute a cmm file.  the function should get the full path of the .cmm file
	def execute_cmm_file(self, cmm_file):
		command = "CD.DO {}".format(cmm_file)
		if (self.t32api.T32_Cmd(command) != T32_OK):
			write_to_log("Error while executing {}".format(cmm_file))
		else:
			write_to_log("{} executed successfully".format(cmm_file))
  

###############################################################################################################

#This class is used for communicating with the analog Test Chip of DBM series.
#The communication is set through DBMD2 chip, that is connected to the Test Chip through SPI, and is using the FW_boot_file
#of nir michael, and the ART commands.
class UartDeviceTC(UartDevice):
	def __init__(self, name, com, baudrate=115200, bytesize=8, parity='N', stopbits=1,timeout=1, boot_file=r"t:\art\classc\script\classd_boot_166.bin"):
		UartDevice.__init__(self, name, com, baudrate, bytesize, parity, stopbits, timeout)
		self.name=name
		self.sync(10)
		self.load_boot_file(boot_file)
		time.sleep(1)



	#Write to register of the Test Chip:
	def write_register(self, address, value):
		if type(address) == str:
			address = address.lower().lstrip('0x')
		if type(address) in [int, long]:
			address = hex(address).rstrip('L').lower().lstrip('0x')


		if type(value) == str:
			value = value.lower().lstrip('0x')
		if type(value) in [int, long]:
			value = hex(value).rstrip('L').lower().lstrip('0x')

		time.sleep(0.05)
		self.write_data("\r\ntc_write 0x{} 0x{}\r\n".format(address, value))
		self.ser.reset_input_buffer()
		self.ser.reset_output_buffer()
		print self.read_register(address)

	#Read a register of the Test Chip:
	def read_register(self, address):
		if type(address) == str:
			address = address.lower().lstrip('0x')
		if type(address) in [int, long]:
			address = hex(address).rstrip('L').lower().lstrip('0x')

		unknown = 0
		while not unknown:
			self.ser.reset_input_buffer()
			command = "tc_read 0x{}\r\n".format(address)
			self.write_data(command)
			time.sleep(0.05)
			input = ''
			c = self.ser.read(1)
			while c != '\n':
				c = self.ser.read(1)
			c = self.ser.read(1)
			while c != '\n':
				input += c
				c = self.ser.read(1)
			input = input.replace(chr(0), '').replace(' ','').rstrip('\r')
			if input != 'Unknowncommand':
				unknown = 1
		return input

	#Set bits in a register of the Test Chip:
	def tc_setbits(self, address, bits_to_set):
		if type(address) == str:
			address = address.lower().replace('0x', '')
		elif type(address) in [int, long]:
			address = hex(address).rstrip('L').lower().replace('0x', '')

		if type(bits_to_set) == str:
			bits_to_set = bits_to_set.lower().replace('0x', '')
		elif type(bits_to_set) in [int, long]:
			bits_to_set = hex(bits_to_set).rstrip('L').lower().replace('0x', '')

		self.write_data("\r\ntc_setbits 0x{} 0x{}\r\n".format(address, bits_to_set))
		self.ser.reset_input_buffer()
		self.ser.reset_output_buffer()

	#Clear bits in a register of the Test Chip:
	def tc_clrbits(self, address, bits_to_clr):
		if type(address) == str:
			address = address.lower().replace('0x', '')
		elif type(address) in [int, long]:
			address = hex(address).rstrip('L').lower().replace('0x', '')

		if type(bits_to_clr) == str:
			bits_to_clr = bits_to_clr.lower().replace('0x', '')
		elif type(bits_to_clr) in [int, long]:
			bits_to_clr = hex(bits_to_clr).rstrip('L').lower().replace('0x', '')

		self.write_data("\r\ntc_clrbits 0x{} 0x{}\r\n".format(address, bits_to_clr))
		self.ser.reset_input_buffer()
		self.ser.reset_output_buffer()


	def tc_modify_register(self, address, bits_to_modify, mask):
		if type(address) == str:
			address = address.lower().replace('0x', '')
		elif type(address) in [int, long]:
			address = hex(address).rstrip('L').lower().replace('0x', '')

		if type(bits_to_modify) == str:
			bits_to_modify = bits_to_modify.lower().replace('0x', '')
		elif type(bits_to_modify) in [int, long]:
			bits_to_modify = hex(bits_to_modify).rstrip('L').lower().replace('0x', '')

		if type(mask) == str:
			mask = mask.lower().replace('0x', '')
		elif type(mask) in [int, long]:
			mask = hex(mask).rstrip('L').lower().replace('0x', '')

		bits_to_set = hex(int(bits_to_modify, 16) & int(mask, 16))[2:].rstrip('L')
		self.tc_setbits(address, bits_to_set)
		bits_to_clr = hex((int(bits_to_modify,16) ^ 0xffffffff) & int(mask, 16))[2:].rstrip('L')
		self.tc_clrbits(address, bits_to_clr)
		print self.read_register(address)

	def read_version(self):
		flag = 0
		while not flag:
			self.ser.reset_input_buffer()
			self.write_data("\r\nversion\r\n")
			time.sleep(0.001)
			input = ''
			c = self.ser.read(1)
			while c != '\n':
				c = self.ser.read(1)
			c = self.ser.read(1)
			while c != '\n':
				input += c
				c = self.ser.read(1)
			input = input.replace(chr(0), '').replace(' ','').rstrip('\r')
			if input != 'Unknowncommand':
				flag = 1
		return input





class UartDeviceD7FPGA(UartDevice):
	def __init__(self, name, com, baudrate=115200, bytesize=8, parity='N', stopbits=1,timeout=1):
		UartDevice.__init__(self, name, com, baudrate, bytesize, parity, stopbits, timeout)
		self.name=name


	#Write to register of the Test Chip:
	def write_register(self, address, value):
		if type(address) == str:
			address = address.lower().lstrip('0x')
		if type(address) in [int, long]:
			address = hex(address).rstrip('L').lower().lstrip('0x')


		if type(value) == str:
			value = value.lower().lstrip('0x')
		if type(value) in [int, long]:
			value = hex(value).rstrip('L').lower().lstrip('0x')

		time.sleep(0.05)
		self.write_data("\r\naw 0x{} 0x{}\r\n".format(address, value))
		self.ser.reset_input_buffer()
		self.ser.reset_output_buffer()
		# print self.read_register(address)

	#Read a register of the Test Chip:
	# def read_register_old(self, address):
	# 	if type(address) == str:
	# 		address = address.lower().lstrip('0x')
	# 	if type(address) in [int, long]:
	# 		address = hex(address).rstrip('L').lower().lstrip('0x')
	#
	# 	unknown = 0
	# 	while not unknown:
	# 		time.sleep(0.1)
	# 		self.ser.reset_input_buffer()
	# 		command = "ad 0x{}\r\n".format(address)
	# 		self.write_data(command)
	# 		# time.sleep(0.05)
	# 		input = ''
	# 		c = self.ser.read(1)
	# 		while c != '\n':
	# 			c = self.ser.read(1)
	# 		c = self.ser.read(3)
	# 		while c != ' ':
	# 			c = self.ser.read(1)
	#
	# 		c = self.ser.read(1)
	# 		while c != '\n':
	# 			input += c
	# 			c = self.ser.read(1)
	#
	# 		if input != 'Unknowncommand':
	# 			unknown = 1
	#
	# 		input = input.replace(chr(0), '').split(' ')
	# 		for p in input:
	# 			if p != '':
	# 				input = p
	# 				break
	# 		# input = input.replace(chr(0), '').replace(' ','').rstrip('\r')
	# 	return input

		# Read a register of the Test Chip:
	def read_register(self, address):
		if type(address) == str:
			address = address.lower().lstrip('0x')
		if type(address) in [int, long]:
			address = hex(address).rstrip('L').lower().lstrip('0x')

		unknown = 0
		while not unknown:
			self.ser.reset_input_buffer()
			command = "ar 0x{}\r\n".format(address)
			self.write_data(command)
			# time.sleep(0.05)
			input = ''
			c = self.ser.read(1)
			while c != '\n':
				c = self.ser.read(1)
			c = self.ser.read(1)
			while c != '\n':
				input += c
				c = self.ser.read(1)
			input = input.replace(chr(0), '').replace(' ', '').rstrip('\r').replace('0x', '')
			if input != 'Unknowncommand':
				unknown = 1
		return input

	#Set bits in a register of the Test Chip:
	def setbits(self, address, bits_to_set):
		if type(address) == str:
			address = address.lower().replace('0x', '')
		elif type(address) in [int, long]:
			address = hex(address).rstrip('L').lower().replace('0x', '')

		if type(bits_to_set) == str:
			bits_to_set = bits_to_set.lower().replace('0x', '')
		elif type(bits_to_set) in [int, long]:
			bits_to_set = hex(bits_to_set).rstrip('L').lower().replace('0x', '')

		self.write_data("\r\napb_setbits 0x{} 0x{}\r\n".format(address, bits_to_set))
		self.ser.reset_input_buffer()
		self.ser.reset_output_buffer()

	#Clear bits in a register of the Test Chip:
	def clrbits(self, address, bits_to_clr):
		if type(address) == str:
			address = address.lower().replace('0x', '')
		elif type(address) in [int, long]:
			address = hex(address).rstrip('L').lower().replace('0x', '')

		if type(bits_to_clr) == str:
			bits_to_clr = bits_to_clr.lower().replace('0x', '')
		elif type(bits_to_clr) in [int, long]:
			bits_to_clr = hex(bits_to_clr).rstrip('L').lower().replace('0x', '')

		self.write_data("\r\napb_clrbits 0x{} 0x{}\r\n".format(address, bits_to_clr))
		self.ser.reset_input_buffer()
		self.ser.reset_output_buffer()


	def modify_register(self, address, bits_to_modify, mask):
		if type(address) == str:
			address = address.lower().replace('0x', '')
		elif type(address) in [int, long]:
			address = hex(address).rstrip('L').lower().replace('0x', '')

		if type(bits_to_modify) == str:
			bits_to_modify = bits_to_modify.lower().replace('0x', '')
		elif type(bits_to_modify) in [int, long]:
			bits_to_modify = hex(bits_to_modify).rstrip('L').lower().replace('0x', '')

		if type(mask) == str:
			mask = mask.lower().replace('0x', '')
		elif type(mask) in [int, long]:
			mask = hex(mask).rstrip('L').lower().replace('0x', '')

		bits_to_set = hex(int(bits_to_modify, 16) & int(mask, 16))[2:].rstrip('L')
		self.apb_setbits(address, bits_to_set)
		bits_to_clr = hex((int(bits_to_modify,16) ^ 0xffffffff) & int(mask, 16))[2:].rstrip('L')
		self.apb_clrbits(address, bits_to_clr)
		print self.read_register(address)

	def read_version(self):
		flag = 0
		while not flag:
			self.ser.reset_input_buffer()
			self.write_data("version\r\n")
			time.sleep(0.001)
			input = ''
			c = self.ser.read(1)
			while c != '\n':
				c = self.ser.read(1)
			c = self.ser.read(1)
			while c != '\n':
				input += c
				c = self.ser.read(1)
			input = input.replace(chr(0), '').replace(' ','').rstrip('\r')
			if input != 'Unknowncommand':
				flag = 1
		return input


class RaspberryPi():
	def __init__(self, ip_address, user_name, user_password ):
		self.ip_address = ip_address
		self.user_name = user_name
		self.user_password = user_password
		# open an ssh connection:
		self.ssh = paramiko.SSHClient()
		self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		self.ssh.connect(self.ip_address, username=self.user_name, password=self.user_password, allow_agent=False)
		# open a channel:
		self.channel = self.ssh.invoke_shell()
		self.channel.settimeout(3)
		# check connection:
		time.sleep(0.5)
		self.read()
		check = self.send("echo check")
		if check != "check\r\n":
			write_to_log("Error: failed to open an ssh conncetion with the RaspberryPi")
			self.close
		# go to DBMA7_valab directory
		self.send("cd ../DBMA7_valab")
		# reset d2 and a7, init d2:
		self.send("sudo python host_valab.py atc3 reset")
		self.send("sudo python host_valab.py d2 reset")
		self.send("sudo python host_valab.py init_d2")
		time.sleep(1)

	def send(self, command):
		'''send command to the RaspberryPi's terminal, and returns the answer'''
		self.channel.sendall(command + '\n')
		time.sleep(0.1)
		while (not self.channel.recv_ready()):
			pass
		self.channel.recv(len(command+'\n')+1) #ignore the echo of the command itself
		return self.read()

	def read(self):
		'''reads the answer from the RaspberryPi's terminal'''
		if (not self.channel.recv_ready()):
			time.sleep(1)
			if (not self.channel.recv_ready()):
				return
		answer = self.channel.recv(8192)
		while (self.channel.recv_ready()):
			answer += self.channel.recv(8192)
		answer = answer.rsplit("{}@raspberry".format(self.user_name))[0]
		return answer

	def read_register_D2(self, address):
		answer = RPI.send("sudo python host_valab.py d2 r {}".format(address))
		answer = answer.split("value: ")[1].lstrip("0x").rstrip('\r\n')
		return answer

	def write_register_D2(self, address, value):
		RPI.send("sudo python host_valab.py d2 w {} {}".format(address, value))

	def read_register_A7(self, address):
		answer = RPI.send("sudo python host_valab.py atc3 r {}".format(address))
		answer = answer.split("value: ")[1].lstrip("0x").rstrip('\r\n')
		return answer

	def write_register_A7(self, address, value):
		RPI.send("sudo python host_valab.py atc3 w {} {}".format(address, value))

	def close(self):
		'''close connection with the RaspberryPi'''
		self.channel.close()
		self.ssh.close()


