execfile(r"C:\Users\bar.kristal\Documents\GitHub\Python\apx525_module.py")

import matplotlib.pyplot as plt
import threading



################################################################
### some examples:
## initialize APx500
# APx = APx500_Application(APxOperatingMode.BenchMode, True)
# APx.Visible = True


### running an APx project:
# filename = 'Electrical_Test_Setup_APX_100mV_0dB.approjx'
# directory = "T:\Barkristal\DBMD6\DBMD6_electrical_functionality_tests\Tools"
# fullpath = os.path.join(directory, filename)
# APx.OpenProject(fullpath)


### BenchMode, FFT:
'''Connect the Digital Serial output to the Digital Serial input.
   The test generates a sine wave from the digital serial, and show it's FFT'''
# APx.BenchMode.Setup.OutputConnector.Type = OutputConnectorType.DigitalSerial
# APx.BenchMode.Setup.InputConnector.Type = InputConnectorType.DigitalSerial
# APx.SignalPathSetup.SerialDigitalTransmitter.EnableOutputs = True
# #APx.BenchMode.Generator.Levels.SetValue(OutputChannelIndex.Ch1, 0.02)
# APx.BenchMode.Generator.Frequency.Value = 2000
# APx.BenchMode.Generator.On = True
# fft = APx.BenchMode.Measurements.Fft
# fft.Show()
# fft.Start()
# time.sleep(2)
# xValues = fft.FFTSpectrum.GetXValues(InputChannelIndex.Ch1, VerticalAxis.Left)
# yValues = fft.FFTSpectrum.GetYValues(InputChannelIndex.Ch1, VerticalAxis.Left)
# yval = []
# xval = []
# for i in yValues:
#     yval.append(i)
# for j in xValues:
#     xval.append(j)
# plt.semilogx(xval, yval)
# plt.show()

### BenchMode, THD:
'''Connect the Digital Serial output to the Digital Serial input.
   The test generates a sine wave from the digital serial, and measure it's THD'''
# APx.BenchMode.Setup.OutputConnector.Type = OutputConnectorType.DigitalSerial
# APx.BenchMode.Setup.InputConnector.Type = InputConnectorType.DigitalSerial
# APx.SignalPathSetup.SerialDigitalTransmitter.EnableOutputs = True
# APx.BenchMode.Generator.Frequency.Value = 2000
# APx.BenchMode.Generator.On = True
# AcousticResponse = APx.BenchMode.Measurements.AcousticResponse
# AcousticResponse.Start()     #start measurements
# THD = AcousticResponse.ThdLevel
# time.sleep(2)
# xValues = THD.GetXValues(InputChannelIndex.Ch1, VerticalAxis.Left)
# yValues = THD.GetYValues(InputChannelIndex.Ch1, VerticalAxis.Left)
# yval = []
# xval = []
# for i in yValues:
#     yval.append(i)
# for j in xValues:
#     xval.append(j)
# plt.semilogx(xval,yval)
# plt.show()



### BenchMode, THD, load project:
'''Connect the Digital Serial output to the Digital Serial input.
   The test generates a sine wave from the digital serial, and measure it's THD'''
# APx.OpenProject(r"C:\Users\bar.kristal\Documents\GitHub\Python\Tests\apx500_functionality_test\THD_test.approjx")
# AcousticResponse = APx.BenchMode.Measurements.AcousticResponse
# AcousticResponse.Start()     #start measurements
# THD = AcousticResponse.ThdLevel
# time.sleep(2)
# xValues = THD.GetXValues(InputChannelIndex.Ch1, VerticalAxis.Left)
# yValues = THD.GetYValues(InputChannelIndex.Ch1, VerticalAxis.Left)
# yval = []
# xval = []
# for i in yValues:
#     yval.append(i)
# for j in xValues:
#     xval.append(j)
# plt.semilogx(xval,yval)
# plt.show()



### SequenceMode, SNR, load project:
def SequenceMode_SNR_from_project(project_path):
	'''This function loads a specified project, and returns the SNR results.
		Results are in the following form: list results, str units. The length of the results list
		 is dependent on the number of channels that turned on in the project.
		The project need to be in Sequence mode'''
	APx = APx500_Application()
	APx.Visible = True
	APx.OpenProject(project_path)
	SNR = APx.Sequence.GetMeasurement("Signal Path1", "Signal to Noise Ratio")
	SNR.Checked = True
	SNR.Run()
	show_fft(APx)  # save a figure of the FFT
	if SNR.HasSequenceResults:
		readingValues = SNR.SequenceResults[MeasurementResultType.SignalToNoiseRatioMeter].GetMeterValues()
		units = SNR.SequenceResults[MeasurementResultType.SignalToNoiseRatioMeter].MeterUnit

	results = []
	for i in range(len(readingValues)):
		results.append(readingValues[i])
	return results, units



def SequenceMode_THDN_Ratio_from_project(project_path):
	'''This function loads a specified project, and returns the THD+N results.
		Results are in the following form: list results, str units. The length of the results list
		 is dependent on the number of channels that turned on in the project.
		The project need to be in Sequence mode'''
	APx = APx500_Application()
	APx.Visible = True
	APx.OpenProject(project_path)
	THD_N = APx.Sequence.GetMeasurement("Signal Path1", "THD+N")
	THD_N.Checked = True
	THD_N.Run()   #run the measurement
	show_fft(APx)  # save a figure of the FFT
	if THD_N.HasSequenceResults:
		readingValues = THD_N.SequenceResults[MeasurementResultType.ThdNRatioMeter].GetMeterValues()
		units = THD_N.SequenceResults[MeasurementResultType.ThdNRatioMeter].MeterUnit
	results = []
	for i in range(len(readingValues)):
		results.append(readingValues[i])

	return results, units



def SequenceMode_THD_from_project(project_path):
	'''This function loads a specified project, and returns the THD results.
		Results are in the following form: list results, str units. The length of the results list
		 is dependent on the number of channels that turned on in the project.
		The project need to be in Sequence mode'''
	APx = APx500_Application()
	APx.Visible = True
	APx.OpenProject(project_path)
	THD = APx.Sequence.GetMeasurement("Signal Path1", "THD+N")
	THD.Checked = True
	THD.Run()   #run the measurement
	show_fft(APx)  # save a figure of the FFT
	if THD.HasSequenceResults:
		readingValues = THD.SequenceResults[MeasurementResultType.ThdRatioMeter].GetMeterValues()
		units = THD.SequenceResults[MeasurementResultType.ThdRatioMeter].MeterUnit
	results = []
	for i in range(len(readingValues)):
		results.append(readingValues[i])

	return results, units


def SequenceMode_SINAD_from_project(project_path):
	'''This function loads a specified project, and returns the SINAD results.
		Results are in the following form: list results, str units. The length of the results list
		 is dependent on the number of channels that turned on in the project.
		The project need to be in Sequence mode'''
	APx = APx500_Application()
	APx.Visible = True
	APx.OpenProject(project_path)
	SINAD = APx.Sequence.GetMeasurement("Signal Path1", "SINAD")
	SINAD.Checked = True
	SINAD.Run()   #run the measurement
	time.sleep(4)
	show_fft(APx) #save a figure of the FFT
	if SINAD.HasSequenceResults:
		readingValues = SINAD.SequenceResults[MeasurementResultType.SinadRatioMeter].GetMeterValues()
		units = SINAD.SequenceResults[MeasurementResultType.SinadRatioMeter].MeterUnit
	results = []
	for i in range(len(readingValues)):
		results.append(readingValues[i])

	return results, units


def SequenceMode_NoiseLevel_from_project(project_path):
	'''This function loads a specified project, and returns the Noise level results.
		Results are in the following form: list results, str units. The length of the results list
		 is dependent on the number of channels that turned on in the project.
		The project need to be in Sequence mode'''
	APx = APx500_Application()
	APx.Visible = True
	APx.OpenProject(project_path)
	Noise = APx.Sequence.GetMeasurement("Signal Path1", "Noise (RMS)")
	Noise.Checked = True
	Noise.Run()   #run the measurement
	show_fft(APx)  # save a figure of the FFT
	if Noise.HasSequenceResults:
		readingValues = Noise.SequenceResults[MeasurementResultType.NoiseRmsLevelMeter].GetMeterValues()
		units = Noise.SequenceResults[MeasurementResultType.NoiseRmsLevelMeter].MeterUnit
	results = []
	for i in range(len(readingValues)):
		results.append(readingValues[i])

	return results, units

def SequenceMode_CMRR_from_project(project_path):
	'''This function loads a specified project, and returns the CMRR results.
		Results are in the following form: list results, str units. The length of the results list
		 is dependent on the number of channels that turned on in the project.
		The project need to be in Sequence mode'''
	APx = APx500_Application()
	APx.Visible = True
	APx.OpenProject(project_path)
	CMRR = APx.Sequence.GetMeasurement("Signal Path1", "CMRR")
	CMRR.Checked = True
	CMRR.Run()   #run the measurement
	show_fft(APx)  # save a figure of the FFT
	if CMRR.HasSequenceResults:
		readingValues = CMRR.SequenceResults[MeasurementResultType.CmrrMeter].GetMeterValues()
		units = CMRR.SequenceResults[MeasurementResultType.CmrrMeter].MeterUnit
	results = []
	for i in range(len(readingValues)):
		results.append(readingValues[i])

	return results, units



def SequenceMode_frequency_response_from_project(project_path):
	'''This function loads a specified project, and returns the frequency response results.
		Results are in the following form: list results, str units. The length of the results list
		 is dependent on the number of channels that turned on in the project.
		The project need to be in Sequence mode'''
	APx = APx500_Application()
	APx.Visible = True
	APx.OpenProject(project_path)
	APx.FrequencyResponse.Start()
	level = APx.FrequencyResponse.Level
	data = level.GetValues(0, APx.FrequencyResponse.Level.AcquisitionCount - 1)
	xval = []
	yval = []
	for i in range(len(data)):
		# print "point %s: (%s %s,%s %s)"%(i, data[i].X, level.XAxis.Unit, data[i].Y, level.YAxis.Unit)
		xval.append(data[i].X)
		yval.append(data[i].Y)

	graph_path = DIR_NAME + r"\\" + TEST_NAME + r"_" + "frequency_response" + TEST_DATE + r"_" + TEST_TIME + r".png"
	plt.plot(xval, yval)
	# plt.show()
	plt.savefig(graph_path)
	return graph_path


def SequenceMode_full_sequence_from_project(project_path, results_path):
	'''This function loads a project that runs a sequence of measurments,
	 sets the path and name for the results_file to be saved,
	 and runs the sequence.'''

	APx = APx500_Application()
	APx.Visible = True
	APx.OpenProject(project_path)
	SequenceMode_change_log_path(APx, results_path)
	APx.Sequence.Run()




def SequenceMode_change_log_path(APx, log_path):
	'''
	:param  APx:      instance ot the APx_Application() class
			log_path: path for the results csv file to be saved
					  for example: log_path = "c:\DBMA7\SNR", than the results_file will be saved at:  "c:\DBMA7\SNR\date&time.csv"
	:return: none
	'''
	path = log_path+"$(Date)$(Time).csv"
	try:
		APx.Sequence.DataOutput.MeterReadingsFileName = path
	except:
		raise "path is not valid"


def show_scope(APx):
	scope_path = DIR_NAME + r"\\" + TEST_NAME + r"_" + "scope_figure" + TEST_DATE + r"_" + TEST_TIME + r".png"

	scope = APx.ScopeSignalMonitor.Scope
	yValues = scope.GetYValues(InputChannelIndex.Ch1, VerticalAxis.Left)
	xValues = scope.GetXValues(InputChannelIndex.Ch1, VerticalAxis.Left)

	yval = []
	xval = []
	for i in yValues:
		yval.append(i)
	for j in xValues:
		xval.append(j)
	plt.plot(xval, yval)
	#plt.show()
	plt.savefig(scope_path)


def show_fft(APx):
	fft_path = DIR_NAME + r"\\" + TEST_NAME + r"_" + "fft_figure" + TEST_DATE + r"_" + TEST_TIME + r".png"

	fft = APx.FftSpectrumSignalMonitor
	fft.FFTLength = FFTLength.FFT_48000
	xValues = fft.FFTSpectrum.GetXValues(InputChannelIndex.Ch1, VerticalAxis.Left)
	yValues = fft.FFTSpectrum.GetYValues(InputChannelIndex.Ch1, VerticalAxis.Left)
	yval = []
	xval = []
	for i in yValues:
		yval.append(i)
	for j in xValues:
		xval.append(j)
	plt.semilogx(xval, yval)
	#plt.show()
	plt.savefig(fft_path)


def show_scope_new_thread(APx):
	thread = threading.Thread(target=show_scope, args=(APx,))
	thread.start()


def show_fft_new_thread(APx):
	thread = threading.Thread(target=show_fft, args=(APx,))
	thread.start()


