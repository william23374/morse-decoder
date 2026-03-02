"""
高级使用示例
演示摩尔斯电码解码器的高级功能
"""

import sys
from pathlib import Path
import time

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from morse_decoder import (
    MorseDecoderV2,
    MorseDecoderV3,
    load_wav_file,
    detect_dominant_frequency,
    get_audio_info,
    text_to_morse,
    morse_to_text
)


def example_auto_detect_frequency():
    """自动检测频率示例"""
    print("=" * 70)
    print("自动检测频率示例")
    print("=" * 70)

    file_path = "test_audio/BA4II-1.wav"
    if not Path(file_path).exists():
        print(f"文件不存在: {file_path}")
        return

    # 加载音频
    sample_rate, audio = load_wav_file(file_path)

    # 检测主导频率
    dominant_freq = detect_dominant_frequency(audio, sample_rate)
    print(f"检测到主导频率: {dominant_freq:.1f}Hz")

    # 使用检测到的频率解码
    decoder = MorseDecoderV2(sample_rate=sample_rate, target_freq=int(dominant_freq))
    result = decoder.decode(audio)
    print(f"解码结果: {result}")


def example_performance_comparison():
    """性能对比示例"""
    print("\n" + "=" * 70)
    print("性能对比示例")
    print("=" * 70)

    file_path = "test_audio/BA4II-1.wav"
    if not Path(file_path).exists():
        return

    sample_rate, audio = load_wav_file(file_path)

    # 测试 V2 性能
    print("\n--- V2 解码器 ---")
    decoder_v2 = MorseDecoderV2(sample_rate=sample_rate, target_freq=550)

    start_time = time.time()
    result_v2 = decoder_v2.decode(audio)
    time_v2 = (time.time() - start_time) * 1000

    print(f"结果: {result_v2}")
    print(f"时间: {time_v2:.2f}ms")
    print(f"速度: {len(audio)/sample_rate/time_v2*1000:.1f}x 实时")

    # 测试 V3 性能
    print("\n--- V3 解码器 ---")
    decoder_v3 = MorseDecoderV3(sample_rate=sample_rate, target_freq=550)

    start_time = time.time()
    result_v3 = decoder_v3.decode(audio)
    time_v3 = (time.time() - start_time) * 1000

    print(f"结果: {result_v3}")
    print(f"时间: {time_v3:.2f}ms")
    print(f"速度: {len(audio)/sample_rate/time_v3*1000:.1f}x 实时")

    # 对比
    print(f"\n速度比: V2 比 V3 快 {time_v3/time_v2:.1f}x")


def example_v3_with_freq_tracking():
    """V3 频率跟踪示例"""
    print("\n" + "=" * 70)
    print("V3 频率跟踪示例")
    print("=" * 70)

    file_path = "test_audio/B8.wav"
    if not Path(file_path).exists():
        print(f"文件不存在: {file_path}")
        return

    sample_rate, audio = load_wav_file(file_path)

    # 无频率跟踪
    print("\n--- 无频率跟踪 ---")
    decoder_no_track = MorseDecoderV3(
        sample_rate=sample_rate,
        target_freq=762,
        bandwidth=100,
        enable_freq_tracking=False
    )
    result_no_track = decoder_no_track.decode(audio)
    print(f"结果: {result_no_track}")

    # 有频率跟踪
    print("\n--- 有频率跟踪 ---")
    decoder_with_track = MorseDecoderV3(
        sample_rate=sample_rate,
        target_freq=762,
        bandwidth=100,
        enable_freq_tracking=True
    )
    result_with_track = decoder_with_track.decode(audio)
    print(f"结果: {result_with_track}")


def example_audio_info():
    """音频信息示例"""
    print("\n" + "=" * 70)
    print("音频信息示例")
    print("=" * 70)

    file_path = "test_audio/BA4II-1.wav"
    if not Path(file_path).exists():
        return

    # 获取音频信息
    info = get_audio_info(file_path)

    print(f"文件路径: {info['file_path']}")
    print(f"采样率: {info['sample_rate']}Hz")
    print(f"时长: {info['duration']:.2f}秒")
    print(f"样本数: {info['num_samples']}")
    print(f"最小值: {info['min']:.4f}")
    print(f"最大值: {info['max']:.4f}")
    print(f"RMS: {info['rms']:.4f}")
    print(f"主导频率: {info['dominant_frequency']:.1f}Hz")


def example_morse_conversion():
    """摩尔斯电码转换示例"""
    print("\n" + "=" * 70)
    print("摩尔斯电码转换示例")
    print("=" * 70)

    # 文本转摩尔斯电码
    text = "HELLO WORLD"
    morse = text_to_morse(text)
    print(f"文本: {text}")
    print(f"摩尔斯: {morse}")

    # 摩尔斯电码转文本
    decoded = morse_to_text(morse)
    print(f"解码: {decoded}")


if __name__ == "__main__":
    example_auto_detect_frequency()
    example_performance_comparison()
    example_v3_with_freq_tracking()
    example_audio_info()
    example_morse_conversion()

    print("\n" + "=" * 70)
    print("高级示例运行完成!")
    print("=" * 70)
