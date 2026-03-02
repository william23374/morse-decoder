"""
摩尔斯电码字典和工具函数
"""

# 标准摩尔斯电码字典
MORSE_CODE_DICT = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z', '.----': '1', '..---': '2', '...--': '3',
    '....-': '4', '.....': '5', '-....': '6', '--...': '7',
    '---..': '8', '----.': '9', '-----': '0'
}

# 反向字典（字母到摩尔斯电码）
REVERSE_MORSE_DICT = {v: k for k, v in MORSE_CODE_DICT.items()}

# 标准呼号前缀（示例）
CALLSIGN_PREFIXES = {
    'BA': '中国',
    'BI': '中国',
    'CQ': '通用呼叫',
    'DE': '来自',
    'K': '邀请发送',
}


def text_to_morse(text: str) -> str:
    """
    将文本转换为摩尔斯电码

    参数:
        text: 要转换的文本

    返回:
        摩尔斯电码字符串
    """
    morse_list = []
    for char in text.upper():
        if char in REVERSE_MORSE_DICT:
            morse_list.append(REVERSE_MORSE_DICT[char])
        elif char == ' ':
            morse_list.append('/')
        else:
            morse_list.append('?')

    return ' '.join(morse_list)


def morse_to_text(morse: str) -> str:
    """
    将摩尔斯电码转换为文本

    参数:
        morse: 摩尔斯电码字符串（用空格分隔）

    返回:
        解码后的文本
    """
    # 分割为独立的摩尔斯电码
    codes = morse.split()

    text = []
    for code in codes:
        if code == '/':
            text.append(' ')
        elif code in MORSE_CODE_DICT:
            text.append(MORSE_CODE_DICT[code])
        else:
            text.append('?')

    return ''.join(text)


def validate_morse_code(morse: str) -> bool:
    """
    验证摩尔斯电码字符串是否有效

    参数:
        morse: 摩尔斯电码字符串

    返回:
        如果有效返回 True，否则返回 False
    """
    # 分割为独立的摩尔斯电码
    codes = morse.split()

    for code in codes:
        if code == '/':
            continue
        if code not in MORSE_CODE_DICT:
            return False

    return True


def get_morse_dict() -> dict:
    """
    获取摩尔斯电码字典

    返回:
        摩尔斯电码字典的副本
    """
    return MORSE_CODE_DICT.copy()


def get_reverse_morse_dict() -> dict:
    """
    获取反向摩尔斯电码字典

    返回:
        反向摩尔斯电码字典的副本
    """
    return REVERSE_MORSE_DICT.copy()
