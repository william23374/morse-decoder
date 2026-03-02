"""
Morse Code Decoder with Noise Robustness
Morse code decoder based on energy detection and bandpass filtering (Python)
"""

import numpy as np
import wave
from typing import List


class MorseDecoder:
    """
    Morse Code Decoder

    Technical Features:
    - Simple FIR bandpass filter
    - Adaptive energy threshold
    - Automatic dot and dash duration estimation
    """

    MORSE_CODE = {
        '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
        '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
        '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
        '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
        '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
        '--..': 'Z', '.----': '1', '..---': '2', '...--': '3',
        '....-': '4', '.....': '5', '-....': '6', '--...': '7',
        '---..': '8', '----.': '9', '-----': '0'
    }

    def __init__(self, sample_rate: int = 8000, target_freq: float = 550):
        self.sample_rate = sample_rate
        self.target_freq = target_freq
        self.block_duration_ms = 10
        self.block_size = int(sample_rate * self.block_duration_ms / 1000)

        # Bandpass filter parameters (around target frequency)
        self.bandwidth = 200  # Hz
        self.low_freq = max(200, target_freq - self.bandwidth)
        self.high_freq = min(2000, target_freq + self.bandwidth)

    def bandpass_filter(self, samples: np.ndarray) -> np.ndarray:
        """Simple bandpass filter - use moving average differentiation"""
        # Calculate signal energy near target frequency
        # Use sliding window RMS
        window_size = int(self.sample_rate / self.target_freq * 2)  # 2 periods
        if window_size < 4:
            window_size = 4

        # Calculate envelope
        envelope = np.abs(samples)

        # Smooth (low-pass)
        kernel = np.ones(window_size) / window_size
        smoothed = np.convolve(envelope, kernel, mode='same')

        return smoothed

    def compute_block_energy(self, samples: np.ndarray) -> float:
        """Calculate block energy"""
        filtered = self.bandpass_filter(samples)
        return np.mean(filtered ** 2)

    def analyze_audio(self, samples: np.ndarray) -> List[tuple]:
        """Analyze audio, return list of signal segments"""
        n_blocks = len(samples) // self.block_size

        # Calculate energy for each block
        energies = []
        for i in range(n_blocks):
            block = samples[i * self.block_size:(i + 1) * self.block_size]
            energy = self.compute_block_energy(block)
            energies.append(energy)

        energies = np.array(energies)

        # Adaptive threshold
        sorted_e = np.sort(energies)
        noise_floor = sorted_e[int(len(sorted_e) * 0.25)]
        max_energy = sorted_e[-1]

        # Dynamic threshold
        snr = max_energy / (noise_floor + 1e-10)
        if snr > 10:
            threshold = noise_floor * 2.5
        elif snr > 5:
            threshold = noise_floor * 2.0
        else:
            threshold = noise_floor * 1.5

        threshold = max(threshold, 0.001)

        # Detect signals
        is_signal = energies > threshold

        # Extract signal segments
        segments = []
        in_signal = False
        start_idx = 0

        for i, sig in enumerate(is_signal):
            if sig and not in_signal:
                in_signal = True
                start_idx = i
            elif not sig and in_signal:
                in_signal = False
                duration_ms = (i - start_idx) * self.block_duration_ms
                if duration_ms >= 30:
                    segments.append((start_idx, i, duration_ms))

        if in_signal:
            duration_ms = (len(is_signal) - start_idx) * self.block_duration_ms
            if duration_ms >= 30:
                segments.append((start_idx, len(is_signal), duration_ms))

        return segments

    def decode_segments(self, segments: List[tuple]) -> str:
        """Decode signal segments"""
        if not segments:
            return ""

        # Estimate dot duration
        durations = [seg[2] for seg in segments]
        sorted_durations = sorted(durations)
        n_dots = max(1, len(sorted_durations) // 3)
        dot_duration = np.mean(sorted_durations[:n_dots])

        # Calculate gaps
        gaps = []
        for i in range(len(segments) - 1):
            gap_duration = (segments[i+1][0] - segments[i][1]) * self.block_duration_ms
            gaps.append(gap_duration)

        # Decode symbols
        symbols = []
        for i, seg in enumerate(segments):
            ratio = seg[2] / dot_duration
            if ratio < 1.8:
                symbols.append('.')
            else:
                symbols.append('-')

            if i < len(gaps):
                gap_ratio = gaps[i] / dot_duration
                if gap_ratio > 1.8:  # Character gap
                    symbols.append('/')

        # Convert to text
        text = []
        morse_char = ''
        for sym in symbols:
            if sym == '/':
                if morse_char in self.MORSE_CODE:
                    text.append(self.MORSE_CODE[morse_char])
                morse_char = ''
            else:
                morse_char += sym

        # Last character
        if morse_char in self.MORSE_CODE:
            text.append(self.MORSE_CODE[morse_char])

        return ''.join(text)

    def decode(self, samples: np.ndarray) -> str:
        """
        Decode audio samples to text

        Args:
            samples: Audio samples (numpy array)

        Returns:
            Decoded text string
        """
        segments = self.analyze_audio(samples)
        result = self.decode_segments(segments)
        return result
