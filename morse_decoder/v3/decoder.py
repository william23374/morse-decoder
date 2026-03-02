"""
Morse Code Decoder v3 - Optimized Version
优化版摩斯电码解码器
改进：
- 使用真正的 IIR 带通滤波器
- 包络检波技术
- 自适应能量阈值
- 智能点和划识别
- 频率跟踪
"""

import numpy as np
from scipy import signal
from scipy.fft import fft, fftfreq
from typing import List, Tuple
import warnings
warnings.filterwarnings('ignore')


class MorseDecoderV3:
    """
    优化版摩斯电码解码器

    技术改进：
    - IIR 带通滤波器（Butterworth）
    - 包络检波（Hilbert 变换）
    - 自适应阈值检测
    - 统计学的点和划识别
    - 自动频率跟踪
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
        初始化解码器

        参数:
            sample_rate: 采样率 (Hz)
            target_freq: 目标频率 (Hz)
            bandwidth: 带宽 (Hz)
            enable_freq_tracking: 是否启用频率跟踪
        """
        self.sample_rate = sample_rate
        self.target_freq = target_freq
        self.bandwidth = bandwidth
        self.enable_freq_tracking = enable_freq_tracking

        # 滤波器参数
        self.low_freq = max(200, target_freq - bandwidth / 2)
        self.high_freq = min(2000, target_freq + bandwidth / 2)

        # 滤波器缓存
        self._filter_state = None
        self._filter_b = None
        self._filter_a = None

        # 设计滤波器
        self._design_filter()

        # 分析参数
        self.block_duration_ms = 5  # 更短的块，提高时间分辨率
        self.block_size = int(sample_rate * self.block_duration_ms / 1000)

    def _design_filter(self):
        """设计 IIR 带通滤波器 (Butterworth)"""
        nyquist = self.sample_rate / 2
        low = self.low_freq / nyquist
        high = self.high_freq / nyquist

        if low >= 1.0 or high <= 0.0 or low >= high:
            # 频率无效，使用全通
            self._filter_b = np.array([1.0])
            self._filter_a = np.array([1.0])
            return

        # 4阶 Butterworth 带通滤波器
        self._filter_b, self._filter_a = signal.butter(4, [low, high], btype='band')
        self._filter_state = None

    def _update_frequency(self, samples: np.ndarray) -> float:
        """检测并更新主导频率"""
        if not self.enable_freq_tracking:
            return self.target_freq

        # 使用 FFT 检测主导频率
        n = min(len(samples), 4096)  # 限制样本数提高速度
        yf = fft(samples[:n])
        xf = fftfreq(n, 1 / self.sample_rate)

        # 只考虑正频率
        positive_freqs = xf[:n // 2]
        power = np.abs(yf[:n // 2]) ** 2

        # 只考虑 200-1500Hz 范围
        mask = (positive_freqs >= 200) & (positive_freqs <= 1500)
        if not np.any(mask):
            return self.target_freq

        # 找出最大功率频率
        peak_idx = np.argmax(power * mask)
        detected_freq = positive_freqs[peak_idx]

        # 平滑频率更新 (低通滤波)
        alpha = 0.3  # 更新率
        new_freq = self.target_freq * (1 - alpha) + detected_freq * alpha

        # 限制在合理范围内
        new_freq = np.clip(new_freq, 300, 1200)

        # 如果频率变化太大，更新滤波器
        if abs(new_freq - self.target_freq) > self.bandwidth * 0.3:
            self.target_freq = new_freq
            self.low_freq = max(200, new_freq - self.bandwidth / 2)
            self.high_freq = min(2000, new_freq + self.bandwidth / 2)
            self._design_filter()

        return self.target_freq

    def _bandpass_filter(self, samples: np.ndarray) -> np.ndarray:
        """IIR 带通滤波"""
        if self._filter_state is None:
            filtered = signal.lfilter(self._filter_b, self._filter_a, samples)
        else:
            filtered, self._filter_state = signal.lfilter(self._filter_b, self._filter_a, samples, zi=self._filter_state)
        return filtered

    def _envelope_detection(self, samples: np.ndarray) -> np.ndarray:
        """包络检波 (使用 Hilbert 变换)"""
        analytic = signal.hilbert(samples)
        envelope = np.abs(analytic)

        # 平滑包络
        cutoff_freq = 20  # Hz
        nyquist = self.sample_rate / 2
        b, a = signal.butter(2, cutoff_freq / nyquist, btype='low')
        envelope = signal.filtfilt(b, a, envelope)

        return envelope

    def _detect_signal_segments(self, envelope: np.ndarray) -> List[Tuple[int, int, float]]:
        """
        检测信号段 - 使用自适应 Otsu 方法

        返回: [(start_idx, end_idx, duration_ms), ...]
        """
        # 归一化包络
        if envelope.max() > envelope.min():
            normalized = (envelope - envelope.min()) / (envelope.max() - envelope.min())
        else:
            normalized = envelope

        # 使用 Otsu 方法寻找最佳阈值
        # 简化版本：使用中位数 + 偏差
        median_val = np.median(normalized)
        std_val = np.std(normalized)

        # 阈值设置为中位数 + 标准差
        threshold = median_val + std_val * 0.3  # 降低系数

        # 确保阈值在合理范围内
        threshold = np.clip(threshold, 0.3, 0.7)

        # 检测信号
        is_signal = normalized > threshold

        # 轻微去抖动
        min_signal_blocks = 2  # 最小信号长度 (块数)

        # 只扩展信号，不扩展间隔
        is_signal = np.convolve(is_signal.astype(int), np.ones(min_signal_blocks), mode='same') > 0

        # 提取信号段
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

                # 最小长度过滤
                if duration_ms >= 8:  # 8ms
                    segments.append((start_idx, end_idx, duration_ms))

        if in_signal:
            duration_ms = (len(is_signal) - start_idx) * self.block_duration_ms
            if duration_ms >= 8:
                segments.append((start_idx, len(is_signal), duration_ms))

        return segments

    def _classify_dot_dash(self, durations: List[float]) -> Tuple[float, List[str]]:
        """
        使用聚类算法分类点和划

        返回: (dot_duration, ['. '-', '-', ...])
        """
        if not durations:
            return 50.0, []

        durations = np.array(durations)

        # 使用 K-means 聚分类分为两类 (点和划)
        from sklearn.cluster import KMeans

        # 标准化
        if len(durations) == 1:
            # 只有一个信号，假设是点
            return durations[0], ['.']

        # 尝试 K-means
        try:
            kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
            labels = kmeans.fit_predict(durations.reshape(-1, 1))
            centers = kmeans.cluster_centers_.flatten()

            # 确定哪个是点（较短的）
            if centers[0] < centers[1]:
                dot_label = 0
                dot_duration = centers[0]
            else:
                dot_label = 1
                dot_duration = centers[1]

            # 分类
            symbols = ['.'] if label == dot_label else ['-' for label in labels]

        except:
            # 回退到简单阈值
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
        解码音频

        参数:
            samples: 音频样本 (float32, 归一化到 [-1, 1])

        返回:
            解码后的文本
        """
        if len(samples) == 0:
            return ""

        # 更新频率跟踪
        self._update_frequency(samples)

        # 带通滤波
        filtered = self._bandpass_filter(samples)

        # 包络检波
        envelope = self._envelope_detection(filtered)

        # 重采样到块级别
        n_blocks = len(envelope) // self.block_size
        envelope_blocks = envelope[:n_blocks * self.block_size].reshape(-1, self.block_size)
        envelope_avg = np.mean(envelope_blocks, axis=1)

        # 检测信号段
        segments = self._detect_signal_segments(envelope_avg)

        if not segments:
            return ""

        # 提取时长和间隔
        durations = [seg[2] for seg in segments]
        gaps = []
        for i in range(len(segments) - 1):
            gap_duration = (segments[i + 1][0] - segments[i][1]) * self.block_duration_ms
            gaps.append(gap_duration)

        # 分类点和划
        dot_duration, symbols = self._classify_dot_dash(durations)

        # 添加间隔分隔符
        result_symbols = []
        for i, sym in enumerate(symbols):
            result_symbols.append(sym)

            # 检查是否是字符间隔
            if i < len(gaps):
                gap_ratio = gaps[i] / dot_duration
                if gap_ratio > 2.0:  # 字符间隔
                    result_symbols.append('/')
                elif gap_ratio > 4.0:  # 单词间隔
                    result_symbols.append(' ')

        # 转换为文本
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
            text.append(' ')  # 单词间隔

        return ''.join(text).strip()


def load_wav_file(file_path: str) -> Tuple[int, np.ndarray]:
    """
    加载 WAV 文件

    返回: (sample_rate, samples)
    """
    from scipy.io import wavfile
    sample_rate, audio = wavfile.read(file_path)

    # 转换为 float32
    if audio.dtype == np.int16:
        audio = audio.astype(np.float32) / 32768.0
    elif audio.dtype == np.int32:
        audio = audio.astype(np.float32) / 2147483648.0
    elif audio.dtype == np.int8:
        audio = audio.astype(np.float32) / 128.0
    elif audio.dtype == np.uint8:
        audio = (audio.astype(np.float32) - 128.0) / 128.0
    elif audio.dtype == np.float32:
        audio = audio.astype(np.float32)
    elif audio.dtype == np.float64:
        audio = audio.astype(np.float32)
    else:
        audio = audio.astype(np.float32)
        audio = audio / (np.max(np.abs(audio)) + 1e-10)

    # 立体声转单声道
    if len(audio.shape) > 1:
        audio = np.mean(audio, axis=1)

    # 清理 NaN/Inf
    audio = np.nan_to_num(audio, nan=0.0, posinf=1.0, neginf=-1.0)

    # 归一化
    max_val = np.max(np.abs(audio))
    if max_val > 1.0:
        audio = audio / max_val

    return sample_rate, audio


if __name__ == "__main__":
    import time

    print("="*70)
    print(" "*15 + "摩尔斯电码解码器 V3 - 优化版")
    print("="*70)

    # 测试文件
    test_files = [
        ("test_audio/BA4II-1.wav", 550),
        ("test_audio/BI1NZI.wav", 550),
        ("test_audio/B8.wav", 762),
    ]

    for file_path, target_freq in test_files:
        print(f"\n{'='*70}")
        print(f"📁 文件: {file_path}")
        print(f"{'='*70}")

        if not __import__('pathlib').Path(file_path).exists():
            print(f"⚠️  文件不存在")
            continue

        # 加载音频
        sample_rate, audio = load_wav_file(file_path)
        print(f"🎵 音频信息: {sample_rate}Hz, {len(audio)/sample_rate:.2f}秒")

        # 解码
        decoder = MorseDecoderV3(
            sample_rate=sample_rate,
            target_freq=target_freq,
            bandwidth=100,
            enable_freq_tracking=True
        )

        start_time = time.time()
        result = decoder.decode(audio)
        decode_time = (time.time() - start_time) * 1000

        print(f"🔍 解码结果: {result}")
        print(f"⏱️  解码时间: {decode_time:.2f}ms")
        print(f"📊 处理速度: {len(audio)/sample_rate/decode_time*1000:.1f}x 实时")

    print(f"\n{'='*70}")
    print("✅ 测试完成!")
    print(f"{'='*70}")
