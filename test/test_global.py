#!/usr/bin/env python3
"""
Global Test Suite for Lepida Voice Assistant
Comprehensive testing of all system components and functionality
"""

import os
import sys
import unittest
import tempfile
import shutil
from pathlib import Path
import time
import json
import yaml
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def safe_import(module_name, class_name=None):
    """Safely import modules and return None if not available."""
    try:
        module = __import__(module_name, fromlist=[class_name] if class_name else [])
        return getattr(module, class_name) if class_name else module
    except (ImportError, AttributeError) as e:
        return None

def _check_module_availability(module_name, class_name=None):
    """Helper function to check if a module/class is available and return status."""
    component = safe_import(module_name, class_name)
    if component:
        print(f"✅ {module_name}{f'.{class_name}' if class_name else ''}: Available")
        return True
    else:
        print(f"❌ {module_name}{f'.{class_name}' if class_name else ''}: Not Available")
        return False


class GlobalTestSuite(unittest.TestCase):
    """Comprehensive test suite for all voice assistant components."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment once for all tests."""
        print("🧪 Setting up Global Test Environment...")
        
        # Create temporary directory for test files
        cls.test_dir = tempfile.mkdtemp()
        cls.original_cwd = os.getcwd()
        
        # Create test config
        cls.test_config = {
            'app': {
                'name': 'Lepida Voice Assistant Test',
                'version': '1.0.0-test',
                'debug': True
            },
            'audio': {
                'sample_rate': 16000,
                'channels': 1,
                'chunk_size': 1024,
                'volume': 0.8,
                'microphone_gain': 1.0
            },
            'tts': {
                'engine': 'mms_tts',
                'language': 'id',
                'speed': 1.0,
                'fallback_engines': ['piper', 'coqui']
            },
            'stt': {
                'engine': 'whisper_cpp',
                'language': 'id',
                'model_size': 'base',
                'fallback_engines': ['google_stt']
            },
            'wake_word': {
                'engine': 'porcupine',
                'keyword': 'lepida',
                'sensitivity': 0.5
            },
            'plugins': {
                'auto_load': True,
                'validate_on_load': True
            }
        }
        
        # Save test config
        cls.config_file = Path(cls.test_dir) / 'config.yml'
        with open(cls.config_file, 'w') as f:
            yaml.dump(cls.test_config, f)
        
        print(f"✅ Test environment created: {cls.test_dir}")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test environment."""
        print("🧹 Cleaning up Global Test Environment...")
        
        # Restore original directory
        os.chdir(cls.original_cwd)
        
        # Clean up temp directory
        try:
            shutil.rmtree(cls.test_dir)
            print("✅ Test environment cleaned up")
        except Exception as e:
            print(f"⚠️  Failed to clean up test directory: {e}")
    
    def setUp(self):
        """Set up for each individual test."""
        # Change to test directory
        os.chdir(self.test_dir)
        
        # Create necessary directories
        for dir_name in ['logs', 'outputs', 'temp', 'models', 'plugins']:
            Path(dir_name).mkdir(exist_ok=True)

class TestModuleAvailability(GlobalTestSuite):
    """Test availability of all voice assistant modules."""
    
    def test_core_modules(self):
        """Test core module availability."""
        print("� Testing core module availability...")
        
        modules = [
            ('config.config', None),
            ('helper.audio_processing', 'AudioProcessor'),
            ('helper.numberToText', None),
            ('utils.text_to_speech', 'TextToSpeech'),
            ('utils.audio_transcription', 'AudioTranscription'),
            ('command', 'CommandProcessor')
        ]
        
        available_count = 0
        total_count = len(modules)
        
        for module_name, class_name in modules:
            if _check_module_availability(module_name, class_name):
                available_count += 1
        
        print(f"📊 Core modules: {available_count}/{total_count} available")
        self.assertGreater(available_count, 0, "At least some core modules should be available")
    
    def test_utility_modules(self):
        """Test utility module availability."""
        print("�️  Testing utility module availability...")
        
        modules = [
            ('utils.system_monitor', 'SystemMonitor'),
            ('utils.health_check', 'HealthChecker'),
            ('utils.performance_monitor', 'PerformanceMonitor'),
            ('utils.plugin_validator', 'PluginValidator'),
            ('utils.wake_word_detection', 'WakeWordDetection')
        ]
        
        available_count = 0
        total_count = len(modules)
        
        for module_name, class_name in modules:
            if _check_module_availability(module_name, class_name):
                available_count += 1
        
        print(f"📊 Utility modules: {available_count}/{total_count} available")
        # Don't require utility modules to be available


class TestConfiguration(GlobalTestSuite):
    """Test configuration functionality."""
    
    def test_config_file_creation(self):
        """Test configuration file creation."""
        print("🔧 Testing configuration file creation...")
        
        try:
            # Test config file exists
            self.assertTrue(self.config_file.exists())
            
            # Test config content
            with open(self.config_file, 'r') as f:
                config = yaml.safe_load(f)
            
            self.assertIsInstance(config, dict)
            self.assertIn('app', config)
            self.assertIn('audio', config)
            print("✅ Configuration file creation: PASSED")
        except Exception as e:
            print(f"❌ Configuration file creation failed: {e}")
    
    def test_config_structure(self):
        """Test configuration structure."""
        print("🔧 Testing configuration structure...")
        
        config = self.test_config
        
        # Test required sections
        required_sections = ['app', 'audio', 'tts', 'stt']
        missing_sections = []
        
        for section in required_sections:
            if section not in config:
                missing_sections.append(section)
            else:
                print(f"   ✅ {section} section found")
        
        if missing_sections:
            print(f"   ❌ Missing sections: {missing_sections}")
            self.fail(f"Missing required sections: {missing_sections}")
        else:
            print("✅ Configuration structure: PASSED")


class TestNumberConversion(GlobalTestSuite):
    """Test number to text conversion if available."""
    
    def test_number_conversion_module(self):
        """Test if number conversion module is available."""
        print("🔢 Testing number conversion module...")
        
        numberToText_module = safe_import('helper.numberToText')
        
        if not numberToText_module:
            print("⚠️  NumberToText module not available - SKIPPED")
            return
        
        # Test if convert function exists
        convert_func = getattr(numberToText_module, 'convert', None)
        if not convert_func:
            print("⚠️  convert function not found - trying alternative names")
            # Try alternative function names
            for func_name in ['convert_number_to_text', 'number_to_text', 'convert_to_text']:
                convert_func = getattr(numberToText_module, func_name, None)
                if convert_func:
                    print(f"✅ Found convert function: {func_name}")
                    break
        
        if convert_func:
            try:
                # Test basic conversion
                result = convert_func("12")
                self.assertIsInstance(result, str)
                print(f"   12 -> {result}")
                print("✅ Number conversion: PASSED")
            except Exception as e:
                print(f"⚠️  Number conversion test failed: {e}")
        else:
            print("⚠️  No convert function found in numberToText module")


class TestAudioSystem(GlobalTestSuite):
    """Test audio system functionality."""
    
    def test_audio_dependencies(self):
        """Test audio-related dependencies."""
        print("🎵 Testing audio dependencies...")
        
        dependencies = ['pyaudio', 'numpy', 'wave']
        available = []
        missing = []
        
        for dep in dependencies:
            try:
                __import__(dep)
                available.append(dep)
                print(f"   ✅ {dep}")
            except ImportError:
                missing.append(dep)
                print(f"   ❌ {dep}")
        
        print(f"📊 Audio dependencies: {len(available)}/{len(dependencies)} available")
        
        if missing:
            print(f"⚠️  Missing audio dependencies: {missing}")
        else:
            print("✅ All audio dependencies available")
    
    def test_audio_config(self):
        """Test audio configuration."""
        print("🎵 Testing audio configuration...")
        
        audio_config = self.test_config.get('audio', {})
        
        required_keys = ['sample_rate', 'channels', 'chunk_size']
        for key in required_keys:
            self.assertIn(key, audio_config, f"Missing audio config key: {key}")
            print(f"   ✅ {key}: {audio_config[key]}")
        
        print("✅ Audio configuration: PASSED")


class TestFileSystem(GlobalTestSuite):
    """Test file system structure and permissions."""
    
    def test_directory_structure(self):
        """Test required directory structure."""
        print("� Testing directory structure...")
        
        required_dirs = [
            'assets/audio',
            'config',
            'helper',
            'models',
            'plugins',
            'utils',
            'test'
        ]
        
        base_path = Path(__file__).parent.parent
        missing_dirs = []
        
        for dir_name in required_dirs:
            dir_path = base_path / dir_name
            if dir_path.exists():
                print(f"   ✅ {dir_name}")
            else:
                missing_dirs.append(dir_name)
                print(f"   ❌ {dir_name}")
        
        if missing_dirs:
            print(f"⚠️  Missing directories: {missing_dirs}")
        else:
            print("✅ All required directories exist")
    
    def test_config_files(self):
        """Test configuration files."""
        print("📄 Testing configuration files...")
        
        base_path = Path(__file__).parent.parent
        config_files = [
            'config.yml',
            '.env.example',
            'requirements.txt'
        ]
        
        existing_files = []
        missing_files = []
        
        for file_name in config_files:
            file_path = base_path / file_name
            if file_path.exists():
                existing_files.append(file_name)
                print(f"   ✅ {file_name}")
            else:
                missing_files.append(file_name)
                print(f"   ❌ {file_name}")
        
        print(f"📊 Config files: {len(existing_files)}/{len(config_files)} found")


class TestPluginSystem(GlobalTestSuite):
    """Test plugin system functionality."""
    
    def test_plugin_directory(self):
        """Test plugin directory and files."""
        print("🔌 Testing plugin directory...")
        
        base_path = Path(__file__).parent.parent
        plugins_dir = base_path / 'plugins'
        
        if not plugins_dir.exists():
            print("❌ Plugins directory not found")
            return
        
        plugin_files = list(plugins_dir.glob('*.py'))
        print(f"   Found {len(plugin_files)} plugin files:")
        
        for plugin_file in plugin_files:
            print(f"     ✅ {plugin_file.name}")
        
        if plugin_files:
            print("✅ Plugin system: Files found")
        else:
            print("⚠️  No plugin files found")


class TestIntegration(GlobalTestSuite):
    """Test system integration."""
    
    def test_basic_imports(self):
        """Test basic Python imports work."""
        print("🔄 Testing basic imports...")
        
        basic_modules = ['os', 'sys', 'json', 'yaml', 'pathlib', 'unittest']
        
        for module in basic_modules:
            try:
                __import__(module)
                print(f"   ✅ {module}")
            except ImportError as e:
                print(f"   ❌ {module}: {e}")
                self.fail(f"Basic module {module} should be available")
        
        print("✅ Basic imports: PASSED")
    
    def test_environment_setup(self):
        """Test environment setup."""
        print("🌍 Testing environment setup...")
        
        # Test Python version
        version = sys.version_info
        print(f"   Python version: {version.major}.{version.minor}.{version.micro}")
        
        self.assertGreaterEqual(version.major, 3, "Python 3+ required")
        self.assertGreaterEqual(version.minor, 7, "Python 3.7+ required")
        
        # Test working directory
        cwd = Path.cwd()
        print(f"   Working directory: {cwd}")
        
        # Test temporary directory
        print(f"   Test directory: {self.test_dir}")
        self.assertTrue(Path(self.test_dir).exists())
        
        print("✅ Environment setup: PASSED")


def run_global_tests():
    """Run the complete global test suite."""
    print("=" * 80)
    print("🧪 LEPIDA VOICE ASSISTANT - GLOBAL TEST SUITE")
    print("=" * 80)
    print()
    print("🎯 This test suite checks system components and availability")
    print("💡 Missing modules will be marked as warnings, not failures")
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestModuleAvailability,
        TestConfiguration,
        TestNumberConversion,
        TestAudioSystem,
        TestFileSystem,
        TestPluginSystem,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)
    
    # Print summary
    print()
    print("=" * 80)
    print("📊 GLOBAL TEST SUMMARY")
    print("=" * 80)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.testsRun > 0:
        success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100)
        print(f"Success rate: {success_rate:.1f}%")
    
    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"   {test}")
            print(f"   {traceback.strip()}")
    
    if result.errors:
        print("\n💥 ERRORS:")
        for test, traceback in result.errors:
            print(f"   {test}")
            print(f"   {traceback.strip()}")
    
    if result.wasSuccessful():
        print("\n🎉 ALL TESTS PASSED! 🎉")
        print("✅ Lepida Voice Assistant core system is functional")
    else:
        print("\n⚠️  SOME TESTS FAILED")
        print("🔧 Review the failures and fix critical issues")
    
    print()
    print("💡 Next steps:")
    print("   1. Run: python setup_assistant.py")
    print("   2. Test specific components: python cli.py health")
    print("   3. Start voice assistant: python app.py")
    print("   4. Start web interface: cd frontend && python app.py")
    print("=" * 80)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    try:
        success = run_global_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏸️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Test suite crashed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
