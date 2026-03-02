# Morse Decoder

高性能摩尔斯电码解码器，支持多种解码算法。

## 特性

- **V2 解码器**: 高性能解码器，适合实时应用
  - 处理速度: 1000-1300x 实时
  - 准确率: 100% (清晰信号)
  - 轻量级实现

- **V3 解码器**: 先进算法解码器，适合高噪声环境
  - 4阶 Butterworth IIR 带通滤波器
  - Hilbert 变换包络检波
  - K-means 聚类算法智能分类
  - 自动频率跟踪

- **完整工具集**:
  - 音频加载和保存
  - 音频归一化
  - 信噪比计算
  - 频率检测
  - 摩尔斯电码转换

## 安装

### 从源码安装

```bash
git clone https://github.com/yourusername/morse-decoder.git
cd morse-decoder
pip install -e .
```

### 使用 pip 安装

```bash
pip install morse-decoder
```

### 依赖项

- Python >= 3.8
- numpy >= 1.20.0
- scipy >= 1.7.0
- scikit-learn >= 0.24.0
- sounddevice >= 0.4.5 (可选，用于命令行工具的音频捕获)

## 快速开始

### Python API

```python
from morse_decoder import MorseDecoderV2, load_wav_file

# 加载音频文件
audio_data, sample_rate = load_wav_file("audio.wav")

# 创建解码器
decoder = MorseDecoderV2(sample_rate=sample_rate, frequency=550)

# 解码音频
result = decoder.decode(audio_data)
print(f"解码结果: {result.text}")
```

详细使用说明请参阅 [快速入门指南](docs/QUICKSTART.md)。

### 命令行工具

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

详细命令行使用说明请参阅 [CLI 使用指南](docs/CLI.md)。

### 使用 V3 解码器

```python
from morse_decoder import MorseDecoderV3, load_wav_file

# 加载音频文件
audio_data, sample_rate = load_wav_file("audio.wav")

# 创建解码器（高噪声环境）
decoder = MorseDecoderV3(
    sample_rate=sample_rate,
    frequency=550,
    bandwidth=100,
    enable_freq_tracking=False
)

# 解码音频
result = decoder.decode(audio)
print(f"解码结果: {result.text}")
```

### 自动频率检测

```python
from morse_decoder import MorseDecoderV2, load_wav_file, detect_dominant_frequency

# 加载音频文件
audio_data, sample_rate = load_wav_file("audio.wav")

# 自动检测频率
frequency = detect_dominant_frequency(audio_data, sample_rate)
print(f"检测到频率: {frequency}Hz")

# 使用检测到的频率解码
decoder = MorseDecoderV2(sample_rate=sample_rate, frequency=frequency)
result = decoder.decode(audio_data)
print(f"解码结果: {result.text}")
```

### 摩尔斯电码转换

```python
from morse_decoder import text_to_morse, morse_to_text

# 文本转摩尔斯电码
morse = text_to_morse("HELLO")
print(f"HELLO -> {morse}")

# 摩尔斯电码转文本
text = morse_to_text(".... . .-.. .-.. ---")
print(f".... . .-.. .-.. --- -> {text}")
```

## 命令行工具

`morse-decode` 提供了强大的命令行接口，支持三种输入模式：

### 文件模式
```bash
morse-decode -i audio.wav -f 550
```

### 自动频率检测
```bash
morse-decode -i audio.wav --auto-detect
```

### 麦克风模式
```bash
morse-decode --mic -d 5 -f 550
```

### 流模式（持续监听）
```bash
morse-decode --stream -f 550
```

查看所有选项：
```bash
morse-decode --help
```

详细使用说明请参阅 [CLI 使用指南](docs/CLI.md)。

## 音频工具函数

- `load_wav_file(file_path)`: 加载 WAV 文件
- `save_wav_file(file_path, samples, sample_rate)`: 保存 WAV 文件
- `normalize_audio(samples)`: 归一化音频
- `calculate_snr(signal, noise)`: 计算信噪比
- `detect_dominant_frequency(samples, sample_rate)`: 检测主导频率
- `get_audio_info(file_path)`: 获取音频文件信息

### 摩尔斯电码工具函数

- `text_to_morse(text)`: 文本转摩尔斯电码
- `morse_to_text(morse)`: 摩尔斯电码转文本
- `validate_morse_code(morse)`: 验证摩尔斯电码

## 文档

- **[快速入门指南](docs/QUICKSTART.md)**: 快速开始使用
- **[CLI 使用指南](docs/CLI.md)**: 命令行工具详细说明
- **[API 文档](docs/API.md)**: 完整的 API 参考

## 性能对比

| 解码器 | 准确率 | 速度 | 推荐场景 |
|--------|--------|------|---------|
| V2 | 100% | 1200x | 实时应用 |
| V3 | 100% | 400x | 高噪声环境 |

## 示例

查看 `examples/` 目录获取更多示例：

- `basic_usage.py`: 基础使用示例
- `advanced_usage.py`: 高级功能示例

运行示例：

```bash
cd examples
python basic_usage.py
python advanced_usage.py
```

## 测试

运行测试：

```bash
python -m pytest tests/
```

或使用 unittest：

```bash
python -m unittest tests.test_all
```

## 项目结构

```
morse-decoder/
├── morse_decoder/          # 主包
│   ├── __init__.py
│   ├── v2/                # V2 解码器
│   │   ├── __init__.py
│   │   └── decoder.py
│   ├── v3/                # V3 解码器
│   │   ├── __init__.py
│   │   └── decoder.py
│   └── utils/             # 工具函数
│       ├── __init__.py
│       ├── audio.py
│       └── morse.py
├── tests/                 # 测试
│   ├── __init__.py
│   └── test_all.py
├── examples/              # 示例
│   ├── basic_usage.py
│   └── advanced_usage.py
├── setup.py              # 安装脚本
├── requirements.txt      # 依赖项
├── README.md            # 本文件
└── LICENSE              # 许可证
```

## 贡献

欢迎贡献！请遵循以下步骤：

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 作者

Morse Decoder Team

## 致谢

- M5 CW Decoder 项目
- 音频处理和信号处理领域的开源贡献者

## 更新日志

### 1.0.0 (2026-03-01)

- 初始发布
- V2 解码器：高性能实时解码
- V3 解码器：先进算法，支持高噪声环境
- 完整工具集：音频处理、摩尔斯电码转换
- 测试套件和示例代码

## 联系方式

- 项目主页: https://github.com/yourusername/morse-decoder
- 问题反馈: https://github.com/yourusername/morse-decoder/issues
- 邮箱: contact@morsedecoder.dev
