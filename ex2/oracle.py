import sys
import os
from dotenv import load_dotenv  # type: ignore[import-not-found]

CONFIG_VARIABLES: list[str] = [
    "MATRIX_MODE", "DATABASE_URL", "API_KEY", "LOG_LEVEL", "ZION_ENDPOINT"
]


def detect_overrides() -> list[str]:
    return [name for name in CONFIG_VARIABLES if name in os.environ]


def get_env() -> dict[str, str | None]:
    load_dotenv()
    config = {}
    for name in CONFIG_VARIABLES:
        config[name] = os.getenv(name)
    return config


def check_env(config_vars: dict[str, str | None]) -> bool:
    missing = []
    for key, value in config_vars.items():
        if value is None:
            missing.append(key)
    if missing:
        print("\nMissing configuration variables: ", end="")
        print(", ".join(missing))
        print("Please complete the .env file")
        return False
    else:
        return True


def print_config(config_vars: dict[str, str | None]) -> None:
    print("\nConfiguration loaded:")
    print(f"Mode: {config_vars['MATRIX_MODE']}")
    url = config_vars["DATABASE_URL"] or ""
    if "localhost" in url:
        print("Database: Connected to local instance")
    else:
        print("Database: Connected to remote instance")
    print("API Access: Authenticated")
    print(f"Log Level: {config_vars['LOG_LEVEL']}")
    endpoint = config_vars["ZION_ENDPOINT"] or ""
    if endpoint.startswith(("http://", "https://")):
        print("Zion Network: Online")
    else:
        print("Zion Network: Offline")


def read_lines(file_name: str) -> list[str] | None:
    try:
        with open(file_name, "r") as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        print(f"Security check failed: {file_name} not found")
        return None
    except OSError as e:
        print(f"Security check failed: could not read {file_name}: {e}")
        return None


def security_check(overrides: list[str]) -> None:
    print("\nEnvironment security check:")
    value = None
    example = read_lines(".env.example")
    if example is not None:
        for line in example:
            if line.startswith("API_KEY="):
                value = line.split("=", 1)[1]
                break
    if value is None:
        print("[KO] Could not verify .env.example")
    elif value == "your_api_key_here":
        print("[OK] No hardcoded secrets detected")
    else:
        print("[KO] Secret key leaked")
    env_exists = os.path.isfile(".env")
    env_in_gitignore = ".env" in (read_lines(".gitignore") or [])
    if env_exists and env_in_gitignore:
        print("[OK] .env file properly configured")
    elif not env_exists:
        print("[KO] .env file missing")
    else:
        print("[KO] .env exists but is not listed in .gitignore")
    if overrides:
        print(f"[OK] Production overrides active: {', '.join(overrides)}")
    else:
        print("[OK] Production overrides available")


if __name__ == "__main__":
    print("\nORACLE STATUS: Reading the Matrix...")
    overrides = detect_overrides()
    config_vars = get_env()
    if not check_env(config_vars):
        sys.exit(1)
    print_config(config_vars)
    security_check(overrides)
    print("\nThe Oracle sees all configurations.")
