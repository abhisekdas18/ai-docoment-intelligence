import subprocess
import sys
import os

ROOT = os.path.dirname(__file__)
SRC = os.path.join(ROOT, "src")

def run(script_name):
    path = os.path.join(SRC, script_name)
    print("="*60)
    print(f"Running {script_name}")
    print("="*60)
    result = subprocess.run([sys.executable, path], capture_output=False)
    if result.returncode != 0:
        print(f"❌ Script {script_name} failed with code {result.returncode}")
        sys.exit(result.returncode)
    print(f"✅ Completed {script_name}\n")

if __name__ == "__main__":
    run("ocr_extraction.py")
    run("text_preprocessing.py")
    run("field_extraction.py")
    print("\n🎯 All steps completed successfully!")
