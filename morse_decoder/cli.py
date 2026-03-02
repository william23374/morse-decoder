"""
摩尔斯电码解码器命令行接口
支持 WAV 文件和实时音频捕获
"""

import argparse
import sys
import time
from pathlib import Path
from typing import Optional
import numpy as np


def decode_from_file(args):
    """从 WAV 文件解码"""
    from morse_decoder import (
        MorseDecoderV2,
        MorseDecoderV3,
        load_wav_file,
        get_audio_info,
        detect_dominant_frequency
    )

    print("=" * 70)
    print("摩尔斯电码解码器 - 文件模式")
    print("=" * 70)

    file_path = args.input

    # 检查文件是否存在
    if not Path(file_path).exists():
        print(f"❌ 错误: 文件不存在: {file_path}")
        return 1

    print(f"\n📁 文件: {file_path}")

    try:
        # 加载音频
        sample_rate, audio = load_wav_file(file_path)
        duration = len(audio) / sample_rate

        print(f"🎵 音频信息:")
        print(f"   采样率: {sample_rate}Hz")
        print(f"   时长: {duration:.2f}秒")
        print(f"   样本数: {len(audio)}")

        # 检测主导频率
        if args.auto_detect:
            dominant_freq = detect_dominant_frequency(audio, sample_rate)
            target_freq = int(dominant_freq)
            print(f"   检测频率: {dominant_freq:.1f}Hz")
        else:
            target_freq = args.frequency
            print(f"   目标频率: {target_freq}Hz")

        # 选择解码器
        if args.decoder == 'v2':
            print(f"\n🔧 使用 V2 解码器")
            decoder = MorseDecoderV2(sample_rate=sample_rate, target_freq=target_freq)
        elif args.decoder == 'v3':
            print(f"\n🔧 使用 V3 解码器")
            decoder = MorseDecoderV3(
                sample_rate=sample_rate,
                target_freq=target_freq,
                bandwidth=args.bandwidth,
                enable_freq_tracking=args.freq_tracking
            )
        else:
            print(f"❌ 错误: 未知的解码器类型: {args.decoder}")
            return 1

        # 解码
        print(f"\n🔍 开始解码...")
        start_time = time.time()
        result = decoder.decode(audio)
        decode_time = (time.time() - start_time) * 1000

        # 输出结果
        print(f"\n{'='*70}")
        print(f"📝 解码结果:")
        print(f"{'='*70}")
        print(f"{result}")
        print(f"\n⏱️  解码时间: {decode_time:.2f}ms")
        print(f"📊 处理速度: {duration/decode_time*1000:.1f}x 实时")

        # 统计信息
        valid_chars = sum(1 for c in result if c.isalnum())
        print(f"\n📈 统计:")
        print(f"   总字符数: {len(result)}")
        print(f"   有效字符数: {valid_chars}")

        return 0

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return 1


def decode_from_mic(args):
    """从麦克风实时解码"""
    try:
        import sounddevice as sd
    except ImportError:
        print("❌ 错误: 需要安装 sounddevice 库")
        print("   请运行: pip install sounddevice")
        return 1

    from morse_decoder import MorseDecoderV2, MorseDecoderV3

    print("=" * 70)
    print("摩尔斯电码解码器 - 实时模式")
    print("=" * 70)

    # 参数
    sample_rate = args.sample_rate
    duration = args.duration  # 秒
    channels = 1  # 单声道

    print(f"\n🎤 音频捕获设置:")
    print(f"   采样率: {sample_rate}Hz")
    print(f"   时长: {duration}秒")
    print(f"   频率: {args.frequency}Hz")

    # 选择解码器
    if args.decoder == 'v2':
        print(f"\n🔧 使用 V2 解码器")
        decoder = MorseDecoderV2(sample_rate=sample_rate, target_freq=args.frequency)
    elif args.decoder == 'v3':
        print(f"\n🔧 使用 V3 解码器")
        decoder = MorseDecoderV3(
            sample_rate=sample_rate,
            target_freq=args.frequency,
            bandwidth=args.bandwidth,
            enable_freq_tracking=args.freq_tracking
        )
    else:
        print(f"❌ 错误: 未知的解码器类型: {args.decoder}")
        return 1

    print(f"\n🎙️  请播放摩尔斯电码音频...")

    # 录制音频
    try:
        print(f"⏳ 录制中... (按 Ctrl+C 停止)")
        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=channels,
            dtype='float64'
        )
        sd.wait()  # 等待录制完成
    except KeyboardInterrupt:
        print(f"\n⚠️  录制已取消")
        return 0
    except Exception as e:
        print(f"\n❌ 录制失败: {e}")
        return 1

    # 转换为单声道
    audio = recording.flatten()
    audio = audio.astype(np.float32)

    print(f"\n✅ 录制完成")

    # 解码
    print(f"\n🔍 开始解码...")
    start_time = time.time()
    result = decoder.decode(audio)
    decode_time = (time.time() - start_time) * 1000

    # 输出结果
    print(f"\n{'='*70}")
    print(f"📝 解码结果:")
    print(f"{'='*70}")
    print(f"{result}")
    print(f"\n⏱️  解码时间: {decode_time:.2f}ms")

    return 0


def decode_from_stream(args):
    """从音频流实时解码（持续模式）"""
    try:
        import sounddevice as sd
    except ImportError:
        print("❌ 错误: 需要安装 sounddevice 库")
        print("   请运行: pip install sounddevice")
        return 1

    from morse_decoder import MorseDecoderV2, MorseDecoderV3

    print("=" * 70)
    print("摩尔斯电码解码器 - 流模式 (持续解码)")
    print("=" * 70)

    # 参数
    sample_rate = args.sample_rate
    block_size = int(args.block_size * sample_rate)  # 块大小
    channels = 1

    print(f"\n🎤 音频流设置:")
    print(f"   采样率: {sample_rate}Hz")
    print(f"   块大小: {args.block_size}秒 ({block_size} 样本)")
    print(f"   频率: {args.frequency}Hz")
    print(f"\n🎙️  正在监听音频流... (按 Ctrl+C 停止)")

    # 选择解码器
    if args.decoder == 'v2':
        decoder = MorseDecoderV2(sample_rate=sample_rate, target_freq=args.frequency)
    elif args.decoder == 'v3':
        decoder = MorseDecoderV3(
            sample_rate=sample_rate,
            target_freq=args.frequency,
            bandwidth=args.bandwidth,
            enable_freq_tracking=args.freq_tracking
        )
    else:
        print(f"❌ 错误: 未知的解码器类型: {args.decoder}")
        return 1

    # 音频回调函数
    audio_buffer = []
    last_decode_time = time.time()

    def audio_callback(indata, frames, time_info, status):
        nonlocal audio_buffer, last_decode_time

        if status:
            print(f"⚠️  音频状态: {status}", file=sys.stderr)

        # 添加到缓冲区
        audio_chunk = indata.flatten().astype(np.float32)
        audio_buffer.extend(audio_chunk)

        # 检查是否需要解码
        current_time = time.time()
        if len(audio_buffer) >= sample_rate * args.block_size:
            # 提取块
            samples = np.array(audio_buffer[:int(sample_rate * args.block_size)])
            audio_buffer = audio_buffer[int(sample_rate * args.block_size):]

            # 解码
            try:
                result = decoder.decode(samples)

                # 如果有结果，显示
                if result and len(result) > 0:
                    valid_chars = sum(1 for c in result if c.isalnum())
                    if valid_chars > 0:
                        timestamp = time.strftime("%H:%M:%S")
                        print(f"[{timestamp}] {result}")

                last_decode_time = current_time
            except Exception as e:
                print(f"❌ 解码错误: {e}", file=sys.stderr)

    try:
        # 创建音频流
        with sd.InputStream(
            samplerate=sample_rate,
            channels=channels,
            callback=audio_callback
        ):
            # 持续运行直到用户中断
            while True:
                time.sleep(0.1)

    except KeyboardInterrupt:
        print(f"\n\n⚠️  已停止")
        return 0
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return 1


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='摩尔斯电码解码器命令行工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 从 WAV 文件解码
  morse-decode -i audio.wav -f 550

  # 从麦克风录制并解码
  morse-decode --mic -d 5 -f 550

  # 持续监听音频流
  morse-decode --stream -f 550

  # 使用 V3 解码器
  morse-decode -i audio.wav -f 550 --decoder v3
        """
    )

    # 输入模式
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        '-i', '--input',
        type=str,
        help='输入 WAV 文件路径'
    )
    mode_group.add_argument(
        '--mic',
        action='store_true',
        help='从麦克风录制'
    )
    mode_group.add_argument(
        '--stream',
        action='store_true',
        help='持续监听音频流'
    )

    # 解码器参数
    parser.add_argument(
        '-f', '--frequency',
        type=float,
        default=550,
        help='目标频率 (Hz), 默认: 550'
    )
    parser.add_argument(
        '-b', '--bandwidth',
        type=float,
        default=100,
        help='带宽 (Hz), 默认: 100'
    )
    parser.add_argument(
        '--decoder',
        type=str,
        choices=['v2', 'v3'],
        default='v2',
        help='解码器类型 (v2 或 v3), 默认: v2'
    )

    # V3 特定参数
    parser.add_argument(
        '--freq-tracking',
        action='store_true',
        help='启用频率跟踪 (仅 V3)'
    )

    # 自动检测
    parser.add_argument(
        '--auto-detect',
        action='store_true',
        help='自动检测音频频率'
    )

    # 麦克风参数
    parser.add_argument(
        '-d', '--duration',
        type=float,
        default=5.0,
        help='录制时长 (秒), 默认: 5.0'
    )
    parser.add_argument(
        '--sample-rate',
        type=int,
        default=8000,
        help='采样率 (Hz), 默认: 8000'
    )
    parser.add_argument(
        '--block-size',
        type=float,
        default=1.0,
        help='流模式块大小 (秒), 默认: 1.0'
    )

    # 解析参数
    args = parser.parse_args()

    # 根据模式执行
    if args.input:
        return decode_from_file(args)
    elif args.mic:
        return decode_from_mic(args)
    elif args.stream:
        return decode_from_stream(args)
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
