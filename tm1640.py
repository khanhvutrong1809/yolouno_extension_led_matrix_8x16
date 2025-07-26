# tm1640_matrix.py
from micropython import const
from machine import Pin
from time import sleep_us

TM1640_CMD1 = const(0x40)  # Data command
TM1640_CMD2 = const(0xC0)  # Address command
TM1640_CMD3 = const(0x80)  # Display control command
TM1640_DSP_ON = const(0x08)
TM1640_DELAY = const(10)   # microseconds delay

class TM1640:
    def __init__(self, clk, dio, brightness=7):
        self.clk = clk
        self.dio = dio
        self.buffer = bytearray(16)  # 16 columns (8x16 matrix)

        if not 0 <= brightness <= 7:
            raise ValueError("Brightness out of range")
        self._brightness = brightness

        self.clk.init(Pin.OUT, value=0)
        self.dio.init(Pin.OUT, value=0)
        sleep_us(TM1640_DELAY)

        self._write_data_cmd()
        self._write_dsp_ctrl()

    def _start(self):
        self.dio(1)
        self.clk(1)
        sleep_us(TM1640_DELAY)
        self.dio(0)
        sleep_us(TM1640_DELAY)
        self.clk(0)
        sleep_us(TM1640_DELAY)

    def _stop(self):
        self.clk(0)
        sleep_us(TM1640_DELAY)
        self.dio(0)
        sleep_us(TM1640_DELAY)
        self.clk(1)
        sleep_us(TM1640_DELAY)
        self.dio(1)
        sleep_us(TM1640_DELAY)

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
        if val is None:
            return self._brightness
        if not 0 <= val <= 7:
            raise ValueError("Brightness out of range")
        self._brightness = val
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

    # Phương thức mới để xử lý việc hoán đổi hàng và cột
    def set_pixel(self, row, col, val):
        """
        Sets a pixel at the specified row and column.
        row: 0-7 (for 8 rows)
        col: 0-15 (for 16 columns)
        val: 0 for off, 1 for on
        """
        # Kiểm tra giới hạn
        if not (0 <= row < 8 and 0 <= col < 16):
            return

        # Khi chân bị hoán đổi, 'col' thực tế là chỉ mục byte trong buffer (cột)
        # và 'row' thực tế là bit trong byte đó (hàng).
        if val:
            self.buffer[col] |= (1 << row)
        else:
            self.buffer[col] &= ~(1 << row)

    def draw_bitmap(self, data):
        """
        Draws a 8x16 bitmap. `data` should be a 16-byte bytearray or list.
        Each byte in `data` represents a column, and each bit in the byte
        represents a row (LSB for row 0, MSB for row 7).
        """
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

    def draw_char(self, char_data, pos=0):
        """
        Draws an 8x8 character bitmap. `char_data` should be an 8-byte list/bytearray.
        `pos` is the starting column (0-15).
        """
        for i in range(min(8, len(char_data))):
            if pos + i < 16:
                self.buffer[pos + i] = char_data[i]
        self.show()
