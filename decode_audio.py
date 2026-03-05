#!/usr/bin/env python3
"""
Universal Morse Code Decoder
Supports multiple audio formats: M4A, WAV, MP3, OGG, FLAC, etc.
"""

import argparse
import sys
import time
import re
from pathlib import Path

try:
    import librosa
    import numpy as np
except ImportError:
    print("❌ Error: Required libraries not installed")
    print("   Please run: pip install librosa soundfile")
    sys.exit(1)

# Add the release package to path
sys.path.insert(0, '/workspace/projects/release')

from morse_decoder import (
    MorseDecoderV2,
    MorseDecoderV3,
    detect_dominant_frequency
)


def load_audio_file(file_path: str, target_sr: int = 8000) -> tuple:
    """
    Load audio file (supports M4A, WAV, MP3, OGG, FLAC, etc.)

    Args:
        file_path: Path to audio file
        target_sr: Target sample rate (default: 8000 Hz)

    Returns:
        (audio_samples, sample_rate)
    """
    if not Path(file_path).exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Load audio with librosa (supports multiple formats)
    audio, sr = librosa.load(file_path, sr=target_sr, mono=True)

    # Convert to float32
    audio = audio.astype(np.float32)

    # Normalize
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val

    return audio, sr


def clean_result(result: str) -> str:
    """Clean and format the decoded result"""
    # Add spaces after 5-6 consecutive letters to separate words
    cleaned = re.sub(r'([A-Z]{5,6})(?=[A-Z])', r'\1 ', result)
    # Add spaces before callsigns
    cleaned = re.sub(r'([A-Z]{1,2}[0-9][A-Z]{1,3})', r' \1 ', cleaned)
    # Clean up multiple spaces
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned.strip()


def format_with_char_spacing(result: str) -> str:
    """Format result with space between each character"""
    return ' '.join(result)


def analyze_callsigns(result: str) -> list:
    """Extract potential amateur radio callsigns"""
    # Pattern for callsigns: 1-2 letters, 1 digit, 1-3 letters (e.g., YO3AAJ, EM3AAJ)
    pattern = r'[A-Z]{1,2}[0-9][A-Z]{1,3}'
    callsigns = re.findall(pattern, result)
    unique_callsigns = sorted(set(callsigns))
    return unique_callsigns


def decode_audio(file_path: str, decoder_type: str = 'v2',
                 frequency: int = None, bandwidth: int = 100,
                 auto_detect: bool = True, verbose: bool = True,
                 char_spacing: bool = True) -> dict:
    """
    Decode audio file

    Args:
        file_path: Path to audio file
        decoder_type: 'v2' or 'v3'
        frequency: Target frequency (None for auto-detect)
        bandwidth: Bandwidth for decoder (Hz)
        auto_detect: Auto-detect frequency
        verbose: Print detailed output

    Returns:
        Dictionary with decoding results
    """

    result = {
        'success': False,
        'text': '',
        'cleaned_text': '',
        'callsigns': [],
        'decode_time': 0.0,
        'processing_speed': 0.0,
        'sample_rate': 0,
        'duration': 0.0,
        'frequency_used': 0,
        'valid_chars': 0,
        'total_chars': 0
    }

    try:
        if verbose:
            print("=" * 70)
            print("Morse Code Decoder - Universal Audio Decoder")
            print("=" * 70)
            print(f"\n📁 File: {file_path}")

        # Load audio
        audio, sample_rate = load_audio_file(file_path)
        duration = len(audio) / sample_rate

        result['sample_rate'] = sample_rate
        result['duration'] = duration

        if verbose:
            print(f"🎵 Audio Info:")
            print(f"   Sample Rate: {sample_rate}Hz")
            print(f"   Duration: {duration:.2f}s")
            print(f"   Samples: {len(audio)}")

        # Detect frequency if needed
        if auto_detect or frequency is None:
            if verbose:
                print(f"\n🔍 Detecting dominant frequency...")
            detected_freq = detect_dominant_frequency(audio, sample_rate)
            frequency = int(detected_freq)

            if verbose:
                print(f"   Detected Frequency: {detected_freq:.1f}Hz")

        result['frequency_used'] = frequency

        # Create decoder
        if decoder_type == 'v2':
            if verbose:
                print(f"\n🔧 Using V2 Decoder at {frequency}Hz")
            decoder = MorseDecoderV2(sample_rate=sample_rate, target_freq=frequency)
        elif decoder_type == 'v3':
            if verbose:
                print(f"\n🔧 Using V3 Decoder at {frequency}Hz (with frequency tracking)")
            decoder = MorseDecoderV3(
                sample_rate=sample_rate,
                target_freq=frequency,
                bandwidth=bandwidth,
                enable_freq_tracking=True
            )
        else:
            raise ValueError(f"Invalid decoder type: {decoder_type}")

        # Decode
        if verbose:
            print(f"🔍 Starting decoding...")

        start_time = time.time()
        decoded_text = decoder.decode(audio)
        decode_time = (time.time() - start_time) * 1000

        result['decode_time'] = decode_time
        result['processing_speed'] = duration / decode_time * 1000
        result['text'] = decoded_text
        result['total_chars'] = len(decoded_text)
        result['valid_chars'] = sum(1 for c in decoded_text if c.isalnum())

        # Clean result
        cleaned_text = clean_result(decoded_text)
        result['cleaned_text'] = cleaned_text

        # Extract callsigns
        callsigns = analyze_callsigns(decoded_text)
        result['callsigns'] = callsigns

        if verbose:
            print(f"\n{'='*70}")
            print(f"📝 Decoded Result:")
            print(f"{'='*70}")

            # Show result with character spacing
            if char_spacing:
                spaced_text = format_with_char_spacing(decoded_text)
                print(f"{spaced_text}")
            else:
                print(f"{decoded_text}")

            print(f"\n⏱️  Decode Time: {decode_time:.2f}ms")
            print(f"📊 Processing Speed: {result['processing_speed']:.1f}x real-time")

            print(f"\n{'='*70}")
            print(f"📝 Cleaned Result (with word spacing):")
            print(f"{'='*70}")
            print(f"{cleaned_text}")

            if callsigns:
                print(f"\n{'='*70}")
                print(f"📡 Detected Callsigns:")
                print(f"{'='*70}")
                for callsign in callsigns:
                    print(f"  {callsign}")

            print(f"\n{'='*70}")
            print(f"📈 Statistics:")
            print(f"{'='*70}")
            print(f"  Total Characters: {result['total_chars']}")
            print(f"  Valid Characters: {result['valid_chars']}")
            print(f"  Valid Ratio: {result['valid_chars']/result['total_chars']:.2%}")

        result['success'] = True

    except Exception as e:
        if verbose:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()

    return result


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Universal Morse Code Decoder',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Supported audio formats: M4A, WAV, MP3, OGG, FLAC, and more.

Examples:
  # Decode with auto frequency detection
  python decode_audio.py audio.m4a

  # Decode with specific frequency
  python decode_audio.py audio.m4a -f 550

  # Use V3 decoder
  python decode_audio.py audio.m4a --decoder v3

  # Quiet mode (only output decoded text)
  python decode_audio.py audio.m4a --quiet
        """
    )

    parser.add_argument(
        'input_file',
        type=str,
        help='Input audio file (M4A, WAV, MP3, etc.)'
    )

    parser.add_argument(
        '--decoder',
        type=str,
        choices=['v2', 'v3'],
        default='v2',
        help='Decoder type (default: v2)'
    )

    parser.add_argument(
        '-f', '--frequency',
        type=int,
        default=None,
        help='Target frequency (Hz, default: auto-detect)'
    )

    parser.add_argument(
        '-b', '--bandwidth',
        type=int,
        default=100,
        help='Bandwidth for V3 decoder (Hz, default: 100)'
    )

    parser.add_argument(
        '--no-auto-detect',
        action='store_true',
        help='Disable auto frequency detection'
    )

    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Quiet mode (only output decoded text)'
    )

    parser.add_argument(
        '--no-char-spacing',
        action='store_true',
        help='Disable character spacing in output'
    )

    args = parser.parse_args()

    # Decode audio
    result = decode_audio(
        file_path=args.input_file,
        decoder_type=args.decoder,
        frequency=args.frequency,
        bandwidth=args.bandwidth,
        auto_detect=not args.no_auto_detect,
        verbose=not args.quiet,
        char_spacing=not args.no_char_spacing
    )

    # Exit code
    sys.exit(0 if result['success'] else 1)


if __name__ == '__main__':
    main()
