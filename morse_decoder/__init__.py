"""
Morse Decoder Package
Morse code decoder package

Provides multiple Morse code decoder implementations:
- V2: High-performance decoder for real-time applications
- V3: Advanced algorithm decoder for high-noise environments
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
__author__ = 'william23374'
__email__ = 'William23374@163.com'

# Export main classes
__all__ = [
    # Decoders
    'MorseDecoderV2',
    'MorseDecoderV3',

    # Audio utilities
    'load_wav_file',
    'save_wav_file',
    'normalize_audio',
    'calculate_snr',
    'detect_dominant_frequency',
    'get_audio_info',

    # Morse code utilities
    'MORSE_CODE_DICT',
    'REVERSE_MORSE_DICT',
    'text_to_morse',
    'morse_to_text',
    'validate_morse_code',

    # Metadata
    '__version__',
    '__author__',
    '__email__',
]


# For backward compatibility, provide alias
MorseDecoder = MorseDecoderV2  # Default to V2
