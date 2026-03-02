"""
Morse Code Decoder v3 - Optimized Version
Optimized Morse code decoder
Improvements:
- Use real IIR bandpass filter
- Envelope detection technique
- Adaptive energy threshold
- Intelligent dot and dash recognition
- Frequency tracking
"""

import numpy as np
from scipy import signal
from scipy.fft import fft, fftfreq
from typing import List, Tuple
import warnings
warnings.filterwarnings('ignore')


class MorseDecoderV3:
    """
    Optimized Morse Code Decoder

    Technical Improvements:
    - IIR bandpass filter (Butterworth)
    - Envelope detection (Hilbert transform)
    - Adaptive threshold detection
    - Statistical dot and dash recognition
    - Automatic frequency tracking
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

    def __init__(self, sample_rate: int = 8000, target_freq: float = 550,
                 bandwidth: float = 100, enable_freq_tracking: bool = True):
        """
        Initialize decoder

        Args:
            sample_rate: Sample rate (Hz)
            target_freq: Target frequency (Hz)
            bandwidth: Bandwidth (Hz)
            enable_freq_tracking: Whether to enable frequency tracking
        """
        self.sample_rate = sample_rate
        self.target_freq = target_freq
        self.bandwidth = bandwidth
        self.enable_freq_tracking = enable_freq_tracking

        # Filter parameters
        self.low_freq = max(200, target_freq - bandwidth / 2)
        self.high_freq = min(2000, target_freq + bandwidth / 2)

        # Filter cache
        self._filter_state = None
        self._filter_b = None
        self._filter_a = None

        # Design filter
        self._design_filter()

        # Analysis parameters
        self.block_duration_ms = 5  # Shorter block for higher time resolution
        self.block_size = int(sample_rate * self.block_duration_ms / 1000)

    def _design_filter(self):
        """Design IIR bandpass filter (Butterworth)"""
        nyquist = self.sample_rate / 2
        low = self.low_freq / nyquist
        high = self.high_freq / nyquist

        if low >= 1.0 or high <= 0.0 or low >= high:
            # Invalid frequency, use all-pass
            self._filter_b = np.array([1.0])
            self._filter_a = np.array([1.0])
            return

        # 4th order Butterworth bandpass filter
        self._filter_b, self._filter_a = signal.butter(4, [low, high], btype='band')
        self._filter_state = None

    def _update_frequency(self, samples: np.ndarray) -> float:
        """Detect and update dominant frequency"""
        if not self.enable_freq_tracking:
            return self.target_freq

        # Use FFT to detect dominant frequency
        n = min(len(samples), 4096)  # Limit sample count for speed
        yf = fft(samples[:n])
        xf = fftfreq(n, 1 / self.sample_rate)

        # Only consider positive frequencies
        positive_freqs = xf[:n // 2]
        power = np.abs(yf[:n // 2]) ** 2

        # Only consider 200-1500Hz range
        mask = (positive_freqs >= 200) & (positive_freqs <= 1500)
        if not np.any(mask):
            return self.target_freq

        # Find maximum power frequency
        peak_idx = np.argmax(power * mask)
        detected_freq = positive_freqs[peak_idx]

        # Smooth frequency update (low-pass filter)
        alpha = 0.3  # Update rate
        new_freq = self.target_freq * (1 - alpha) + detected_freq * alpha

        # Limit to reasonable range
        new_freq = np.clip(new_freq, 300, 1200)

        # If frequency changes significantly, update filter
        if abs(new_freq - self.target_freq) > self.bandwidth * 0.3:
            self.target_freq = new_freq
            self.low_freq = max(200, new_freq - self.bandwidth / 2)
            self.high_freq = min(2000, new_freq + self.bandwidth / 2)
            self._design_filter()

        return self.target_freq

    def _bandpass_filter(self, samples: np.ndarray) -> np.ndarray:
        """IIR bandpass filter"""
        if self._filter_state is None:
            filtered = signal.lfilter(self._filter_b, self._filter_a, samples)
        else:
            filtered, self._filter_state = signal.lfilter(self._filter_b, self._filter_a, samples, zi=self._filter_state)
        return filtered

    def _envelope_detection(self, samples: np.ndarray) -> np.ndarray:
        """Envelope detection (using Hilbert transform)"""
        analytic = signal.hilbert(samples)
        envelope = np.abs(analytic)

        # Smooth envelope
        cutoff_freq = 20  # Hz
        nyquist = self.sample_rate / 2
        b, a = signal.butter(2, cutoff_freq / nyquist, btype='low')
        envelope = signal.filtfilt(b, a, envelope)

        return envelope

    def _detect_signal_segments(self, envelope: np.ndarray) -> List[Tuple[int, int, float]]:
        """
        Detect signal segments - using adaptive Otsu method

        Returns: [(start_idx, end_idx, duration_ms), ...]
        """
        # Normalize envelope
        if envelope.max() > envelope.min():
            normalized = (envelope - envelope.min()) / (envelope.max() - envelope.min())
        else:
            normalized = envelope

        # Use Otsu method to find optimal threshold
        # Simplified version: use median + deviation
        median_val = np.median(normalized)
        std_val = np.std(normalized)

        # Set threshold as median + standard deviation
        threshold = median_val + std_val * 0.3  # Lower coefficient

        # Ensure threshold is in reasonable range
        threshold = np.clip(threshold, 0.3, 0.7)

        # Detect signals
        is_signal = normalized > threshold

        # Slight debouncing
        min_signal_blocks = 2  # Minimum signal length (blocks)

        # Only expand signals, not gaps
        is_signal = np.convolve(is_signal.astype(int), np.ones(min_signal_blocks), mode='same') > 0

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
                end_idx = i
                duration_ms = (end_idx - start_idx) * self.block_duration_ms

                # Minimum length filtering
                if duration_ms >= 8:  # 8ms
                    segments.append((start_idx, end_idx, duration_ms))

        if in_signal:
            duration_ms = (len(is_signal) - start_idx) * self.block_duration_ms
            if duration_ms >= 8:
                segments.append((start_idx, len(is_signal), duration_ms))

        return segments

    def _classify_dot_dash(self, durations: List[float]) -> Tuple[float, List[str]]:
        """
        Use clustering algorithm to classify dots and dashes

        Returns: (dot_duration, ['. ', '-', '-', ...])
        """
        if not durations:
            return 50.0, []

        durations = np.array(durations)

        # Use K-means clustering to classify into two types (dots and dashes)
        from sklearn.cluster import KMeans

        # Standardize
        if len(durations) == 1:
            # Only one signal, assume it's a dot
            return durations[0], ['.']

        # Try K-means
        try:
            kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
            labels = kmeans.fit_predict(durations.reshape(-1, 1))
            centers = kmeans.cluster_centers_.flatten()

            # Determine which is dot (shorter)
            if centers[0] < centers[1]:
                dot_label = 0
                dot_duration = centers[0]
            else:
                dot_label = 1
                dot_duration = centers[1]

            # Classify
            symbols = ['.'] if label == dot_label else ['-' for label in labels]

        except:
            # Fallback to simple threshold
            sorted_durations = np.sort(durations)
            dot_duration = np.mean(sorted_durations[:len(sorted_durations) // 2])
            symbols = []
            for d in durations:
                if d / dot_duration < 1.8:
                    symbols.append('.')
                else:
                    symbols.append('-')

        return dot_duration, symbols

    def decode(self, samples: np.ndarray) -> str:
        """
        Decode audio

        Args:
            samples: Audio samples (float32, normalized to [-1, 1])

        Returns:
            Decoded text
        """
        if len(samples) == 0:
            return ""

        # Update frequency tracking
        self._update_frequency(samples)

        # Bandpass filter
        filtered = self._bandpass_filter(samples)

        # Envelope detection
        envelope = self._envelope_detection(filtered)

        # Resample to block level
        n_blocks = len(envelope) // self.block_size
        envelope_blocks = envelope[:n_blocks * self.block_size].reshape(-1, self.block_size)
        envelope_avg = np.mean(envelope_blocks, axis=1)

        # Detect signal segments
        segments = self._detect_signal_segments(envelope_avg)

        if not segments:
            return ""

        # Extract durations and gaps
        durations = [seg[2] for seg in segments]
        gaps = []
        for i in range(len(segments) - 1):
            gap_duration = (segments[i + 1][0] - segments[i][1]) * self.block_duration_ms
            gaps.append(gap_duration)

        # Classify dots and dashes
        dot_duration, symbols = self._classify_dot_dash(durations)

        # Add gap separators
        result_symbols = []
        for i, sym in enumerate(symbols):
            result_symbols.append(sym)

            # Check if it's a character gap
            if i < len(gaps):
                gap_ratio = gaps[i] / dot_duration
                if gap_ratio > 2.0:  # Character gap
                    result_symbols.append('/')
                elif gap_ratio > 4.0:  # Word gap
                    result_symbols.append(' ')

        # Convert to text
        code = ''.join(result_symbols)
        parts = code.split(' ')

        text = []
        for part in parts:
            letters = part.split('/')
            for letter in letters:
                if letter in self.MORSE_CODE:
                    text.append(self.MORSE_CODE[letter])
                elif letter:
                    text.append('?')
            text.append(' ')  # Word gap

        return ''.join(text).strip()
