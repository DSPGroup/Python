################################################################
## Test ID:
USER_NAME = 'Bar'
FOLDER_PATH = r"C:\\Users\bar.kristal\Documents\GitHub\Python\Tests\functionality_test"
TEST_NAME = "tektronix_test"


T32_APP_CMM_PATH = r"T:\\barkristal\DVF101\SPI\scripts\dvf101_app.cmm"


execfile(r"C:\Users\bar.kristal\Documents\GitHub\Python\init.py")

################################################################



wave_gen = HP33120aWaveGen('GPIB0::12::INSTR')
wave_gen.generate("SIN", 3000, 1.5, 0)



scope = PyTektronixScope.TektronixScope(SCOPE_ADDRESS)
print scope.get_channel_position(1)
scope.start_acq()
time.sleep(2)
scope.channel_on(1)
scope.channel_on(2)
print scope.is_channel_selected(1)
scope.stop_acq()
print scope.meas("frequency", 1)
#print scope.meas_frequency(1)
x1, y1 = scope.read_data_one_channel(1)

scope.display_waveform_one_channel(x1, y1, 1)


print scope.meas("frequency", 1)
print scope.meas("delay", 1, 2)
print scope.meas("delay", 2, 1)
print scope.meas("phase", 1, 2)

wave_gen.output_off()
wave_gen.close()