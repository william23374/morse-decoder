"""
工具函数模块
"""

from .audio import (
    load_wav_file,
    save_wav_file,
    normalize_audio,
    calculate_snr,
    detect_dominant_frequency,
    get_audio_info
)
from .morse import (
    MORSE_CODE_DICT,
    REVERSE_MORSE_DICT,
    text_to_morse,
    morse_to_text,
    validate_morse_code,
    get_morse_dict,
    get_reverse_morse_dict
)

__all__ = [
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
    'get_morse_dict',
    'get_reverse_morse_dict',
]
