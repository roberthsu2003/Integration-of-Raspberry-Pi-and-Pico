"""
環境驗證工具
檢查課程所需的所有軟體和服務
"""

import sys
import subprocess
import os

def print_header(text):
    print("\n" + "=" * 60)
    print(f" {text}")
    print("=" * 60)

def check_python():
    """檢查 Python 版本"""
    version = sys.version.split()[0]
    major, minor = map(int, version.split('.')[:2])
    
    if major >= 3 and minor >= 9:
        print(f"✓ Python {version}")
        return True
    else:
        print(f"✗ Python {version} (需要 3.9+)")
        return False

def check_command(command, name):
    """檢查命令是否可用"""
    try:
        result = subprocess.run(
            [command, '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"✓ {name}: {version}")
            return True
        else:
            print(f"✗ {name}: 未安裝")
            return False
    except FileNotFoundError:
        print(f"✗ {name}: 未安裝")
        return False
    except Exception as e:
        print(f"✗ {name}: {e}")
        return False

def check_docker_services():
    """檢查 Docker 服務"""
    try:
        result = subprocess.run(
            ['docker', 'ps'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if 'mongodb' in result.stdout:
            print("✓ MongoDB 容器運行中")
        else:
            print("✗ MongoDB 容器未運行")
        
        if 'mosquitto' in result.stdout:
            print("✓ Mosquitto 容器運行中")
        else:
            print("✗ Mosquitto 容器未運行")
        
        return True
    except Exception as e:
        print(f"✗ Docker 服務檢查失敗: {e}")
        return False

def check_python_packages():
    """檢查 Python 套件"""
    packages = [
        'fastapi',
        'uvicorn',
        'pymongo',
        'paho-mqtt',
        'pyserial'
    ]
    
    all_installed = True
    for package in packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package}: 未安裝")
            all_installed = False
    
    return all_installed

def main():
    print_header("環境驗證工具")
    
    results = []
    
    # 檢查 Python
    print_header("Python 環境")
    results.append(("Python", check_python()))
    
    # 檢查系統工具
    print_header("系統工具")
    results.append(("Docker", check_command('docker', 'Docker')))
    results.append(("Docker Compose", check_command('docker-compose', 'Docker Compose')))
    results.append(("Git", check_command('git', 'Git')))
    
    # 檢查 Python 套件
    print_header("Python 套件")
    results.append(("Python 套件", check_python_packages()))
    
    # 檢查 Docker 服務
    print_header("Docker 服務")
    results.append(("Docker 服務", check_docker_services()))
    
    # 總結
    print_header("驗證結果")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\n通過: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 所有檢查通過！環境設定完成。")
        return 0
    else:
        print("\n⚠️  部分檢查未通過，請參考 SETUP.md 完成設定。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
