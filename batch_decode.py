#!/usr/bin/env python3
"""
Batch Morse Code Decoder
Decode multiple audio files in batch
"""

import argparse
import sys
import json
from pathlib import Path

# Add the release package to path
sys.path.insert(0, '/workspace/projects/release')

from decode_audio import decode_audio


def batch_decode(input_pattern: str, decoder_type: str = 'v2',
                 frequency: int = None, output_file: str = None):
    """
    Decode multiple audio files

    Args:
        input_pattern: File pattern (e.g., "*.m4a", "audio/*.wav")
        decoder_type: 'v2' or 'v3'
        frequency: Target frequency (None for auto-detect)
        output_file: Output JSON file path (optional)
    """

    # Find files matching pattern
    if '*' in input_pattern or '?' in input_pattern:
        input_dir = Path(input_pattern).parent
        pattern = Path(input_pattern).name
        files = list(input_dir.glob(pattern))
    else:
        file_path = Path(input_pattern)
        files = [file_path] if file_path.exists() else []

    if not files:
        print(f"❌ No files found matching: {input_pattern}")
        return

    print(f"{'='*70}")
    print(f"Batch Morse Code Decoder")
    print(f"{'='*70}")
    print(f"\nFound {len(files)} file(s) to decode:\n")

    results = []

    for i, file_path in enumerate(files, 1):
        print(f"\n[{i}/{len(files)}] Processing: {file_path.name}")
        print("-" * 70)

        result = decode_audio(
            file_path=str(file_path),
            decoder_type=decoder_type,
            frequency=frequency,
            verbose=True
        )

        if result['success']:
            results.append({
                'file': str(file_path),
                'success': True,
                'text': result['text'],
                'cleaned_text': result['cleaned_text'],
                'callsigns': result['callsigns'],
                'decode_time': result['decode_time'],
                'processing_speed': result['processing_speed'],
                'valid_ratio': result['valid_chars'] / result['total_chars']
            })
            print(f"✅ Success")
        else:
            results.append({
                'file': str(file_path),
                'success': False,
                'error': 'Decoding failed'
            })
            print(f"❌ Failed")

    # Save results to JSON if output file specified
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n{'='*70}")
        print(f"✅ Results saved to: {output_file}")

    # Summary
    print(f"\n{'='*70}")
    print(f"📊 Batch Summary:")
    print(f"{'='*70}")
    success_count = sum(1 for r in results if r['success'])
    print(f"  Total files: {len(files)}")
    print(f"  Successful: {success_count}")
    print(f"  Failed: {len(files) - success_count}")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Batch Morse Code Decoder',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Decode all M4A files in current directory
  python batch_decode.py *.m4a

  # Decode all WAV files with specific frequency
  python batch_decode.py *.wav -f 550

  # Decode and save results to JSON
  python batch_decode.py *.m4a -o results.json

  # Use V3 decoder
  python batch_decode.py *.m4a --decoder v3
        """
    )

    parser.add_argument(
        'input_pattern',
        type=str,
        help='Input file pattern (e.g., "*.m4a", "audio/*.wav")'
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
        '-o', '--output',
        type=str,
        default=None,
        help='Output JSON file path'
    )

    args = parser.parse_args()

    # Batch decode
    batch_decode(
        input_pattern=args.input_pattern,
        decoder_type=args.decoder,
        frequency=args.frequency,
        output_file=args.output
    )


if __name__ == '__main__':
    main()
