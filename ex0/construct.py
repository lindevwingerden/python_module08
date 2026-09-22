import sys
import site


def check_python() -> str:
    return f"Current Python: {sys.executable}"


def outside_venv() -> None:
    print("\nMATRIX STATUS: You're still plugged in")
    print(f"\n{check_python()}")
    print("Virtual Environment: None detected")
    print("\nWARNING: You're in the global environment!")
    print("The machines can see everything you install.")
    print("\nTo enter the construct, run:")
    print("python3 -m venv matrix_env")
    print("source matrix_env/bin/activate # On Unix")
    print("matrix_env\\Scripts\\activate # On Windows")
    print("\nThen run this program again.")


def inside_venv() -> None:
    print("\nMATRIX STATUS: Welcome to the construct")
    print(f"\n{check_python()}")
    path = sys.prefix
    venv = path.split("/")[-1]
    print(f"Virtual Environment: {venv}")
    print(f"Environment Path: {path}")
    print("\nSUCCESS: You're in an isolated environment!")
    print("Safe to install packages without affecting the global system.")
    print("\nPackage installation path:")
    print(site.getsitepackages()[0])


if __name__ == "__main__":
    if sys.prefix != sys.base_prefix:
        inside_venv()
    else:
        outside_venv()
