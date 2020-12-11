# -*- coding: utf-8 -*-

IC2BUS = 1

ADDRESS = 0x27

import smbus
from time import sleep

class i2c_device:
    def __init__(self, addr, port=IC2BUS):
      self.addr = addr
      self.bus = smbus.SMBus(port)

    def write_cmd(self, cmd):
      self.bus.write_byte(self.addr, cmd)
      sleep(0.0001)

    def write_cmd_arg(self, cmd, data):
      self.bus.write_byte_data(self, addr, cmd, data)
      sleep(0.0001)

    def write_block_data(self, fmd, data):
      self.bus.write_block_data(self, addr, cmd, data)
      sleep(0.0001)

    def read(self):
      return self.bus.read_byte(self.addr)

    def read_data(self, cmd):
      return self.bus.read_bute_data(self.addr, cmd)

    def read_block_data(self, cmd):
      return self.bus.read_block_data(self.addr, cmd)

LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00

LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00

En = 0b00000100 # Enable bit
Rw = 0b00000010 # Read/Write bit
Rs = 0b00000001 # Register select bit

class lcd:
    def __init__(self):
      self.lcd_device = i2c_device(ADDRESS)

      self.lcd_write(0x03)
      self.lcd_write(0x03)
      self.lcd_write(0x03)
      self.lcd_write(0x02)

      self.lcd_write(LCD_FUNCTIONSET | LCD_2LINE | LCD_5x8DOTS | LCD_4BITMODE)
      self.lcd_write(LCD_DISPLAYCONTROL | LCD_DISPLAYON)
      self.lcd_write(LCD_CLEARDISPLAY)
      self.lcd_write(LCD_ENTRYMODESET | LCD_ENTRYLEFT)
      sleep(0.2)

    def lcd_strobe(self, data):
      self.lcd_device.write_cmd(data | En | LCD_BACKLIGHT)
      sleep(.0005)
      self.lcd_device.write_cmd(((data & ~En) | LCD_BACKLIGHT))
      sleep(.0001)

    def lcd_write_four_bits(self, data):
      self.lcd_device.write_cmd(data | LCD_BACKLIGHT)
      self.lcd_strobe(data)

    def lcd_write(self, cmd, mode=0):
      self.lcd_write_four_bits(mode | (cmd & 0xF0))
      self.lcd_write_four_bits(mode | ((cmd << 4) & 0xF0))

    def lcd_write_char(self, charvalue, mode=1):
      self.lcd_write_four_bits(mode | (charvalue & 0xF0))
      self.lcd_write_four_bits(mode | ((charvalue << 4) & 0xF0))

    def lcd_display_string(self, string, line=1, pos=0):
      if line == 1:
          pos_new = pos
      elif line == 2:
          pos_new = 0x40 + pos
      elif line == 3:
          pos_new = 0x14 + pos
      elif line == 4:
          pos_new = 0x54 + pos

      self.lcd_write(0x80 + pos_new)

      for char in string:
          self.lcd_write(ord(char), Rs)

    def lcd_clear(self):
      self.lcd_write(LCD_CLEARDISPLAY)
      self.lcd_write(LCD_RETURNHOME)

    def backlight(self, state):
      if state == 1:
          self.lcd_device.write_cmd(LCD_BACKLIGHT)
      elif state == 0:
          self.lcd_device.write_cmd(LCD_NOBACKLIGHT)

    def lcd_load_custom_chars(self, fontdata):
      self.lcd_write(0x40);
      for char in fontdata:
          for line in char:
              self.lcd_write_char(line)
