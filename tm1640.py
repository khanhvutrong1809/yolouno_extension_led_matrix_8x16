from micropython import const
from machine import Pin
from time import sleep_us

TM1640_CMD1 = const(64)   # 0x40: data command
TM1640_CMD2 = const(192)  # 0xC0: address command
TM1640_CMD3 = const(128)  # 0x80: display control command
TM1640_DSP_ON = const(8)  # 0x08: display on
TM1640_DELAY = const(10)  # 10us delay

class TM1640(object):
    """Library for LED matrix display modules based on the TM1640 LED driver."""
    def __init__(self, clk, dio, brightness=7):
        self.clk = clk
        self.dio = dio

        if not 0 <= brightness <= 7:
            raise ValueError("Brightness out of range")
        self._brightness = brightness

        self.clk.init(Pin.OUT, value=0)
        self.dio.init(Pin.OUT, value=0)
        sleep_us(TM1640_DELAY)

        self._write_data_cmd()
        self._write_dsp_ctrl()

    def _start(self):
        self.dio(0)
        sleep_us(TM1640_DELAY)
        self.clk(0)
        sleep_us(TM1640_DELAY)

    def _stop(self):
        self.dio(0)
        sleep_us(TM1640_DELAY)
        self.clk(1)
        sleep_us(TM1640_DELAY)
        self.dio(1)

    def _write_data_cmd(self):
        self._start()
        self._write_byte(TM1640_CMD1)
        self._stop()

    def _write_dsp_ctrl(self):
        self._start()
        self._write_byte(TM1640_CMD3 | TM1640_DSP_ON | self._brightness)
        self._stop()

    def _write_byte(self, b):
        for i in range(8):
            self.dio((b >> i) & 1)
            sleep_us(TM1640_DELAY)
            self.clk(1)
            sleep_us(TM1640_DELAY)
            self.clk(0)
            sleep_us(TM1640_DELAY)

    def brightness(self, val=None):
        """Set the display brightness 0-7."""
        if val is None:
            return self._brightness
        if not 0 <= val <= 7:
            raise ValueError("Brightness out of range")

        self._brightness = val
        self._write_data_cmd()
        self._write_dsp_ctrl()

    def write_int(self, int, pos=0, len=8):
        self.write(int.to_bytes(len, 'big'), pos)

    def write_hmsb(self, buf, pos=0):
        self._write_data_cmd()
        self._start()

        self._write_byte(TM1640_CMD2 | pos)
        for i in range(7 - pos, -1, -1):
            self._write_byte(buf[i])

        self._stop()
        self._write_dsp_ctrl()

    def write(self, rows, pos=0):
        if not 0 <= pos <= 15:
            raise ValueError("Position out of range")

        # Hoán đổi cột 7 và 8 nếu đủ 8 byte
        data = list(rows)
        if len(data) >= 8:
            data[6], data[7] = data[7], data[6]

        self._write_data_cmd()
        self._start()

        self._write_byte(TM1640_CMD2 | pos)
        for row in data:
            self._write_byte(row)

        self._stop()
        self._write_dsp_ctrl()


    def clear(self):
        self.buffer = bytearray(16)
        self.show()

    def show(self):
        self._write_data_cmd()
        self._start()
        self._write_byte(TM1640_CMD2 | 0x00)
        for b in self.buffer:
            self._write_byte(b)
        self._stop()
        self._write_dsp_ctrl()

    def set_pixel(self, x, y, val):
        if not (0 <= x < 16 and 0 <= y < 8):
            return
        if val:
            self.buffer[x] |= (1 << y)
        else:
            self.buffer[x] &= ~(1 << y)

    def draw_bitmap(self, data):
        for i in range(min(16, len(data))):
            self.buffer[i] = data[i]
        self.show()

    def scroll_left(self):
        for i in range(15):
            self.buffer[i] = self.buffer[i + 1]
        self.buffer[15] = 0
        self.show()

    def scroll_right(self):
        for i in range(15, 0, -1):
            self.buffer[i] = self.buffer[i - 1]
        self.buffer[0] = 0
        self.show()

    def draw_char(self, char, font, pos=0):
        if char not in font:
            return
        data = font[char]
        for i in range(min(8, len(data))):
            if pos + i < 16:
                self.buffer[pos + i] = data[i]
        self.show()
