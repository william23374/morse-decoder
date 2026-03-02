# API 文档

## 模块索引

### morse_decoder.v2.decoder

V2 解码器模块

#### MorseDecoder

高性能摩尔斯电码解码器

**初始化参数**:
- `sample_rate` (int): 采样率 (Hz)，默认 8000
- `target_freq` (float): 目标频率 (Hz)，默认 550
- `bandwidth` (float): 带宽 (Hz)，默认 200

**方法**:

##### `decode(samples: np.ndarray) -> str`

解码音频样本

**参数**:
- `samples`: 音频样本 (float32, 归一化到 [-1, 1])

**返回**:
- 解码后的文本字符串

---

### morse_decoder.v3.decoder

V3 解码器模块

#### MorseDecoderV3

先进算法摩尔斯电码解码器

**初始化参数**:
- `sample_rate` (int): 采样率 (Hz)，默认 8000
- `target_freq` (float): 目标频率 (Hz)，默认 550
- `bandwidth` (float): 带宽 (Hz)，默认 100
- `enable_freq_tracking` (bool): 是否启用频率跟踪，默认 True

**方法**:

##### `decode(samples: np.ndarray) -> str`

解码音频样本

**参数**:
- `samples`: 音频样本 (float32, 归一化到 [-1, 1])

**返回**:
- 解码后的文本字符串

---

### morse_decoder.utils.audio

音频工具函数模块

#### `load_wav_file(file_path: str) -> Tuple[int, np.ndarray]`

加载 WAV 文件

**参数**:
- `file_path`: WAV 文件路径

**返回**:
- `(sample_rate, samples)` 元组
  - sample_rate: 采样率 (Hz)
  - samples: 音频样本 (float32, 归一化到 [-1, 1])

#### `save_wav_file(file_path: str, samples: np.ndarray, sample_rate: int)`

保存 WAV 文件

**参数**:
- `file_path`: 输出文件路径
- `samples`: 音频样本 (float32, 应该在 [-1, 1] 范围内)
- `sample_rate`: 采样率 (Hz)

#### `normalize_audio(samples: np.ndarray) -> np.ndarray`

归一化音频到 [-1, 1] 范围

**参数**:
- `samples`: 音频样本

**返回**:
- 归一化后的音频样本

#### `calculate_snr(signal: np.ndarray, noise: np.ndarray) -> float`

计算信噪比 (SNR)

**参数**:
- `signal`: 信号
- `noise`: 噪声

**返回**:
- SNR (dB)

#### `detect_dominant_frequency(samples: np.ndarray, sample_rate: int) -> float`

检测音频中的主导频率

**参数**:
- `samples`: 音频样本
- `sample_rate`: 采样率

**返回**:
- 主导频率 (Hz)

#### `get_audio_info(file_path: str) -> dict`

获取音频文件信息

**参数**:
- `file_path`: WAV 文件路径

**返回**:
- 包含音频信息的字典：
  - `file_path`: 文件路径
  - `sample_rate`: 采样率
  - `duration`: 时长 (秒)
  - `num_samples`: 样本数
  - `num_channels`: 声道数
  - `min`: 最小值
  - `max`: 最大值
  - `rms`: RMS 值
  - `dominant_frequency`: 主导频率

---

### morse_decoder.utils.morse

摩尔斯电码工具函数模块

#### `MORSE_CODE_DICT`

标准摩尔斯电码字典 (代码 -> 字母)

#### `REVERSE_MORSE_DICT`

反向摩尔斯电码字典 (字母 -> 代码)

#### `text_to_morse(text: str) -> str`

将文本转换为摩尔斯电码

**参数**:
- `text`: 要转换的文本

**返回**:
- 摩尔斯电码字符串

#### `morse_to_text(morse: str) -> str`

将摩尔斯电码转换为文本

**参数**:
- `morse`: 摩尔斯电码字符串（用空格分隔）

**返回**:
- 解码后的文本

#### `validate_morse_code(morse: str) -> bool`

验证摩尔斯电码字符串是否有效

**参数**:
- `morse`: 摩尔斯电码字符串

**返回**:
- 如果有效返回 True，否则返回 False

#### `get_morse_dict() -> dict`

获取摩尔斯电码字典

**返回**:
- 摩尔斯电码字典的副本

#### `get_reverse_morse_dict() -> dict`

获取反向摩尔斯电码字典

**返回**:
- 反向摩尔斯电码字典的副本
