const LEDMATRIX16x8ColorBlock = "#5d2c91";

var digitalPins = [
  [
    "D3",
    "D3"
  ],
  [
    "D4",
    "D4"
  ],
  [
    "D5",
    "D5"
  ],
  [
    "D6",
    "D6"
  ],
  [
    "D7",
    "D7"
  ],
  [
    "D8",
    "D8"
  ],
  [
    "D9",
    "D9"
  ],
  [
    "D10",
    "D10"
  ],
  [
    "D11",
    "D11"
  ],
  [
    "D12",
    "D12"
  ],
  [
    "D13",
    "D13"
  ],
  [
    "D0",
    "D0"
  ],
  [
    "D1",
    "D1"
  ],
  [
    "D2",
    "D2"
  ]
];

Blockly.Blocks["uno_led_matrix_create"] = {
  /**
   * Block for waiting.
   * @this Blockly.Block
   */
  init: function () {
    this.jsonInit({
      type: "uno_led_matrix_create",
      message0: "khởi tạo module led matrix chân DIO %1 chân CLK %2",
      args0: [
        {
          type: "field_dropdown",
          name: "DATA",
          options: digitalPins
        },
        {
          type: "field_dropdown",
          name: "CLK",
          options: digitalPins
        },
      ],
      previousStatement: null,
      nextStatement: null,
      colour: LEDMATRIX16x8ColorBlock,
      tooltip: "",
      helpUrl: "",
    });
  },
  getDeveloperVars: function () {
    return ["led_matrix"];
  },
};

Blockly.Blocks["uno_led_matrix_show_adv_image"] = {
  init: function () {
    this.jsonInit({
      colour: LEDMATRIX16x8ColorBlock,
      nextStatement: null,
      tooltip: 'Click vào để thay đổi hình ảnh',
      message0: 'led matrix hiện hình ảnh %1',
      previousStatement: null,
      args0: [
        {
          type: "field_matrix_image",
          name: "matrix_image",
          src: [0, 0, 0, 0, 60, 66, 149, 161, 161, 149, 66, 60, 0, 0, 0, 0],
          width: 50,
          height: 25,
          cols: 16,
          rows: 8,
          alt: "*",
        },
      ],
      helpUrl: ''
    });
  },
};

Blockly.Blocks["uno_led_matrix_show_image"] = {
  init: function () {
    this.jsonInit({
      colour: LEDMATRIX16x8ColorBlock,
      nextStatement: null,
      tooltip: '',
      message0: 'led matrix hiện hình ảnh %1 %2',
      previousStatement: null,
      args0: [
        { type: "input_value", name: "image", check: "yolobit_image" },
        { type: "input_dummy" }
      ],
      helpUrl: '',
    });
  }
};

Blockly.Blocks["uno_led_matrix_display"] = {
  init: function () {
    this.jsonInit({
      colour: LEDMATRIX16x8ColorBlock,
      nextStatement: null,
      tooltip: '',
      message0: 'led matrix hiện giá trị %1 %2',
      previousStatement: null,
      args0: [
        { type: "input_value", name: "value" },
        { type: "input_dummy" },
      ],
      helpUrl: ''
    });
  },
  getDeveloperVars: function () {
    return ["led_matrix"];
  },
};

// Khối mới: uno_led_matrix_scan
Blockly.Blocks["uno_led_matrix_scan"] = {

  init: function () {

    this.jsonInit({

      type: "uno_led_matrix_scan",

      message0: "led matrix quét LED với độ trễ %1 ms",

      args0: [

        {

          type: "field_number",

          name: "DELAY",

          value: 50, // Giá trị mặc định cho độ trễ

          min: 1,

          precision: 1,

        },

      ],

      previousStatement: null,

      nextStatement: null,

      colour: LEDMATRIX16x8ColorBlock,

      tooltip: "Bật từng đèn LED một trên ma trận.",

      helpUrl: "",

    });

  },

  getDeveloperVars: function () {

    return ["led_matrix"];

  },

};
Blockly.Blocks["uno_led_matrix_blink_image"] = {
  /**
   * Khối để nhấp nháy hình ảnh.
   * @this Blockly.Block
   */
  init: function () {
    this.jsonInit({
      type: "uno_led_matrix_blink_image",
      message0: "led matrix nhấp nháy hình ảnh %1 trong %2 ms, lặp lại %3 lần",
      args0: [
        {
          type: "field_matrix_image",
          name: "matrix_image",
          src: [0, 0, 0, 0, 60, 66, 149, 161, 161, 149, 66, 60, 0, 0, 0, 0], // Giá trị mặc định hoặc hình ảnh mẫu
          width: 50,
          height: 25,
          cols: 16,
          rows: 8,
          alt: "*",
        },
        {
          type: "field_number",
          name: "DELAY",
          value: 100, // Giá trị mặc định cho độ trễ nhấp nháy
          min: 1,
          precision: 1,
        },
        {
          type: "field_number",
          name: "TIMES",
          value: 3, // Giá trị mặc định cho số lần lặp lại
          min: 1,
          precision: 1,
        },
      ],
      previousStatement: null,
      nextStatement: null,
      colour: LEDMATRIX16x8ColorBlock,
      tooltip: "Nhấp nháy một hình ảnh trên ma trận LED.",
      helpUrl: "",
    });
  },
  getDeveloperVars: function () {
    return ["led_matrix"];
  },
};
// Khối mới: uno_led_matrix_test_led
Blockly.Blocks["uno_led_matrix_test_led"] = {
  init: function () {
    this.jsonInit({
      type: "uno_led_matrix_test_led",
      message0: "led matrix bật LED tại hàng %1 cột %2 trong %3 ms",
      args0: [
        {
          type: "field_number",
          name: "ROW",
          value: 0, // Giá trị mặc định
          min: 0,
          max: 7, // 8 hàng (0-7)
          precision: 1,
        },
        {
          type: "field_number",
          name: "COL",
          value: 0, // Giá trị mặc định
          min: 0,
          max: 15, // 16 cột (0-15)
          precision: 1,
        },
        {
          type: "field_number",
          name: "DURATION",
          value: 500, // Giá trị mặc định cho thời gian bật LED
          min: 1,
          precision: 1,
        },
      ],
      previousStatement: null,
      nextStatement: null,
      colour: LEDMATRIX16x8ColorBlock,
      tooltip: "Bật một đèn LED cụ thể tại vị trí hàng và cột được chỉ định.",
      helpUrl: "",
    });
  },
  getDeveloperVars: function () {
    return ["led_matrix"];
  },
};
Blockly.Python["uno_led_matrix_create"] = function (block) {
  var dropdown_clk = block.getFieldValue("CLK");
  var dropdown_data = block.getFieldValue("DATA");
  // TODO: Assemble Python into code variable.
  Blockly.Python.definitions_["import_tm1637"] = "from led_matrix import *";
  Blockly.Python.definitions_['init_tm1637'] = "led_matrix = LedMatrix(dio=" + dropdown_data + "_PIN, clk=" + dropdown_clk + "_PIN)";
  var code = '';
  return code;
};

Blockly.Python['uno_led_matrix_show_adv_image'] = function (block) {
  var matrix_image = block.getFieldValue('matrix_image');
  matrix_image = `[${matrix_image.toString()}]`;
  var code = 'led_matrix.show(' + matrix_image + ')\n';
  return code;
};

Blockly.Python['uno_led_matrix_show_image'] = function (block) {
  var value_image = Blockly.Python.valueToCode(block, 'image', Blockly.Python.ORDER_MEMBER);
  var code = 'led_matrix.show(' + value_image + ')\n';
  return code;
};

Blockly.Python['uno_led_matrix_display'] = function (block) {
  var value_text = Blockly.Python.valueToCode(block, 'value', Blockly.Python.ORDER_MEMBER);
  var code = 'led_matrix.show(' + value_text + ')\n';
  return code;
};

// Trình tạo Python mới cho khối uno_led_matrix_scan
Blockly.Python['uno_led_matrix_scan'] = function (block) {
  var delay = block.getFieldValue('DELAY');
  var code = 'led_matrix.scan_leds(' + delay + ')\n';
  return code;
};

// Trình tạo Python mới cho khối uno_led_matrix_test_led
Blockly.Python['uno_led_matrix_test_led'] = function (block) {
  var row = block.getFieldValue('ROW');
  var col = block.getFieldValue('COL');
  var duration = block.getFieldValue('DURATION');
  var code = 'led_matrix.test_individual_led(' + row + ', ' + col + ', ' + duration + ')\n';
  return code;
};

