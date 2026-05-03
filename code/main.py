import subprocess
import sys
from pathlib import Path

def main():
    app_path = Path(__file__).resolve().parent / "ui" / "app.py"
    print(f"Launching Streamlit AI Support Agent UI...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", str(app_path)])
    except KeyboardInterrupt:
        print("\nShutting down AI Support Agent...")

if __name__ == "__main__":
    main()
