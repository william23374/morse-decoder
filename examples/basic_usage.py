"""
基础使用示例
演示如何使用摩尔斯电码解码器的基本功能
"""

import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from morse_decoder import MorseDecoderV2, MorseDecoderV3, load_wav_file


def example_basic_usage():
    """基础使用示例"""
    print("=" * 70)
    print("基础使用示例")
    print("=" * 70)

    # 加载音频文件
    file_path = "test_audio/BA4II-1.wav"
    if not Path(file_path).exists():
        print(f"文件不存在: {file_path}")
        return

    sample_rate, audio = load_wav_file(file_path)
    print(f"音频信息: {sample_rate}Hz, {len(audio)/sample_rate:.2f}秒")

    # 使用 V2 解码器
    print("\n--- V2 解码器 ---")
    decoder_v2 = MorseDecoderV2(sample_rate=sample_rate, target_freq=550)
    result_v2 = decoder_v2.decode(audio)
    print(f"解码结果: {result_v2}")

    # 使用 V3 解码器
    print("\n--- V3 解码器 ---")
    decoder_v3 = MorseDecoderV3(sample_rate=sample_rate, target_freq=550, bandwidth=100)
    result_v3 = decoder_v3.decode(audio)
    print(f"解码结果: {result_v3}")


def example_custom_parameters():
    """自定义参数示例"""
    print("\n" + "=" * 70)
    print("自定义参数示例")
    print("=" * 70)

    file_path = "test_audio/BA4II-1.wav"
    if not Path(file_path).exists():
        return

    sample_rate, audio = load_wav_file(file_path)

    # 创建自定义配置的解码器
    decoder = MorseDecoderV2(
        sample_rate=8000,
        target_freq=600,
        bandwidth=150
    )

    result = decoder.decode(audio)
    print(f"自定义频率 (600Hz) 解码结果: {result}")


def example_multiple_files():
    """多文件处理示例"""
    print("\n" + "=" * 70)
    print("多文件处理示例")
    print("=" * 70)

    files = [
        ("test_audio/BA4II-1.wav", 550),
        ("test_audio/BI1NZI.wav", 550),
    ]

    for file_path, freq in files:
        if not Path(file_path).exists():
            continue

        sample_rate, audio = load_wav_file(file_path)

        decoder = MorseDecoderV2(sample_rate=sample_rate, target_freq=freq)
        result = decoder.decode(audio)

        print(f"\n文件: {Path(file_path).name}")
        print(f"结果: {result}")


if __name__ == "__main__":
    example_basic_usage()
    example_custom_parameters()
    example_multiple_files()

    print("\n" + "=" * 70)
    print("示例运行完成!")
    print("=" * 70)
