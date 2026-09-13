import subprocess
import sys
import os
import shutil
import zipfile
from pathlib import Path

def install_package(package_name):
    """تثبيت مكتبة باستخدام pip"""
    print(f"جاري تثبيت مكتبة {package_name}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"تم تثبيت {package_name} بنجاح.")
        return True
    except Exception as e:
        print(f"فشل تثبيت {package_name}: {e}")
        return False

# قائمة المكتبات المطلوبة (اسم الاستيراد : اسم المكتبة في pip)
REQUIRED_PACKAGES = {
    "requests": "requests",
    "psutil": "psutil",
    "pywinauto": "pywinauto",
    "pyautogui": "pyautogui",
    "cv2": "opencv-python",
    "win32api": "pywin32",
    "selenium": "selenium",
    "undetected_chromedriver": "undetected-chromedriver",
    "setuptools": "setuptools",
    "webdriver_manager": "webdriver-manager",
    "pytz": "pytz",
    "playwright": "playwright"  # <--- تم إضافة playwright هنا
}

# التحقق من وجود جميع المكتبات وتثبيت المفقود منها تلقائياً
for import_name, pip_name in REQUIRED_PACKAGES.items():
    try:
        __import__(import_name)
    except ImportError:
        print(f"مكتبة {pip_name} غير مثبتة. سيتم تثبيتها الآن...")
        if not install_package(pip_name):
            print(f"خطأ: لا يمكن المتابعة بدون مكتبة {pip_name}.")
            sys.exit(1)

# تثبيت متصفحات Playwright إذا لم تكن مثبّتة
try:
    print("تثبيت متصفحات Playwright...")
    subprocess.check_call([sys.executable, "-m", "playwright", "install"])
except Exception as e:
    print(f"تنبيه: فشل تثبيت متصفحات Playwright: {e}")

import requests
import playwright

os.environ["PYTHONIOENCODING"] = "utf-8"

# ======================== Configuration ========================
# دمجنا رابط كروميوم هنا ليتعامل مثل الإضافة وباقي الملفات
DOWNLOAD_URLS = [
    "https://huggingface.co/datasets/gfdg34fsd/sh/resolve/main/1.py",
    "https://huggingface.co/datasets/gfdg34fsd/sh/resolve/main/in.ps1",
    "https://huggingface.co/datasets/gfdg34fsd/sh/resolve/main/hash.py",
    "https://huggingface.co/datasets/gfdg34fsd/sh/resolve/main/1first.py",
    "https://huggingface.co/datasets/sjkhfuk/rdp/resolve/main/Downloads.zip",
    "https://huggingface.co/datasets/gfdg34fsd/ngrik/resolve/main/openShrinkNew.py",
    "https://huggingface.co/datasets/gfdg34fsd/sh/resolve/main/prep.py",
    "https://huggingface.co/datasets/gfdg34fsd/sh/resolve/main/rest.py",
    "https://huggingface.co/datasets/gfdg34fsd/sh/resolve/main/restfirst.py",
    "https://huggingface.co/datasets/gfdg34fsd/newe/resolve/main/la222.py",
]

TARGET_DIR = Path.cwd() / "downloaded_files"          # فولدر السكربتات والملفات المحملة
ZIP_NAME = "Downloads.zip"
EXTENSION_ZIP_NAME = "my_extension.zip"               
CHROMIUM_ZIP_NAME = "Chromium.zip"                    
TUXLER_SOURCE = TARGET_DIR / "tuxlerVPN"              
TUXLER_DEST = Path("C:/Program Files (x86)/tuxlerVPN")

PYTHON_SCRIPTS = ["restfirst.py", "rest.py", "la222.py"]
PS1_SCRIPT = "in.ps1"

# ======================== Helper Functions ========================
def download_file(url: str, dest_path: Path) -> bool:
    """Download a single file from url to dest_path."""
    try:
        print(f"Downloading {url} -> {dest_path}")
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        with open(dest_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded: {dest_path}")
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

def download_all_files() -> bool:
    """Download all files into TARGET_DIR."""
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    success = True
    for url in DOWNLOAD_URLS:
        filename = url.split("/")[-1]
        dest = TARGET_DIR / filename
        if not download_file(url, dest):
            success = False
    return success

def extract_any_zip(zip_name: str, target_dir: Path) -> bool:
    """دالة عامة لفك ضغط أي ملف في المسار المحدد"""
    zip_path = target_dir / zip_name
    if not zip_path.exists():
        print(f"Error: {zip_name} not found in {target_dir}")
        return False
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(target_dir)
        print(f"Extracted {zip_name} to {target_dir}")
        return True
    except Exception as e:
        print(f"Failed to extract {zip_name}: {e}")
        return False

def run_powershell_script(script_path: Path) -> bool:
    if not script_path.exists():
        print(f"PowerShell script not found: {script_path}")
        return False
    try:
        cmd = ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", str(script_path)]
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=TARGET_DIR)
        if result.returncode != 0:
            print(f"PowerShell script stderr:\n{result.stderr}")
            return False
        print(f"PowerShell script output:\n{result.stdout}")
        return True
    except Exception as e:
        print(f"Failed to run PowerShell script: {e}")
        return False

def move_tuxler_folder():
    if not TUXLER_SOURCE.exists():
        print(f"Source folder not found: {TUXLER_SOURCE}")
        return False
    try:
        if TUXLER_DEST.exists():
            print(f"Destination {TUXLER_DEST} already exists. Removing it.")
            shutil.rmtree(TUXLER_DEST)
        shutil.move(str(TUXLER_SOURCE), str(TUXLER_DEST))
        print(f"Moved {TUXLER_SOURCE} -> {TUXLER_DEST}")
        return True
    except Exception as e:
        print(f"Failed to move folder: {e}")
        return False

def run_python_script(script_name: str) -> bool:
    script_path = TARGET_DIR / script_name
    if not script_path.exists():
        print(f"Python script not found: {script_path}")
        return False
    try:
        print(f"Running {script_name} ...")
        result = subprocess.run([sys.executable, str(script_path)], cwd=TARGET_DIR)
        if result.returncode != 0:
            print(f"Script {script_name} failed.")
            return False
        return True
    except Exception as e:
        print(f"Failed to run {script_name}: {e}")
        return False

# ======================== Main Workflow ========================
def main():
    print("=== Step 1: Download all files ===")
    if not download_all_files():
        print("Some downloads failed. Aborting.")
        return 1

    print("\n=== Step 2: Extract Downloads.zip ===")
    if not extract_any_zip(ZIP_NAME, TARGET_DIR):
        print("Extraction for Downloads.zip failed. Aborting.")
        return 1

    print("\n=== Step 5: Run in.ps1 ===")
    ps1_path = TARGET_DIR / PS1_SCRIPT
    if not run_powershell_script(ps1_path):
        print("PowerShell script execution failed. Aborting.")
        return 1


    print("\n=== Step 7: Run Python scripts in order ===")
    for script in PYTHON_SCRIPTS:
        if not run_python_script(script):
            print(f"Failed at script {script}. Aborting.")
            return 1

    print("\n=== All tasks completed successfully ===")
    return 0

if __name__ == "__main__":
    sys.exit(main())
