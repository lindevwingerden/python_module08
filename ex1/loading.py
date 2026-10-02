import importlib.metadata
import importlib.util
import sys

try:
    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
except ImportError:
    pass

DEPENDENCIES: dict[str, str] = {
    "pandas": "Data manipulation ready",
    "numpy": "Numerical computation ready",
    "matplotlib": "Visualization ready",
}

DISTRICTS: tuple[str, ...] = (
    "Centrum", "Nieuw-West", "Noord", "Oost", "West",
    "Zuid", "Zuidoost"
)
PREVALENCE: tuple[float, ...] = (
    0.35, 0.10, 0.10, 0.12, 0.12,
    0.13, 0.08
)
SIGHTINGS: int = 1000
SEED: int | None = None
OUTPUT_FILE: str = "matrix_analysis.png"


def check_dependencies() -> dict[str, str | None]:
    found: dict[str, str | None] = {}
    for name in DEPENDENCIES:
        if importlib.util.find_spec(name) is None:
            found[name] = None
            continue
        try:
            found[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            found[name] = "unknown"
    return found


def report(versions: dict[str, str | None]) -> list[str]:
    missing: list[str] = []
    print("Checking dependencies:")
    for name, description in DEPENDENCIES.items():
        version = versions[name]
        if version is None:
            print(f"[KO] {name} - MISSING")
            missing.append(name)
        else:
            print(f"[OK] {name} ({version}) - {description}")
    return missing


def print_install_help(missing: list[str]) -> None:
    print("\nERROR: missing dependencies:", ", ".join(missing))
    print("\nInstallation instructions for pip:")
    print("  python3 -m venv matrix_env")
    print("  source matrix_env/bin/activate")
    print("  pip install -r requirements.txt")
    print("\nInstallation instructions for Poetry:")
    print("  poetry install")
    print("  poetry run python loading.py")


def simulate_vampire_sightings() -> "pd.DataFrame":
    rng = np.random.default_rng(SEED)
    district = rng.choice(DISTRICTS, size=SIGHTINGS, p=PREVALENCE)
    hour = rng.normal(loc=0.0, scale=2.5, size=SIGHTINGS) % 24
    threat = rng.integers(low=1, high=6, size=SIGHTINGS)
    return pd.DataFrame({
        "district": district,
        "hour": hour,
        "threat": threat,
    })


def analyse_vampire_sightings(data: "pd.DataFrame") -> "pd.DataFrame":
    summary = data.groupby("district").agg(
        sightings=("district", "size"),
        mean_threat=("threat", "mean"),
    )
    return summary.sort_values("sightings", ascending=False)


def visualise_sightings(data: "pd.DataFrame", summary: "pd.DataFrame") -> None:
    matplotlib.use("Agg")
    fig, (left, right) = plt.subplots(1, 2, figsize=(13, 5))

    left.bar(summary.index, summary["sightings"], color="darkred")
    left.set_title("Vampire sightings per district")
    left.set_ylabel("Sightings")
    left.tick_params(axis="x", rotation=45)

    right.hist(data["hour"], bins=24, color="darkslateblue")
    right.set_title("Sightings per hour")
    right.set_xlabel("Hour of the day")
    right.set_ylabel("Sightings")

    fig.tight_layout()
    fig.savefig(OUTPUT_FILE, dpi=150)
    plt.close(fig)


def main() -> None:
    print("LOADING STATUS: Loading programs...\n")
    versions = check_dependencies()
    missing = report(versions)
    if missing:
        print_install_help(missing)
        sys.exit(1)
    print("\nAnalyzing Matrix data...")
    data = simulate_vampire_sightings()
    print(f"Processing {len(data)} data points...\n")
    summary = analyse_vampire_sightings(data)
    print(summary.to_string())
    print("\nGenerating visualization...")
    visualise_sightings(data, summary)
    print(f"\nAnalysis complete!\nResults saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
