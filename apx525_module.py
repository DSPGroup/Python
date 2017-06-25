import sys
sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Lib') # Set the path to import pure Python Libs
sys.path.append(r"C:\Program Files (x86)\Audio Precision\APx500 4.4\API") # Set the path to import the Apx API
sys.path.append(r"C:\Program Files (x86)\Audio Precision\APx500 4.4\API\Python") # Set the path to import the Apx python sampleProject

import clr 											# Import the Common Language Runtime
clr.AddReference("System.Drawing") 					# Needed for Dialog Boxes
clr.AddReference("System.Windows.Forms") 			# Needed for Dialog Boxes
clr.AddReference("C:\Program Files (x86)\Audio Precision\APx500 4.4\API\AudioPrecision.API2.dll")   #the path changed from APx500 4.3 to APx500 4.4
clr.AddReference("C:\Program Files (x86)\Audio Precision\APx500 4.4\API\AudioPrecision.API.dll")

from AudioPrecision.API import * # Import the APx API



################################################################
## some examples:

### running an APx project:
# filename = 'Electrical_Test_Setup_APX_100mV_0dB.approjx'
# directory = "T:\Barkristal\DBMD6\DBMD6_electrical_functionality_tests\Tools"
# fullpath = os.path.join(directory, filename1)
# APx = APx500_Application(APxOperatingMode.BenchMode, True)
# APx.Visible= True
# APx.OpenProject(fullpath)


### configure to BenchMode:
# APx.BenchMode.Setup.OutputConnector.Type = OutputConnectorType.AnalogUnbalanced
# APx.BenchMode.Generator.Levels.SetValue(OutputChannelIndex.Ch1, 0.02)
# APx.BenchMode.Generator.Frequency.Value = 1234
# APx.BenchMode.Generator.On = True
# fft = APx.BenchMode.Measurements.Fft
# fft.Show()
# fft.Start()
# time.sleep(1)
# xValues = fft.FFTSpectrum.GetXValues(InputChannelIndex.Ch1, VerticalAxis.Left)
# yValues = fft.FFTSpectrum.GetYValues(InputChannelIndex.Ch1)
# for i in xValues:
#     print i