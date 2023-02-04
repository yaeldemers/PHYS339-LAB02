# Import seaborn
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

import serial
import time as t

# Apply the default theme
sns.set_theme()

# Repeating the experiment 10 times to get standard deviations
my_results = np.zeros((10, 500))

for i in range(10):
    value=255
    arraySize=500
    serialPort=serial.Serial()
    serialPort.baudrate=9600
    serialPort.port="COM5"
    serialPort.open()
    dataRead=False
    data=[]
    while (dataRead==False):
        serialPort.write(bytes([value]))
        t.sleep(0.1)
        inByte = serialPort.in_waiting
        #This loop reads in data from the array until byteCount reaches the array size (arraySize)
        byteCount=0
        while ((inByte>0)&(byteCount<arraySize)):
            dataByte=serialPort.read()
            byteCount=byteCount+1
            data=data+[dataByte]
        if (byteCount==arraySize):
            dataRead=True
    serialPort.close()
    dataOut=np.zeros(arraySize)
    arrayIndex=range(arraySize)
    
    #Transform unicode encoding into integers
    for j in arrayIndex:
        dataOut[j]=ord(data[j])
        
    my_results[i]=dataOut

my_stds=np.std(my_results, axis=0)

# Main experiment, we compare this to the previous 10s above
value=255
arraySize=500
serialPort=serial.Serial()
serialPort.baudrate=9600
serialPort.port="COM5"
print(serialPort)
serialPort.open()
dataRead=False
data=[]
while (dataRead==False):
    serialPort.write(bytes([value]))
    t.sleep(0.1)
    inByte = serialPort.in_waiting
    #This loop reads in data from the array until byteCount reaches the array size (arraySize)
    byteCount=0
    while ((inByte>0)&(byteCount<arraySize)):

        dataByte=serialPort.read()
        byteCount=byteCount+1
        data=data+[dataByte]
    if (byteCount==arraySize):
        dataRead=True
serialPort.close()
dataOut=np.zeros(arraySize)
arrayIndex=range(arraySize)

#Transform unicode encoding into integers
for i in arrayIndex:
    dataOut[i]=ord(data[i])
   
number_sent = np.linspace(0, 499,500)

# Exponential function showed in class, will fit and try to find b
def func(x, a, b):
   return  255 - 255*np.exp((-x+a)/b)

#popt, pcov = curve_fit(func, number_sent, dataOut) 

#perr = np.sqrt(np.diag(pcov)) #[0.00857345, 0.00934958]
# Again, manually story things to continue when no arduino setup available
popt = [-1.16429068, 2.57388384]
perr = [0.00857345, 0.00934958] 

# Saving data manually to work on this without the arduino setup
manual_data = np.array([91,146,182,206,221,231,238,243,246,248,250,251,251,252,252,253,253,253,253,253,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,255,255,254,254,255,255,254,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255])
full_span = np.linspace(0, 74, 75)

expected_out=np.zeros(75)
low_bound=np.zeros(75)
high_bound=np.zeros(75)

# Generating data and lower/upper error bounds
for i in range(75):
    expected_out[i]=func(full_span[i], popt[0], popt[1])
    low_bound[i]=func(full_span[i], popt[0]-250*perr[0], popt[1]-250*perr[1])
    high_bound[i]=func(full_span[i], popt[0]+250*perr[0], popt[1]+250*perr[1])

# Plotting the curve, scatter plot and error
plt.plot(full_span, expected_out, linewidth=1, color='black')
plt.scatter(full_span, manual_data, s=15)
plt.fill_between(full_span, low_bound, high_bound, alpha=1/3)
plt.ylim(0, 275)
plt.xlabel("array index")
plt.ylabel("8-bit rounded voltage reading")