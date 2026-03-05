# Morse Code Decoder Usage Guide

## Quick Start

### Single File Decoding

```bash
# Auto-detect frequency (recommended)
python decode_audio.py audio.m4a

# Specify frequency
python decode_audio.py audio.m4a -f 550

# Use V3 decoder
python decode_audio.py audio.m4a --decoder v3

# Quiet mode (only output decoded text)
python decode_audio.py audio.m4a --quiet
```

### Batch Decoding

```bash
# Decode all M4A files in current directory
python batch_decode.py *.m4a

# Decode all WAV files with specific frequency
python batch_decode.py *.wav -f 550

# Decode and save results to JSON
python batch_decode.py *.m4a -o results.json

# Use V3 decoder
python batch_decode.py *.m4a --decoder v3
```

## Supported Audio Formats

- M4A
- WAV
- MP3
- OGG
- FLAC
- And more...

## Command-Line Options

### decode_audio.py

| Option | Description |
|--------|-------------|
| `input_file` | Input audio file path (required) |
| `--decoder {v2,v3}` | Decoder type (default: v2) |
| `-f, --frequency Hz` | Target frequency (default: auto-detect) |
| `-b, --bandwidth Hz` | Bandwidth for V3 decoder (default: 100) |
| `--no-auto-detect` | Disable auto frequency detection |
| `--quiet` | Quiet mode (only output decoded text) |

### batch_decode.py

| Option | Description |
|--------|-------------|
| `input_pattern` | File pattern (e.g., "*.m4a", "audio/*.wav") |
| `--decoder {v2,v3}` | Decoder type (default: v2) |
| `-f, --frequency Hz` | Target frequency (default: auto-detect) |
| `-o, --output FILE` | Output JSON file path |
| `--quiet` | Quiet mode |

## Examples

### Example 1: Decode YO3AAJ.m4a

```bash
python decode_audio.py YO3AAJ.m4a
```

Output:
```
======================================================================
Morse Code Decoder - Universal Audio Decoder
======================================================================

📁 File: YO3AAJ.m4a
🎵 Audio Info:
   Sample Rate: 8000Hz
   Duration: 112.75s
   Samples: 901963

🔍 Detecting dominant frequency...
   Detected Frequency: 201.2Hz

🔧 Using V2 Decoder at 201Hz
🔍 Starting decoding...

======================================================================
📝 Decoded Result:
======================================================================
ATETYTDEM3AAJYOALOMANIALOMANIAYO3AAJEO3AAJYO3AAJ...

⏱️  Decode Time: 94.43ms
📊 Processing Speed: 1194.0x real-time

📡 Detected Callsigns:
  EM3AAJ
  EO3AAJ
  TT9S
  YO3AAJ
```

### Example 2: Decode with specific frequency

```bash
python decode_audio.py audio.m4a -f 580
```

### Example 3: Batch decode multiple files

```bash
python batch_decode.py *.m4a -o results.json
```

### Example 4: Export to script for automation

```bash
# Make script executable
chmod +x decode_audio.py

# Run directly
./decode_audio.py audio.m4a
```

## Troubleshooting

### Error: "Required libraries not installed"

```bash
pip install librosa soundfile
```

### Error: "File not found"

Check the file path is correct and the file exists.

### Poor decoding results

1. Try specifying the correct frequency manually
2. Try the V3 decoder for noisy audio
3. Check if the audio quality is good
4. Verify the audio actually contains Morse code

### Frequency detection issues

If auto-detection gives wrong results:
1. Check the audio spectrum manually
2. Specify the frequency manually using `-f` option
3. Try different frequencies (550Hz, 600Hz, etc.)

## Integration with Other Tools

### Use in Python scripts

```python
from decode_audio import decode_audio

result = decode_audio(
    file_path='audio.m4a',
    decoder_type='v2',
    frequency=550,
    auto_detect=False,
    verbose=True
)

if result['success']:
    print(f"Decoded: {result['text']}")
    print(f"Callsigns: {result['callsigns']}")
```

### Use in shell scripts

```bash
#!/bin/bash

for file in *.m4a; do
    echo "Processing $file..."
    python decode_audio.py "$file" >> results.txt
    echo "---" >> results.txt
done
```

## Performance

- **Processing Speed**: 1000-1200x real-time (V2 decoder)
- **Decode Time**: ~100ms for 2-minute audio
- **Supported Formats**: M4A, WAV, MP3, OGG, FLAC, etc.

## Tips

1. **Always use auto-detect first** to find the correct frequency
2. **V2 decoder** is faster and works well for clear audio
3. **V3 decoder** is better for noisy audio but slower
4. **Batch processing** is useful for multiple files
5. **Export to JSON** for programmatic access to results

## Contact

For issues and questions:
- GitHub: https://github.com/william23374/morse-decoder
- Email: William23374@163.com
