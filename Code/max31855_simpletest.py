# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
max31855_simpletest

Modified by ProfHuster@gmail.com to work on Lolin S2Mini

2022-05-18

S2Mini board import has no SPI()
board.
    - SCK = board.IO7
    - MISO = board.IO9
    - MOSI = board.IO11 (don't need for MAX31855
I will use board.IO5 for CS.

From documentation on busio.SPI
class busio.SPI(
    clock: microcontroller.Pin, 
    MOSI: Optional[microcontroller.Pin] = None,
    MISO: Optional[microcontroller.Pin] = None,
    half_duplex: bool = False)
"""

import time
import board
import digitalio
import adafruit_max31855

if 'lolin_s2_mini' in board.board_id:
    import busio
    print("S2Mini")
    spi = busio.SPI(board.IO35, board.IO36, board.IO33)
else:
    print("Not S2Mini")
    spi = board.SPI()

cs = digitalio.DigitalInOut(board.IO37)

max31855 = adafruit_max31855.MAX31855(spi, cs)
while True:
    tempC = max31855.temperature
    tempF = tempC * 9 / 5 + 32
    print(f"Temperature: {tempC:.2f} C {tempF:.2f} F ")
    time.sleep(1.0)
