# 📋 Setup Logging Guide

## 🎯 Overview
The Lepida Voice Assistant setup system now includes comprehensive logging for all setup activities. This helps with debugging, monitoring, and troubleshooting setup issues.

## 🔧 Logging Features

### ✅ Automatic Logging
- **All setup modes** automatically create detailed logs
- **Timestamped log files** with unique names for each setup session
- **Dual output**: Logs appear both in console and log files
- **Error tracking**: Detailed error information with stack traces
- **Performance monitoring**: Execution time for each setup step

### 📁 Log File Location
```
logs/
├── setup_YYYYMMDD_HHMMSS.log    # Main setup log with timestamp
└── setup_error.log               # Error-only log (legacy)
```

### 📊 Log Information Captured

#### System Information
- Python version and platform details
- Working directory and environment
- System architecture and OS version
- Available disk space and memory
- Internet connectivity status

#### Setup Process
- Each setup step with start/completion status
- Execution time for each step
- Success/failure status with details
- Error messages with solutions
- Recovery suggestions

#### Error Details
- Full error messages and stack traces
- Error codes for easy reference
- Step-by-step troubleshooting guidance
- Recovery mode suggestions

## 🚀 Usage Examples

### Basic Setup with Logging
```bash
# Full setup (creates logs/setup_YYYYMMDD_HHMMSS.log)
python setup_assistant.py

# Quick setup with logging
python setup_assistant.py --quick

# Frontend setup with logging
python setup_assistant.py --frontend

# Recovery mode with logging
python setup_assistant.py --recovery
```

### Log File Analysis
```bash
# View latest setup log
ls -la logs/setup_*.log | tail -1

# Monitor real-time logging (Linux/Mac)
tail -f logs/setup_$(date +%Y%m%d)_*.log

# Search for errors in logs
grep "ERROR" logs/setup_*.log

# Search for specific step
grep "virtual environment" logs/setup_*.log
```

## 📋 Log Levels

### INFO Level
- Setup progress and status updates
- System information and configuration
- Successful completion of steps
- Performance metrics

### WARNING Level
- Non-critical issues that don't stop setup
- Missing optional dependencies
- Configuration warnings
- Recovery suggestions

### ERROR Level
- Setup step failures
- Critical system issues
- Installation problems
- Detailed error information with solutions

### CRITICAL Level
- Fatal setup errors
- System incompatibility issues
- Complete setup failures

## 🔍 Reading Log Files

### Log Entry Format
```
2025-07-25 10:18:09,365 - INFO - Setup started at: 2025-07-25 10:18:09.365252
2025-07-25 10:18:09,384 - INFO - 🔄 STARTING: Checking Python version
2025-07-25 10:18:09,385 - INFO - ✅ SUCCESS: Checking Python version (executed in 0.00s)
```

### Key Log Sections
1. **Setup Header**: System information and session details
2. **Prerequisites Check**: System compatibility validation
3. **Setup Steps**: Individual component installation/configuration
4. **Error Details**: Failure information with recovery guidance
5. **Summary**: Final status and next steps

## 🛠️ Troubleshooting with Logs

### Finding Setup Issues
```bash
# Check for failed steps
grep "❌ ERROR\|FAILED" logs/setup_*.log

# View error codes
grep "Error Code:" logs/setup_*.log

# Check execution times
grep "executed in" logs/setup_*.log
```

### Common Log Patterns

#### Successful Setup
```
INFO - ✅ SUCCESS: Step Name (executed in X.XXs)
INFO - Setup completed. Failed steps: 0
```

#### Failed Setup
```
ERROR - ❌ ERROR: Step Name - Error description
ERROR - Error Code: ERROR_CODE
INFO - Recovery suggestion: Solution description
```

#### System Issues
```
WARNING - ⚠️ WARNING: Prerequisites - Issue description
INFO - System Information: detailed_info
```

## 🔧 Log Management

### Automatic Cleanup
The setup system automatically manages log files:
- Creates timestamped logs for each session
- Preserves historical setup attempts
- No automatic deletion (manual cleanup required)

### Manual Cleanup
```bash
# Remove logs older than 7 days (Linux/Mac)
find logs/ -name "setup_*.log" -mtime +7 -delete

# Keep only last 5 setup logs (Linux/Mac)
ls -t logs/setup_*.log | tail -n +6 | xargs rm -f

# Windows cleanup (PowerShell)
Get-ChildItem logs\setup_*.log | Sort-Object LastWriteTime -Descending | Select-Object -Skip 5 | Remove-Item
```

## 📈 Benefits

### For Users
- **Easy troubleshooting**: Clear error messages with solutions
- **Progress tracking**: See exactly what's happening during setup
- **Historical record**: Review past setup attempts
- **Support assistance**: Share logs for technical support

### For Developers
- **Debug information**: Detailed execution flow and timing
- **Error patterns**: Identify common failure points
- **Performance monitoring**: Optimize slow setup steps
- **User experience**: Improve setup process based on log data

## 🎯 Best Practices

### When to Check Logs
- ✅ After any setup failure
- ✅ When setup takes longer than expected
- ✅ Before reporting issues or requesting support
- ✅ When troubleshooting system compatibility

### Sharing Logs for Support
When requesting help:
1. Include the complete log file from latest setup attempt
2. Mention your operating system and Python version
3. Describe what you were trying to achieve
4. Include any error codes from the log

### Log Security
- ✅ Logs contain system information but no sensitive data
- ✅ Safe to share for troubleshooting purposes
- ✅ No API keys or passwords are logged
- ⚠️ May contain file paths and system configuration

## 🔄 Integration

The logging system integrates with:
- **Error Handling**: All errors are logged with detailed context
- **Recovery Mode**: Logs recovery attempts and results
- **Health Checks**: Performance and system status logging
- **Plugin Validation**: Component-specific logging

## 📞 Support

If you encounter issues with the logging system:
1. Check if `logs/` directory exists and is writable
2. Verify Python logging module is available
3. Try running with `--recovery` mode
4. Check console output for logging-related errors

For technical support, please include:
- Your operating system and version
- Python version (`python --version`)
- Complete log file from latest setup attempt
- Description of the issue you're experiencing
