"""
Morse Decoder Package
摩尔斯电码解码器包

提供多种摩尔斯电码解码器实现：
- V2: 高性能解码器，适合实时应用
- V3: 先进算法解码器，适合高噪声环境
"""

from .v2.decoder import MorseDecoder as MorseDecoderV2
from .v3.decoder import MorseDecoderV3
from .utils.audio import (
    load_wav_file,
    save_wav_file,
    normalize_audio,
    calculate_snr,
    detect_dominant_frequency,
    get_audio_info
)
from .utils.morse import (
    MORSE_CODE_DICT,
    REVERSE_MORSE_DICT,
    text_to_morse,
    morse_to_text,
    validate_morse_code
)

__version__ = '1.0.0'
__author__ = 'Morse Decoder Team'

# 导出主要类
__all__ = [
    # 解码器
    'MorseDecoderV2',
    'MorseDecoderV3',

    # 音频工具
    'load_wav_file',
    'save_wav_file',
    'normalize_audio',
    'calculate_snr',
    'detect_dominant_frequency',
    'get_audio_info',

    # 摩尔斯电码工具
    'MORSE_CODE_DICT',
    'REVERSE_MORSE_DICT',
    'text_to_morse',
    'morse_to_text',
    'validate_morse_code',

    # 元数据
    '__version__',
    '__author__',
]


# 为了向后兼容，提供别名
MorseDecoder = MorseDecoderV2  # 默认使用 V2
