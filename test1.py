execfile(r"C:\Users\bar.kristal\Documents\GitHub\Python\init.py")



########################
## Uart_Device:

# D6 = UartDevice('DBMD6', 'COM13', baudrate=912600, bytesize=8, parity='N', stopbits=1,timeout=1)
# D6.change_baudrate(115200)
# print D6.ser.baudrate
# D6.sync(10)
# D6.load_boot_file(r'T:\Barkristal\VT_D6_ver_293_Sen333.bin')
# print D6.read_IO_port('3000000')



########################
## Lauterbach:

# DVF101 = Lauterbach("DVF101")
# DVF101.write_register("5300000", "5555")
# DVF101.set_bits("5300000", "410", "40")
# print DVF101.read_register("5300000")
# DVF101.execute_cmm_file(br"T:\barkristal\DVF101\SPI\clkout.cmm")
# DVF101.close()



########################
## Excel:

# wb1, full_path = create_excel_file(Dir_Name, Excel_Log_Name")
# ws1 = wb1.create_sheet("new sheet is the new shit!")
# ws1.cell(row=1,column=1).value="write something" 
# wb1.save(full_path)
# wb=open_excel_file(full_path)
# print wb.get_sheet_names()


########################
## Power Supply:

# pwr_sply = QL355TPPwrSply('GPIB0::29::INSTR',RESOURCE_MANAGER)
# print pwr_sply.name
# pwr_sply.set_volt(1,5)
# pwr_sply.read_current(1)
# pwr_sply.sense(2,1)
# pwr_sply.channel_on('1')
# pwr_sply.close()

########################
## Frequency counter:

# freq_counter = HP53131aFreqCounter(FREQUENCY_COUNTER_ADDRESS, RESOURCE_MANAGER)
# print freq_counter.name
# freq_counter.meas("freqency")
# a= freq_counter.meas("volt_min_peak")
# freq_counter.meas("phase")


########################
## Electronc load:

# load = KikusuiPLZ70UA(ELECTRONIC_LOAD, RESOURCE_MANAGER)
# print load.name
# load.reset()
# load.load_on()
# load.load_off()
# load.set_resistance("0.234")
# load.read_current("1")
# load.read_voltage("2")


########################
## Small oven:

# fridg = VotschVT4002("COM19")
# fridg.stop_chamber()
# time.sleep(3)
# fridg.wait_for_temp(82)
# time.sleep(2)
# print fridg.read_error()
# fridg.close()



########################
## Blue oven:

# termotron = Termotron3800(TERMOTRON_TCP_IP)
# termotron.stop_chamber()
# termotron.set_temp(23)
# termotron.wait_for_temp(29)
# print termotron.read_temp()
# time.sleep(3)
# termotron.stop_chamber()