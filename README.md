# Morse Decoder

High-performance Morse code decoder supporting multiple decoding algorithms.

## Features

- **V2 Decoder**: High-performance decoder for real-time applications
  - Processing speed: 1000-1300x real-time
  - Accuracy: 100% (clear signals)
  - Lightweight implementation

- **V3 Decoder**: Advanced algorithm decoder for high-noise environments
  - 4th-order Butterworth IIR bandpass filter
  - Hilbert transform envelope detection
  - K-means clustering algorithm for intelligent classification
  - Automatic frequency tracking

- **Complete Toolset**:
  - Audio loading and saving
  - Audio normalization
  - SNR calculation
  - Frequency detection
  - Morse code conversion

## Installation

### Install from source

```bash
git clone https://github.com/william23374/morse-decoder.git
cd morse-decoder
pip install -e .
```

### Install using pip

```bash
pip install morse-decoder
```

### Dependencies

- Python >= 3.8
- numpy >= 1.20.0
- scipy >= 1.7.0
- scikit-learn >= 0.24.0
- sounddevice >= 0.4.5 (optional, for audio capture in CLI tool)

## Quick Start

### Python API

```python
from morse_decoder import MorseDecoderV2, load_wav_file

# Load audio file
audio_data, sample_rate = load_wav_file("audio.wav")

# Create decoder
decoder = MorseDecoderV2(sample_rate=sample_rate, frequency=550)

# Decode audio
result = decoder.decode(audio_data)
print(f"Decoded result: {result.text}")
```

For detailed usage instructions, see [Quick Start Guide](docs/QUICKSTART.md).

### Command Line Tool

```bash
# File decoding
morse-decode -i audio.wav -f 550

# Auto-detect frequency
morse-decode -i audio.wav --auto-detect

# Microphone recording
morse-decode --mic -d 5 -f 550

# Continuous monitoring
morse-decode --stream -f 550
```

For detailed command line usage instructions, see [CLI Guide](docs/CLI.md).

## Documentation

- **[Quick Start Guide](docs/QUICKSTART.md)**: Get started quickly
- **[CLI Guide](docs/CLI.md)**: Detailed command line tool instructions
- **[API Documentation](docs/API.md)**: Complete API reference

## Performance Comparison

| Decoder | Accuracy | Speed | Recommended Scenario |
|---------|----------|-------|---------------------|
| V2 | 100% | 1200x | Real-time applications |
| V3 | 100% | 400x | High-noise environments |

## Examples

See `examples/` directory for more examples:

- `basic_usage.py`: Basic usage examples
- `advanced_usage.py`: Advanced feature examples

Run examples:

```bash
cd examples
python basic_usage.py
python advanced_usage.py
```

## Testing

Run tests:

```bash
python -m pytest tests/
```

Or use unittest:

```bash
python -m unittest tests.test_all
```

## Project Structure

```
morse-decoder/
├── morse_decoder/          # Main package
│   ├── __init__.py
│   ├── v2/                # V2 decoder
│   │   ├── __init__.py
│   │   └── decoder.py
│   ├── v3/                # V3 decoder
│   │   ├── __init__.py
│   │   └── decoder.py
│   ├── utils/             # Utility functions
│   │   ├── __init__.py
│   │   ├── audio.py
│   │   └── morse.py
│   └── cli.py             # Command line tool
├── tests/                 # Tests
│   ├── __init__.py
│   └── test_all.py
├── examples/              # Examples
│   ├── basic_usage.py
│   └── advanced_usage.py
├── docs/                  # Documentation
│   ├── API.md
│   ├── CLI.md
│   └── QUICKSTART.md
├── setup.py               # Installation script
├── requirements.txt       # Dependencies
├── README.md              # This file
└── LICENSE                # MIT License
```

## API Overview

### MorseDecoderV2

High-performance Morse code decoder.

**Parameters**:
- `sample_rate` (int): Sample rate, default 8000Hz
- `target_freq` (float): Target frequency, default 550Hz
- `bandwidth` (float): Bandwidth, default 200Hz

**Methods**:
- `decode(samples)`: Decode audio samples

### MorseDecoderV3

Advanced algorithm Morse code decoder.

**Parameters**:
- `sample_rate` (int): Sample rate, default 8000Hz
- `target_freq` (float): Target frequency, default 550Hz
- `bandwidth` (float): Bandwidth, default 100Hz
- `enable_freq_tracking` (bool): Whether to enable frequency tracking, default True

**Methods**:
- `decode(samples)`: Decode audio samples

### Audio Utility Functions

- `load_wav_file(file_path)`: Load WAV file
- `save_wav_file(file_path, samples, sample_rate)`: Save WAV file
- `normalize_audio(samples)`: Normalize audio
- `calculate_snr(signal, noise)`: Calculate SNR
- `detect_dominant_frequency(samples, sample_rate)`: Detect dominant frequency
- `get_audio_info(file_path)`: Get audio file information

### Morse Code Utility Functions

- `text_to_morse(text)`: Text to Morse code
- `morse_to_text(morse)`: Morse code to text
- `validate_morse_code(morse)`: Validate Morse code

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to all contributors
- Inspired by Morse code decoders worldwide

## Contact

- Repository: https://github.com/william23374/morse-decoder
- Issues: https://github.com/william23374/morse-decoder/issues

## Changelog

### Version 1.0.0 (2026-03-02)

- Initial release
- V2 decoder implementation
- V3 decoder implementation
- Command line tool
- Complete documentation
- Comprehensive test suite
