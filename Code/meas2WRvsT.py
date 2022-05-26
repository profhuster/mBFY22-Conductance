"""
meas2WRvsT_22a.py
From meas2WResis_22b.py
From meas4WResis_22d1.py
Measures the resistance of a sample
- linear fit of data to get resistance
- Add thermocouple readout

ProfHuster@gmail.com
2022-05-24
"""
import analogio
import board
from time import sleep, monotonic
from math import sqrt
from array import array
# For thermocouple board
import digitalio
import busio
import adafruit_max31855
import microcontroller
import watchdog

print("# meas2WRvsT_22a.py")

debug = False

if "lolin" in board.board_id: 
    dacPin = board.IO18
    v0Pin = board.IO5
    v1Pin = board.IO7
    # 35 = Clock
    # 36 = MOSI (not used, don't wire)
    # 36 = MISO
    # 37 = CS but done later
    spi = busio.SPI(board.IO35, board.IO36, board.IO33)
    cs = digitalio.DigitalInOut(board.IO37)
else:
    raise "board error"

# Make a thermocouple reading object
max31855 = adafruit_max31855.MAX31855(spi, cs)

rSens = 100.0 # Resistance of sensing resistor
nAvg = 10 # number of readings to average
tADC = 0.001 # Time of DAC to settle
loopTime = 2 # Time between readings

# DAC control
countsMax = 0xffff
countsInc = 0x1000
nCounts = len(range(0, countsMax, countsInc))

# Initialize DAC and ADC
dac = analogio.AnalogOut(dacPin)
v0 = analogio.AnalogIn(v0Pin)
v1 = analogio.AnalogIn(v1Pin)
dToV = v0.reference_voltage / 0xffff

# Use watchdog to get a comment with a timeout
wdt = microcontroller.watchdog
wdt.timeout = 10
wdt.mode = watchdog.WatchDogMode.RAISE
try:
    comment = input("Enter comment: ")

except watchdog.WatchDogTimeout as e:
    comment = "No comment"
    
wdt.deinit()
print(f"# board_id = {board.board_id}")
print(f"# dacPin: {dacPin}, dToV: {dToV}")
print(f"# v0Pin: {v0Pin}, v1Pin: {v1Pin}")
print(f"# nAvg: {nAvg}, tADC: {tADC}, loopTime:{loopTime}")
print(f"# {comment}")

def readADC(adcX):
    sum = 0.0
    sumSq = 0.0
    for i in range(nAvg):
        reading = adcX.value * dToV
        sum += reading
        sumSq += reading * reading
        sleep(tADC)
        
    avg = sum / nAvg
    std = sumSq / nAvg - avg * avg
    if std <= 0.0:
        std = 0
    else:
        std = sqrt(sumSq / nAvg - avg * avg)
    return (avg, std)

first = True
# Make arrays for data
ISamp = array('f', nCounts * [0.0])
VSamp = array('f', nCounts * [0.0])
sigV = array('f', nCounts * [0.0])

def measureR():
    global first, ISamp, VSamp, sigV

    # Collect the data into arrays
    nGood = 0
    for (i, out) in enumerate(range(0, countsMax, countsInc)):
        dac.value = out
        sleep(tADC)
        (V0, dV0) = readADC(v0)
        if out > 4000 and V0 < 2.5: 
            (V1, dV1) = readADC(v1)
            ISamp[nGood] = (V0 - V1) / rSens
            VSamp[nGood] = V1
            sigV[nGood] = sqrt(dV0 * dV0 + dV1 * dV1)
            if sigV[nGood] == 0:
                sigV[nGood] = 0.001
            if debug:
                print(f"{out}, {ISamp[nGood]}, {VSamp[nGood]}, {sigV[nGood]}")
            nGood += 1
    
    # On first call print the number of data points
    if first:
        first = False
        print(f"# {nGood} good points")
        
    # Fit data to a line
    (a, resis, varA, varB, covAB) = linReg(nGood, ISamp, VSamp, sigV)
    uncResis = sqrt(varB)
    if debug:
        print(f"# Resistance = {resis:.2f}, {uncResis:.2f}")
        
    # Return resistance and uncertainty
    return (resis, uncResis)


# Do linear fit
def linReg(n, x, y, sigY):
    """linReg - linear fit with returned uncertainties."""
    invSigY2 = 0
    S = 0.0
    Sx = 0.0
    Sy = 0.0
    Sxx = 0.0
    Sxy = 0.0
    for i in range(n):
        invSigY2 = 1.0 / (sigY[i] * sigY[i])
        S += invSigY2
        Sx += x[i] * invSigY2
        Sy += y[i] * invSigY2
        Sxx += x[i] * x[i] * invSigY2
        Sxy += x[i] * y[i] * invSigY2

    Delta = S * Sxx - Sx * Sx
    a = (Sxx * Sy - Sx * Sxy) / Delta
    b = (S * Sxy - Sx * Sy) / Delta
    varA = Sxx / Delta
    varB = S / Delta
    covAB = -Sx / Delta
    return (a, b, varA, varB, covAB)

# Loop forever taking data
# Stop with ^C
t0 = monotonic()
try:
    while True:
        while monotonic() < t0 + loopTime:
            sleep(0.01)
        t0 += loopTime
        (R, sigR) = measureR()
        print(f"{monotonic():.1f}, {R:.2f}, {sigR:.2f}, {max31855.temperature:.2f}")
finally:
    # Clean up
    print("# Cleaning up")
    dac.deinit()
    v0.deinit()
    v1.deinit()
# EOF
