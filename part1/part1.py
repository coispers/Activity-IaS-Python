import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Runs scripts sequentially (not simultaneously).
SCRIPTS_IN_ORDER = [
    "admin_login_test.py",
    "employee_login_test.py",
    "file_access_test.py",
    "file_access_verbose.py",
]


def wait_for_user(script_name: str) -> bool:
    prompt = f"Press Enter to continue to {script_name} (or type q to quit): "
    user_input = input(prompt).strip().lower()
    return user_input != "q"


def run_script(script_name: str) -> bool:
    script_path = BASE_DIR / script_name

    if not script_path.exists():
        print(f"[SKIP] {script_name} not found.")
        return False

    print(f"\n=== Running {script_name} ===")
    try:
        subprocess.run([sys.executable, str(script_path)], check=True)
        print(f"=== Finished {script_name} (OK) ===")
        return True
    except subprocess.CalledProcessError as e:
        print(f"=== Finished {script_name} (FAILED: exit code {e.returncode}) ===")
        return False


def main():
    print("Part 1 IaS sequential runner started.")

    for script in SCRIPTS_IN_ORDER:
        if not wait_for_user(script):
            print("Stopped by user.")
            break

        ok = run_script(script)
        if not ok:
            print("Continuing to next step.")


if __name__ == "__main__":
    main()
