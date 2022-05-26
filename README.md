# Conductivity *versus* Temperature using CircuitPython on a Microcontroller
# Introduction

The ESP32-S2 microcontoller has a true DAC (Digital to Analog
Converter.) This feature is relatively rare in microcontollers but it
enables some unique experiments. In this project you will use the DAC to
control the voltage to a device, and two of the ADC's (Analog to
Digital Converters) to measure the resistance (inverse of the conductance) of a device. 
The microcontroller will measure both the current through and voltage
across the device as the voltage across it changes and fit the result to
a line to get the resistance. I also have a list in an appendix of other 
applications of this project.

To make the project more interesting you will also wire a Type K
thermocouple to a microcontroller breakout board using a digital
protocol. A type K thermocouples can read from -200 °C to 1350 °C. You can
use them to measure the temperature coefficient of the resistance and
the transition temperature of high Tc superconductors.
