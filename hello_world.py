import I2C_LCD_driver
from time import *

mylcd = I2C_LCD_driver.lcd()

mylcd.backlight(0)
mylcd.lcd_display_string("Hello World!", 1)
