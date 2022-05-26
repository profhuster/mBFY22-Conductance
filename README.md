# Conductivity *versus* Temperature using CircuitPython on a Microcontroller
# Introduction

The ESP32-S2 is an amazing little microcontoller. It has built in WiFi 
a true DAC (Digital to Analog Converter), multiple ADC's (Analog to
Digital Converters), and DIO (Digital In Out) pins.
The DAC is relatively rare in microcontollers but it
enables some unique experiments. In this project you will use the DAC to
control the voltage to a device, and two of the ADC's 
to measure the resistance (inverse of the conductance) of a device. 
The microcontroller will measure both the current through and voltage
across the device as the voltage across it changes and fit the result to
a line to get the resistance. I also have a list in an appendix of other 
applications of this project.

To make the project more interesting you will also wire a Type K
thermocouple to a microcontroller breakout board using a digital
protocol. A type K thermocouples can read from -200 °C to 1350 °C. You can
use the thermocouple to measure the temperature coefficient of the resistance and
other experiments.

# Guide to Project Files
- [Main Guide to Project](https://github.com/profhuster/mBFY22-Conductance/blob/19ab132cf7104593252cab7fcc826aaca93124e6/Conductivity-CircuitPython_22d.pdf) You should download 
this document and keep it open as you work.
- [Setting Up CircuitPythonr](https://github.com/profhuster/mBFY22-Conductance/blob/bd73491f5e60a5675a0e9d870f6eabee54c16e31/Setting_Up_CircuitPython_22a.pdf) This is the guide to installing 
CircuitPython on a Microcontroller. You need to do this before working on the project.
