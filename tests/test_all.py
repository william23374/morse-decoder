"""
摩尔斯电码解码器包测试
"""

import unittest
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from morse_decoder.v2.decoder import MorseDecoder as MorseDecoderV2
from morse_decoder.v3.decoder import MorseDecoderV3
from morse_decoder.utils.audio import load_wav_file, normalize_audio, detect_dominant_frequency
from morse_decoder.utils.morse import text_to_morse, morse_to_text, MORSE_CODE_DICT


class TestMorseV2(unittest.TestCase):
    """V2 解码器测试"""

    def setUp(self):
        """设置测试环境"""
        self.decoder = MorseDecoderV2(sample_rate=8000, target_freq=550)

    def test_initialization(self):
        """测试初始化"""
        self.assertEqual(self.decoder.sample_rate, 8000)
        self.assertEqual(self.decoder.target_freq, 550)

    def test_morse_code_dict(self):
        """测试摩尔斯电码字典"""
        self.assertIn('.-', MORSE_CODE_DICT)
        self.assertEqual(MORSE_CODE_DICT['.-'], 'A')


class TestMorseV3(unittest.TestCase):
    """V3 解码器测试"""

    def setUp(self):
        """设置测试环境"""
        self.decoder = MorseDecoderV3(sample_rate=8000, target_freq=550)

    def test_initialization(self):
        """测试初始化"""
        self.assertEqual(self.decoder.sample_rate, 8000)
        self.assertEqual(self.decoder.target_freq, 550)

    def test_filter_design(self):
        """测试滤波器设计"""
        self.assertIsNotNone(self.decoder._filter_b)
        self.assertIsNotNone(self.decoder._filter_a)


class TestAudioUtils(unittest.TestCase):
    """音频工具测试"""

    def test_normalize_audio(self):
        """测试音频归一化"""
        import numpy as np

        # 测试归一化
        audio = np.array([0.5, 1.0, 2.0, 3.0])
        normalized = normalize_audio(audio)
        self.assertAlmostEqual(normalized.max(), 1.0, places=5)

    def test_text_to_morse(self):
        """测试文本转摩尔斯电码"""
        morse = text_to_morse("SOS")
        self.assertEqual(morse, "... --- ...")

    def test_morse_to_text(self):
        """测试摩尔斯电码转文本"""
        text = morse_to_text("... --- ...")
        self.assertEqual(text, "SOS")


class TestIntegration(unittest.TestCase):
    """集成测试"""

    def test_end_to_end(self):
        """端到端测试"""
        import numpy as np

        # 创建简单的摩尔斯电码信号
        sample_rate = 8000
        freq = 550
        t = np.linspace(0, 0.1, int(sample_rate * 0.1))
        signal = 0.5 * np.sin(2 * np.pi * freq * t)

        # 测试 V2 解码器
        decoder_v2 = MorseDecoderV2(sample_rate=sample_rate, target_freq=freq)
        result_v2 = decoder_v2.decode(signal)
        self.assertIsInstance(result_v2, str)

        # 测试 V3 解码器
        decoder_v3 = MorseDecoderV3(sample_rate=sample_rate, target_freq=freq)
        result_v3 = decoder_v3.decode(signal)
        self.assertIsInstance(result_v3, str)


if __name__ == '__main__':
    unittest.main()
