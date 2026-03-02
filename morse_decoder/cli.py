"""
Morse Code Decoder Command Line Interface
Supports WAV file and real-time audio capture
"""

import argparse
import sys
import time
from pathlib import Path
from typing import Optional
import numpy as np


def decode_from_file(args):
    """Decode from WAV file"""
    from morse_decoder import (
        MorseDecoderV2,
        MorseDecoderV3,
        load_wav_file,
        get_audio_info,
        detect_dominant_frequency
    )

    print("=" * 70)
    print("Morse Code Decoder - File Mode")
    print("=" * 70)

    file_path = args.input

    # Check if file exists
    if not Path(file_path).exists():
        print(f"❌ Error: File not found: {file_path}")
        return 1

    print(f"\n📁 File: {file_path}")

    try:
        # Load audio
        sample_rate, audio = load_wav_file(file_path)
        duration = len(audio) / sample_rate

        print(f"🎵 Audio Info:")
        print(f"   Sample Rate: {sample_rate}Hz")
        print(f"   Duration: {duration:.2f}s")
        print(f"   Samples: {len(audio)}")

        # Detect dominant frequency
        if args.auto_detect:
            dominant_freq = detect_dominant_frequency(audio, sample_rate)
            target_freq = int(dominant_freq)
            print(f"   Detected Frequency: {dominant_freq:.1f}Hz")
        else:
            target_freq = args.frequency
            print(f"   Target Frequency: {target_freq}Hz")

        # Select decoder
        if args.decoder == 'v2':
            print(f"\n🔧 Using V2 Decoder")
            decoder = MorseDecoderV2(sample_rate=sample_rate, target_freq=target_freq)
        elif args.decoder == 'v3':
            print(f"\n🔧 Using V3 Decoder")
            decoder = MorseDecoderV3(
                sample_rate=sample_rate,
                target_freq=target_freq,
                bandwidth=args.bandwidth,
                enable_freq_tracking=args.freq_tracking
            )
        else:
            print(f"❌ Error: Unknown decoder type: {args.decoder}")
            return 1

        # Decode
        print(f"\n🔍 Starting decoding...")
        start_time = time.time()
        result = decoder.decode(audio)
        decode_time = (time.time() - start_time) * 1000

        # Output result
        print(f"\n{'='*70}")
        print(f"📝 Decoded Result:")
        print(f"{'='*70}")
        print(f"{result}")
        print(f"\n⏱️  Decode Time: {decode_time:.2f}ms")
        print(f"📊 Processing Speed: {duration/decode_time*1000:.1f}x real-time")

        # Statistics
        valid_chars = sum(1 for c in result if c.isalnum())
        print(f"\n📈 Statistics:")
        print(f"   Total Characters: {len(result)}")
        print(f"   Valid Characters: {valid_chars}")

        return 0

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


def decode_from_mic(args):
    """Decode from microphone in real-time"""
    try:
        import sounddevice as sd
    except ImportError:
        print("❌ Error: sounddevice library is required")
        print("   Please run: pip install sounddevice")
        return 1

    from morse_decoder import MorseDecoderV2, MorseDecoderV3

    print("=" * 70)
    print("Morse Code Decoder - Real-time Mode")
    print("=" * 70)

    # Parameters
    sample_rate = args.sample_rate
    duration = args.duration  # seconds
    channels = 1  # mono

    print(f"\n🎤 Audio Capture Settings:")
    print(f"   Sample Rate: {sample_rate}Hz")
    print(f"   Duration: {duration}s")
    print(f"   Frequency: {args.frequency}Hz")

    # Select decoder
    if args.decoder == 'v2':
        print(f"\n🔧 Using V2 Decoder")
        decoder = MorseDecoderV2(sample_rate=sample_rate, target_freq=args.frequency)
    elif args.decoder == 'v3':
        print(f"\n🔧 Using V3 Decoder")
        decoder = MorseDecoderV3(
            sample_rate=sample_rate,
            target_freq=args.frequency,
            bandwidth=args.bandwidth,
            enable_freq_tracking=args.freq_tracking
        )
    else:
        print(f"❌ Error: Unknown decoder type: {args.decoder}")
        return 1

    print(f"\n🎙️  Please play Morse code audio...")

    # Record audio
    try:
        print(f"⏳ Recording... (Press Ctrl+C to stop)")
        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=channels,
            dtype='float64'
        )
        sd.wait()  # Wait for recording to complete
    except KeyboardInterrupt:
        print(f"\n⚠️  Recording cancelled")
        return 0
    except Exception as e:
        print(f"\n❌ Recording failed: {e}")
        return 1

    # Convert to mono
    audio = recording.flatten()
    audio = audio.astype(np.float32)

    print(f"\n✅ Recording complete")

    # Decode
    print(f"\n🔍 Starting decoding...")
    start_time = time.time()
    result = decoder.decode(audio)
    decode_time = (time.time() - start_time) * 1000

    # Output result
    print(f"\n{'='*70}")
    print(f"📝 Decoded Result:")
    print(f"{'='*70}")
    print(f"{result}")
    print(f"\n⏱️  Decode Time: {decode_time:.2f}ms")

    return 0


def decode_from_stream(args):
    """Decode from audio stream in real-time (continuous mode)"""
    try:
        import sounddevice as sd
    except ImportError:
        print("❌ Error: sounddevice library is required")
        print("   Please run: pip install sounddevice")
        return 1

    from morse_decoder import MorseDecoderV2, MorseDecoderV3

    print("=" * 70)
    print("Morse Code Decoder - Stream Mode (Continuous Decoding)")
    print("=" * 70)

    # Parameters
    sample_rate = args.sample_rate
    block_size = int(args.block_size * sample_rate)  # block size
    channels = 1

    print(f"\n🎤 Audio Stream Settings:")
    print(f"   Sample Rate: {sample_rate}Hz")
    print(f"   Block Size: {args.block_size}s ({block_size} samples)")
    print(f"   Frequency: {args.frequency}Hz")
    print(f"\n🎙️  Listening to audio stream... (Press Ctrl+C to stop)")

    # Select decoder
    if args.decoder == 'v2':
        decoder = MorseDecoderV2(sample_rate=sample_rate, target_freq=args.frequency)
    elif args.decoder == 'v3':
        decoder = MorseDecoderV3(
            sample_rate=sample_rate,
            target_freq=args.frequency,
            bandwidth=args.bandwidth,
            enable_freq_tracking=args.freq_tracking
        )
    else:
        print(f"❌ Error: Unknown decoder type: {args.decoder}")
        return 1

    # Audio callback function
    audio_buffer = []
    last_decode_time = time.time()

    def audio_callback(indata, frames, time_info, status):
        nonlocal audio_buffer, last_decode_time

        if status:
            print(f"⚠️  Audio Status: {status}", file=sys.stderr)

        # Add to buffer
        audio_chunk = indata.flatten().astype(np.float32)
        audio_buffer.extend(audio_chunk)

        # Check if decoding is needed
        current_time = time.time()
        if len(audio_buffer) >= sample_rate * args.block_size:
            # Extract block
            samples = np.array(audio_buffer[:int(sample_rate * args.block_size)])
            audio_buffer = audio_buffer[int(sample_rate * args.block_size):]

            # Decode
            try:
                result = decoder.decode(samples)

                # If there is result, display it
                if result and len(result) > 0:
                    valid_chars = sum(1 for c in result if c.isalnum())
                    if valid_chars > 0:
                        timestamp = time.strftime("%H:%M:%S")
                        print(f"[{timestamp}] {result}")

                last_decode_time = current_time
            except Exception as e:
                print(f"❌ Decoding error: {e}", file=sys.stderr)

    try:
        # Create audio stream
        with sd.InputStream(
            samplerate=sample_rate,
            channels=channels,
            callback=audio_callback
        ):
            # Run continuously until user interrupts
            while True:
                time.sleep(0.1)

    except KeyboardInterrupt:
        print(f"\n\n⚠️  Stopped")
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Morse Code Decoder Command Line Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Decode from WAV file
  morse-decode -i audio.wav -f 550

  # Record from microphone and decode
  morse-decode --mic -d 5 -f 550

  # Continuously monitor audio stream
  morse-decode --stream -f 550

  # Use V3 decoder
  morse-decode -i audio.wav -f 550 --decoder v3
        """
    )

    # Input modes
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        '-i', '--input',
        type=str,
        help='Input WAV file path'
    )
    mode_group.add_argument(
        '--mic',
        action='store_true',
        help='Record from microphone'
    )
    mode_group.add_argument(
        '--stream',
        action='store_true',
        help='Continuously monitor audio stream'
    )

    # Decoder parameters
    parser.add_argument(
        '-f', '--frequency',
        type=float,
        default=550,
        help='Target frequency (Hz), default: 550'
    )
    parser.add_argument(
        '-b', '--bandwidth',
        type=float,
        default=100,
        help='Bandwidth (Hz), default: 100'
    )
    parser.add_argument(
        '--decoder',
        type=str,
        choices=['v2', 'v3'],
        default='v2',
        help='Decoder type (v2 or v3), default: v2'
    )

    # V3 specific parameters
    parser.add_argument(
        '--freq-tracking',
        action='store_true',
        help='Enable frequency tracking (V3 only)'
    )

    # Auto detect
    parser.add_argument(
        '--auto-detect',
        action='store_true',
        help='Auto-detect audio frequency'
    )

    # Microphone parameters
    parser.add_argument(
        '-d', '--duration',
        type=float,
        default=5.0,
        help='Recording duration (seconds), default: 5.0'
    )
    parser.add_argument(
        '--sample-rate',
        type=int,
        default=8000,
        help='Sample rate (Hz), default: 8000'
    )
    parser.add_argument(
        '--block-size',
        type=float,
        default=1.0,
        help='Stream mode block size (seconds), default: 1.0'
    )

    # Parse arguments
    args = parser.parse_args()

    # Execute based on mode
    if args.input:
        return decode_from_file(args)
    elif args.mic:
        return decode_from_mic(args)
    elif args.stream:
        return decode_from_stream(args)
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
