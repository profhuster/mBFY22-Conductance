"""
testDAC.py
Sets the DAC and reads the ADC.

2022-04-28
ProfHuster@gmail.com
"""
import analogio
import board
from time import sleep
from math import sqrt

dacPin = board.IO17
dac = analogio.AnalogOut(dacPin)
adcPin = board.IO18
adc = analogio.AnalogIn(adcPin)
dToV = adc.reference_voltage / 0xffff
nAvg = 10
tADC = 0.01

print(f"# dacPin: {dacPin}, adcPin: {adcPin}, dToV: {dToV}")
print(f"# nAvg: {nAvg}, tADC: {tADC}")

def readADC():
    sum = 0.0
    sumSq = 0.0
    for i in range(nAvg):
        reading = adc.value * dToV
        sum += reading
        sumSq += reading * reading
        sleep(tADC)
        
    avg = sum / nAvg
    std = sqrt(sumSq / nAvg - avg * avg)
    return (avg, std)

for out in range(0, 0xffff, 0x1000):
    print(f"{out}, ", end="")
    dac.value = out
    sleep(0.1)
    (V, dV) = readADC()
    print(f"{V}, {dV}")

out = 0
print(f"{out}, ", end="")
dac.value = out
sleep(0.1)
(V, dV) = readADC()
print(f"{V}, {dV}")

dac.deinit()
adc.deinit()
# EOF