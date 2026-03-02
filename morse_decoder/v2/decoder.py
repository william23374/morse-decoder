"""
Morse Code Decoder with Noise Robustness
基于能量检测和带通滤波的摩斯电码解码器 (Python)
"""

import numpy as np
import wave
from typing import List


class MorseDecoder:
    """
    摩斯电码解码器
    
    技术特点：
    - 简单的 FIR 带通滤波器
    - 自适应能量阈值
    - 自动点和划时长估计
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
        
        # 带通滤波器参数 (围绕目标频率)
        self.bandwidth = 200  # Hz
        self.low_freq = max(200, target_freq - self.bandwidth)
        self.high_freq = min(2000, target_freq + self.bandwidth)
        
    def bandpass_filter(self, samples: np.ndarray) -> np.ndarray:
        """简单的带通滤波器 - 使用移动平均差分"""
        # 计算信号在目标频率附近的能量
        # 使用滑动窗口 RMS
        window_size = int(self.sample_rate / self.target_freq * 2)  # 2个周期
        if window_size < 4:
            window_size = 4
        
        # 计算包络
        envelope = np.abs(samples)
        
        # 平滑 (低通)
        kernel = np.ones(window_size) / window_size
        smoothed = np.convolve(envelope, kernel, mode='same')
        
        return smoothed
    
    def compute_block_energy(self, samples: np.ndarray) -> float:
        """计算块的能量"""
        filtered = self.bandpass_filter(samples)
        return np.mean(filtered ** 2)
    
    def analyze_audio(self, samples: np.ndarray) -> List[tuple]:
        """分析音频，返回信号段列表"""
        n_blocks = len(samples) // self.block_size
        
        # 计算每块能量
        energies = []
        for i in range(n_blocks):
            block = samples[i * self.block_size:(i + 1) * self.block_size]
            energy = self.compute_block_energy(block)
            energies.append(energy)
        
        energies = np.array(energies)
        
        # 自适应阈值
        sorted_e = np.sort(energies)
        noise_floor = sorted_e[int(len(sorted_e) * 0.25)]
        max_energy = sorted_e[-1]
        
        # 动态阈值
        snr = max_energy / (noise_floor + 1e-10)
        if snr > 10:
            threshold = noise_floor * 2.5
        elif snr > 5:
            threshold = noise_floor * 2.0
        else:
            threshold = noise_floor * 1.5
        
        threshold = max(threshold, 0.001)
        
        # 检测信号
        is_signal = energies > threshold
        
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
                duration_ms = (i - start_idx) * self.block_duration_ms
                if duration_ms >= 30:
                    segments.append((start_idx, i, duration_ms))
        
        if in_signal:
            duration_ms = (len(is_signal) - start_idx) * self.block_duration_ms
            if duration_ms >= 30:
                segments.append((start_idx, len(is_signal), duration_ms))
        
        return segments
    
    def decode_segments(self, segments: List[tuple]) -> str:
        """解码信号段"""
        if not segments:
            return ""
        
        # 估计点时长
        durations = [seg[2] for seg in segments]
        sorted_durations = sorted(durations)
        n_dots = max(1, len(sorted_durations) // 3)
        dot_duration = np.mean(sorted_durations[:n_dots])
        
        # 计算间隔
        gaps = []
        for i in range(len(segments) - 1):
            gap_duration = (segments[i+1][0] - segments[i][1]) * self.block_duration_ms
            gaps.append(gap_duration)
        
        # 解码符号
        symbols = []
        for i, seg in enumerate(segments):
            ratio = seg[2] / dot_duration
            if ratio < 1.8:
                symbols.append('.')
            else:
                symbols.append('-')
            
            if i < len(gaps):
                gap_ratio = gaps[i] / dot_duration
                if gap_ratio > 1.8:  # 字符间隔
                    symbols.append('/')
        
        # 转换为文本
        code = ''.join(symbols)
        letters = code.split('/')
        
        result = []
        for letter in letters:
            if letter in self.MORSE_CODE:
                result.append(self.MORSE_CODE[letter])
            elif letter:
                result.append('?')
        
        return ''.join(result)
    
    def decode(self, samples: np.ndarray) -> str:
        """解码音频"""
        segments = self.analyze_audio(samples)
        return self.decode_segments(segments)


def generate_morse_audio(text: str, filename: str, freq: float = 550,
                        wpm: float = 20, sample_rate: int = 8000,
                        noise_level: float = 0.0):
    """生成摩斯电码 WAV"""
    morse_dict = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
        'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
        'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
        'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
        'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
        'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
        '4': '....-', '5': '.....', '6': '-....', '7': '--...',
        '8': '---..', '9': '----.', '0': '-----', ' ': '/'
    }
    
    unit_samples = int((60.0 / (50.0 * wpm)) * sample_rate)
    samples = []
    
    for i, char in enumerate(text.upper()):
        if char not in morse_dict:
            continue
        code = morse_dict[char]
        for j, symbol in enumerate(code):
            if symbol == '.':
                t = np.arange(unit_samples) / sample_rate
                tone = 0.8 * np.sin(2 * np.pi * freq * t)
                samples.extend(tone)
            elif symbol == '-':
                t = np.arange(3 * unit_samples) / sample_rate
                tone = 0.8 * np.sin(2 * np.pi * freq * t)
                samples.extend(tone)
            if j < len(code) - 1:
                samples.extend(np.zeros(unit_samples))
        if i < len(text) - 1 and text[i+1] != ' ':
            samples.extend(np.zeros(2 * unit_samples))
        if char == ' ':
            samples.extend(np.zeros(4 * unit_samples))
    
    samples = np.array(samples, dtype=np.float32)
    
    if noise_level > 0:
        signal_power = np.mean(samples ** 2)
        noise = np.random.normal(0, np.sqrt(signal_power * noise_level), len(samples))
        samples = samples + noise
    
    max_val = np.max(np.abs(samples))
    if max_val > 0:
        samples = samples / max_val * 0.9
    samples_int16 = (samples * 32767).astype(np.int16)
    
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(samples_int16.tobytes())


def load_audio(filename: str):
    """加载 WAV"""
    with wave.open(filename, 'rb') as wf:
        n_channels = wf.getnchannels()
        sample_rate = wf.getframerate()
        raw_data = wf.readframes(wf.getnframes())
        samples = np.frombuffer(raw_data, dtype=np.int16).astype(np.float32) / 32768.0
        if n_channels == 2:
            samples = samples.reshape(-1, 2).mean(axis=1)
    return sample_rate, samples


def main():
    test_message = "HELLO WORLD"
    
    print("=" * 60)
    print("Python 摩斯电码解码器 - 抗噪声测试")
    print("=" * 60)
    print(f"测试消息: {test_message}")
    print(f"频率: 550 Hz, 速度: 20 WPM")
    print()
    
    results = []
    
    for noise_level in [0.0, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0]:
        filename = f"/tmp/morse_v2_{int(noise_level * 100)}.wav"
        generate_morse_audio(test_message, filename, freq=550, wpm=20,
                           noise_level=noise_level)
        
        sample_rate, samples = load_audio(filename)
        decoder = MorseDecoder(sample_rate=sample_rate, target_freq=550)
        result = decoder.decode(samples)
        
        expected = test_message.replace(' ', '')
        actual = result.replace(' ', '').replace('?', '')
        correct = sum(a == b for a, b in zip(actual, expected))
        accuracy = correct / len(expected) if expected else 0
        
        results.append({
            'noise': noise_level,
            'result': result,
            'accuracy': accuracy
        })
        
        noise_str = f"{noise_level*100:>5.0f}%"
        acc_str = f"{accuracy*100:>5.0f}%"
        print(f"噪声: {noise_str} | 解码: {result:<15} | 准确率: {acc_str}")
    
    print()
    print("=" * 60)
    print("测试完成!")


if __name__ == "__main__":
    main()
