# 快速入门指南

## 安装

```bash
pip install morse-decoder
```

## 快速开始

### 1. 从文件解码

```python
from morse_decoder import MorseDecoderV2, load_wav_file

# 加载音频文件
audio_data, sample_rate = load_wav_file('audio.wav')

# 创建解码器
decoder = MorseDecoderV2(sample_rate=sample_rate, frequency=550)

# 解码
result = decoder.decode(audio_data)

print(result.text)  # 解码后的文本
```

### 2. 自动检测频率

```python
from morse_decoder import MorseDecoderV2, load_wav_file, detect_dominant_frequency

# 加载音频
audio_data, sample_rate = load_wav_file('audio.wav')

# 自动检测频率
frequency = detect_dominant_frequency(audio_data, sample_rate)
print(f"检测到频率: {frequency}Hz")

# 使用检测到的频率解码
decoder = MorseDecoderV2(sample_rate=sample_rate, frequency=frequency)
result = decoder.decode(audio_data)

print(result.text)
```

### 3. 使用命令行工具

```bash
# 文件解码
morse-decode -i audio.wav -f 550

# 自动检测频率
morse-decode -i audio.wav --auto-detect

# 麦克风录制
morse-decode --mic -d 5 -f 550

# 持续监听
morse-decode --stream -f 550
```

### 4. 使用 V3 解码器（高噪声环境）

```python
from morse_decoder import MorseDecoderV3, load_wav_file

# 加载音频
audio_data, sample_rate = load_wav_file('noisy_audio.wav')

# 创建 V3 解码器
decoder = MorseDecoderV3(
    sample_rate=sample_rate,
    frequency=550,
    enable_freq_tracking=True
)

# 解码
result = decoder.decode(audio_data)

print(result.text)
```

### 5. 摩尔斯电码转换

```python
from morse_decoder import text_to_morse, morse_to_text

# 文本转摩尔斯
morse = text_to_morse("HELLO WORLD")
print(morse)  # ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."

# 摩尔斯转文本
text = morse_to_text(".... . .-.. .-.. --- / .-- --- .-. .-.. -..")
print(text)  # "HELLO WORLD"
```

### 6. 音频处理工具

```python
from morse_decoder import (
    load_wav_file,
    save_wav_file,
    normalize_audio,
    calculate_snr,
    get_audio_info
)

# 加载音频
audio_data, sample_rate = load_wav_file('audio.wav')

# 获取音频信息
info = get_audio_info(audio_data, sample_rate)
print(f"时长: {info['duration']}秒")
print(f"样本数: {info['num_samples']}")
print(f"最大振幅: {info['max_amplitude']}")

# 归一化
normalized = normalize_audio(audio_data)

# 计算信噪比
snr = calculate_snr(audio_data)
print(f"信噪比: {snr:.2f}dB")

# 保存音频
save_wav_file('normalized.wav', normalized, sample_rate)
```

## 高级用法

### 自定义解码参数

```python
from morse_decoder import MorseDecoderV2, load_wav_file

audio_data, sample_rate = load_wav_file('audio.wav')

decoder = MorseDecoderV2(
    sample_rate=sample_rate,
    frequency=550,
    bandwidth=150,          # 带宽
    dot_duration=0.05,      # 点时长 (秒)
    dash_duration=0.15,     # 划时长 (秒)
    symbol_gap=0.05,        # 符号间隙
    letter_gap=0.15,        # 字母间隙
    word_gap=0.35           # 单词间隙
)

result = decoder.decode(audio_data)
```

### 处理解码结果

```python
from morse_decoder import MorseDecoderV2, load_wav_file

audio_data, sample_rate = load_wav_file('audio.wav')
decoder = MorseDecoderV2(sample_rate=sample_rate, frequency=550)
result = decoder.decode(audio_data)

# 解码结果包含多个信息
print(f"文本: {result.text}")
print(f"摩尔斯码: {result.morse}")
print(f"解码时间: {result.decode_time:.2f}ms")
print(f"处理速度: {result.processing_speed:.1f}x")
print(f"字符数: {result.total_chars}")
print(f"有效字符数: {result.valid_chars}")

# 检查解码是否成功
if result.success:
    print("解码成功！")
else:
    print(f"解码失败: {result.error}")
```

### 批量处理文件

```python
import os
from morse_decoder import MorseDecoderV2, load_wav_file

# 创建解码器
decoder = MorseDecoderV2(sample_rate=8000, frequency=550)

# 处理目录中的所有 WAV 文件
for filename in os.listdir('audio_files'):
    if filename.endswith('.wav'):
        filepath = os.path.join('audio_files', filename)
        audio_data, _ = load_wav_file(filepath)
        result = decoder.decode(audio_data)

        print(f"{filename}: {result.text}")
```

## 命令行高级用法

### 批量处理

```bash
#!/bin/bash
# 批量解码脚本

for file in *.wav; do
    echo "=== 解码 $file ==="
    morse-decode -i "$file" --auto-detect
    echo ""
done
```

### 保存结果

```bash
# 保存解码结果到文件
morse-decode -i audio.wav --auto-detect > results.txt

# 保存到带时间戳的文件
morse-decode -i audio.wav --auto-detect > "result_$(date +%Y%m%d_%H%M%S).txt"
```

### 性能对比

```bash
# 比较 V2 和 V3 解码器
echo "V2 解码器:"
time morse-decode -i audio.wav -f 550 --decoder v2

echo "V3 解码器:"
time morse-decode -i audio.wav -f 550 --decoder v3
```

## 常见问题

### Q: 如何选择解码器？

**A:**
- **V2**: 速度快，适合实时应用和高质量音频
- **V3**: 准确率高，适合高噪声环境

### Q: 如何设置正确的频率？

**A:** 使用自动检测功能：

```python
from morse_decoder import detect_dominant_frequency, load_wav_file

audio_data, sample_rate = load_wav_file('audio.wav')
frequency = detect_dominant_frequency(audio_data, sample_rate)
```

或命令行：

```bash
morse-decode -i audio.wav --auto-detect
```

### Q: 解码结果不准确怎么办？

**A:**
1. 使用 V3 解码器
2. 启用频率跟踪（V3）
3. 调整带宽参数
4. 确保音频质量良好

### Q: 如何处理实时音频？

**A:** 使用命令行的流模式或麦克风模式：

```bash
# 持续监听
morse-decode --stream -f 550

# 录制并解码
morse-decode --mic -d 10 -f 550
```

## 下一步

- 阅读 [API 文档](API.md) 了解所有功能
- 阅读 [CLI 使用指南](CLI.md) 学习命令行工具
- 查看 [示例代码](../examples/) 了解更多用法
- 运行 [测试](../tests/) 验证安装

## 获取帮助

- 文档: https://github.com/yourusername/morse-decoder
- 问题: https://github.com/yourusername/morse-decoder/issues
