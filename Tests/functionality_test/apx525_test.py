################################################################
## Test ID:
USER_NAME = 'Bar'
FOLDER_PATH = r"C:\\Users\bar.kristal\Documents\GitHub\Python\Tests\apx500_functionality_test"
TEST_NAME = "apx500_test"


#call the init.py module:
execfile(r"C:\Users\bar.kristal\Documents\GitHub\Python\init.py")
execfile(r"C:\Users\bar.kristal\Documents\GitHub\Python\apx500_module.py")

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
    if SNR.HasSequenceResults:
        readingValues = SNR.SequenceResults[MeasurementResultType.SignalToNoiseRatioMeter].GetMeterValues()
        units = SNR.SequenceResults[MeasurementResultType.SignalToNoiseRatioMeter].MeterUnit

    for i in range(len(readingValues)):
        results.append(readingValues[i])
    return results, units



def SequenceMode_THDN_from_project(project_path):
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
    if THD_N.HasSequenceResults:
        readingValues = THD_N.SequenceResults[MeasurementResultType.ThdNRatioMeter].GetMeterValues()
        units = THD_N.SequenceResults[MeasurementResultType.ThdNRatioMeter].MeterUnit
    results = []
    for i in range(len(readingValues)):
        results.append(readingValues[i])

    show_fft_new_thread(APx)
    return results, units


def show_scope(APx):
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
    plt.show()


def show_fft(APx):
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
    plt.show()


def show_scope_new_thread(APx):
    thread = threading.Thread(target=show_scope, args=(APx,))
    thread.start()


def show_fft_new_thread(APx):
    thread = threading.Thread(target=show_fft, args=(APx,))
    thread.start()


###########################################
## Main ###################################

# SNR_resutls, units = SequenceMode_SNR_from_project(r"C:\Users\bar.kristal\Documents\GitHub\Python\Tests\apx500_functionality_test\SNR_test2.approjx")
# for i in range(len(SNR_resutls)):
#     print "SNR result on channel %d is: %f%s" % (i + 1, SNR_resutls[i], units)

THDN_resutls, units = SequenceMode_THDN_from_project(r"C:\Users\bar.kristal\Documents\GitHub\Python\Tests\apx500_functionality_test\THD_test2.approjx")
for i in range(len(THDN_resutls)):
    print "THD+N result on channel %d is: %f%s" %(i + 1, THDN_resutls[i], units)
