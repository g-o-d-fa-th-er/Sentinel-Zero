import os
import sys

# Add current directory to path
sys.path.append(os.getcwd())

def test_app_integrity():
    print("Verifying app.py integrity...")
    try:
        with open("app.py", "r", encoding="utf-8") as f:
            content = f.read()
            compile(content, "app.py", "exec")
        print("app.py syntax is valid.")
    except Exception as e:
        print(f"Syntax error in app.py: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_app_integrity()
