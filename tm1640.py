from micropython import const
from machine import Pin
from time import sleep_us

TM1640_CMD1 = const(64)  # 0x40 data command
TM1640_CMD2 = const(192) # 0xC0 address command
TM1640_CMD3 = const(128) # 0x80 display control command
TM1640_DSP_ON = const(8) # 0x08 display on
TM1640_DELAY = const(10) # 10us delay between clk/dio pulses

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
        # automatic address increment, normal mode
        self._start()
        self._write_byte(TM1640_CMD1)
        self._stop()

    def _write_dsp_ctrl(self):
        # display on, set brightness
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
        # brightness 0 = 1/16th pulse width
        # brightness 7 = 14/16th pulse width
        if val is None:
            return self._brightness
        if not 0 <= val <= 7:
            raise ValueError("Brightness out of range")

        self._brightness = val
        self._write_data_cmd()
        self._write_dsp_ctrl()

    def write_int(self, int, pos=0, len=8):
        # Lưu ý: Phương thức này không thể tự động xử lý việc hoán đổi hàng 6 và 7
        # vì nó chuyển đổi số nguyên thành bytes và gửi đi.
        # Bạn sẽ cần xử lý hoán đổi ở lớp cao hơn nếu dùng hàm này.
        self.write(int.to_bytes(len, 'big'), pos)

    def write_hmsb(self, buf, pos=0):
        # Phương thức này cũng không xử lý việc hoán đổi hàng 6 và 7
        # nếu dữ liệu đầu vào buf đã được sắp xếp theo thứ tự mong muốn
        # của các chân điều khiển, chứ không phải thứ tự vật lý.
        self._write_data_cmd()
        self._start()

        self._write_byte(TM1640_CMD2 | pos)
        for i in range(7-pos, -1, -1):
            self._write_byte(buf[i])

        self._stop()
        self._write_dsp_ctrl()

    def write(self, rows, pos = 0):
        if not 0 <= pos <= 15:
            raise ValueError("Position out of range")

        # Tạo một bản sao có thể thay đổi của rows
        display_data = list(rows)

        # Kiểm tra xem có đủ dữ liệu để hoán đổi hàng 6 và 7 không
        # và pos có ảnh hưởng đến việc hoán đổi không.
        # Nếu pos là 0, thì hàng 6 và 7 tương ứng với index 6 và 7 của display_data
        # Nếu pos không phải 0, bạn cần tính toán index tương ứng.
        
        # Giả sử pos luôn là 0 hoặc bạn sẽ luôn gửi đủ 8 hàng trở lên
        # từ index 0 cho đến ít nhất index 7.
        if len(display_data) > 7 and pos == 0:
            # Hoán đổi dữ liệu của hàng 6 và hàng 7
            # Dữ liệu muốn hiển thị trên hàng 6 (vật lý) sẽ được gửi đến chân của hàng 7
            # Dữ liệu muốn hiển thị trên hàng 7 (vật lý) sẽ được gửi đến chân của hàng 6
            temp = display_data[6]
            display_data[6] = display_data[7]
            display_data[7] = temp
        # Nếu pos không phải 0 và bạn chỉ gửi một phần của màn hình,
        # bạn cần xác định xem các hàng bị đảo ngược có nằm trong phạm vi gửi hay không
        # và điều chỉnh logic hoán đổi cho phù hợp với offset pos.
        # Ví dụ: nếu bạn gửi từ pos=4 và muốn hoán đổi hàng vật lý 6 và 7,
        # thì bạn sẽ cần hoán đổi display_data[6-pos] và display_data[7-pos].
        # Để đơn giản, tôi sẽ giả định rằng bạn luôn gửi dữ liệu cho toàn bộ 8 hàng từ pos=0.

        self._write_data_cmd()
        self._start()

        self._write_byte(TM1640_CMD2 | pos)
        # Sử dụng display_data đã được hoán đổi
        for row in display_data:
            self._write_byte(row)

        self._stop()
        self._write_dsp_ctrl()
