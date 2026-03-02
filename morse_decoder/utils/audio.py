"""
音频工具函数
"""

import numpy as np
from pathlib import Path
from typing import Tuple


def load_wav_file(file_path: str) -> Tuple[int, np.ndarray]:
    """
    加载 WAV 文件

    参数:
        file_path: WAV 文件路径

    返回:
        (sample_rate, samples) 元组
        sample_rate: 采样率 (Hz)
        samples: 音频样本 (float32, 归一化到 [-1, 1])
    """
    try:
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
            # 尝试归一化
            audio = audio.astype(np.float32)
            audio = audio / (np.max(np.abs(audio)) + 1e-10)

        # 如果是立体声，转换为单声道
        if len(audio.shape) > 1:
            audio = np.mean(audio, axis=1)

        # 检查是否有异常值
        if np.any(np.isnan(audio)) or np.any(np.isinf(audio)):
            audio = np.nan_to_num(audio, nan=0.0, posinf=1.0, neginf=-1.0)

        # 归一化到 [-1, 1] 范围
        max_val = np.max(np.abs(audio))
        if max_val > 1.0:
            audio = audio / max_val

        return sample_rate, audio
    except Exception as e:
        raise ValueError(f"无法加载 WAV 文件 '{file_path}': {e}")


def save_wav_file(file_path: str, samples: np.ndarray, sample_rate: int):
    """
    保存 WAV 文件

    参数:
        file_path: 输出文件路径
        samples: 音频样本 (float32, 应该在 [-1, 1] 范围内)
        sample_rate: 采样率 (Hz)
    """
    try:
        from scipy.io import wavfile

        # 确保 samples 在 [-1, 1] 范围内
        max_val = np.max(np.abs(samples))
        if max_val > 1.0:
            samples = samples / max_val

        # 转换为 int16
        samples_int16 = (samples * 32767).astype(np.int16)

        wavfile.write(file_path, sample_rate, samples_int16)
    except Exception as e:
        raise ValueError(f"无法保存 WAV 文件 '{file_path}': {e}")


def normalize_audio(samples: np.ndarray) -> np.ndarray:
    """
    归一化音频到 [-1, 1] 范围

    参数:
        samples: 音频样本

    返回:
        归一化后的音频样本
    """
    max_val = np.max(np.abs(samples))
    if max_val > 0:
        return samples / max_val
    return samples


def calculate_snr(signal: np.ndarray, noise: np.ndarray) -> float:
    """
    计算信噪比 (SNR)

    参数:
        signal: 信号
        noise: 噪声

    返回:
        SNR (dB)
    """
    signal_power = np.mean(signal ** 2)
    noise_power = np.mean(noise ** 2)

    if noise_power == 0:
        return float('inf')

    snr = 10 * np.log10(signal_power / noise_power)
    return snr


def detect_dominant_frequency(samples: np.ndarray, sample_rate: int) -> float:
    """
    检测音频中的主导频率

    参数:
        samples: 音频样本
        sample_rate: 采样率

    返回:
        主导频率 (Hz)
    """
    from scipy.fft import fft, fftfreq

    n = min(len(samples), 4096)  # 限制样本数提高速度
    yf = fft(samples[:n])
    xf = fftfreq(n, 1 / sample_rate)

    # 只考虑正频率
    positive_freqs = xf[:n // 2]
    power = np.abs(yf[:n // 2]) ** 2

    # 只考虑 200-1500Hz 范围
    mask = (positive_freqs >= 200) & (positive_freqs <= 1500)
    if not np.any(mask):
        return 0.0

    # 找出最大功率频率
    peak_idx = np.argmax(power * mask)
    dominant_freq = positive_freqs[peak_idx]

    return dominant_freq


def get_audio_info(file_path: str) -> dict:
    """
    获取音频文件信息

    参数:
        file_path: WAV 文件路径

    返回:
        包含音频信息的字典
    """
    sample_rate, samples = load_wav_file(file_path)

    info = {
        'file_path': str(file_path),
        'sample_rate': sample_rate,
        'duration': len(samples) / sample_rate,
        'num_samples': len(samples),
        'num_channels': 1,  # 总是转换为单声道
        'min': float(samples.min()),
        'max': float(samples.max()),
        'rms': float(np.sqrt(np.mean(samples ** 2))),
        'dominant_frequency': detect_dominant_frequency(samples, sample_rate)
    }

    return info
