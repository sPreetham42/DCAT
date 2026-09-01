"""Environment verification for DCAT.

Prints Python, CUDA, GPU, PyTorch and dependency status so that a reproducible
foundation can be confirmed before any experiment runs.

Usage:
    python -m dcat.scripts.env_check
    # or the console script
    dcat-env
"""

from __future__ import annotations

import platform
import sys
from dataclasses import dataclass

# Maps install-name -> import-name (optional when they already match).
_REQUIRED: dict[str, str] = {
    "numpy": "numpy",
    "scipy": "scipy",
    "pandas": "pandas",
    "polars": "polars",
    "torch": "torch",
    "transformers": "transformers",
    "timm": "timm",
    "Pillow": "PIL",
    "beautifulsoup4": "bs4",
    "lxml": "lxml",
    "hydra-core": "hydra",
    "omegaconf": "omegaconf",
    "mlflow": "mlflow",
    "optuna": "optuna",
    "dvc": "dvc",
    "pyarrow": "pyarrow",
    "scikit-learn": "sklearn",
}


@dataclass
class _ModuleStatus:
    name: str
    installed: bool
    version: str = ""


def _probe(import_name: str) -> str:
    """Return the version of a module or an empty string if missing."""
    try:
        module = __import__(import_name)
    except Exception:  # noqa: BLE001 - any import failure means not installed
        return ""
    version = getattr(module, "__version__", "")
    return str(version)


def _torch_info() -> dict[str, str]:
    """Best-effort Torch/CUDA/GPU information without crashing if absent."""
    info: dict[str, str] = {}
    try:
        import torch

        info["torch"] = torch.__version__
        info["cuda_available"] = str(torch.cuda.is_available())
        info["cuda_build"] = str(torch.version.cuda)
        if torch.cuda.is_available():
            info["gpu_name"] = torch.cuda.get_device_name(0)
            info["gpu_count"] = str(torch.cuda.device_count())
            props = torch.cuda.get_device_properties(0)
            info["gpu_memory_mb"] = f"{props.total_memory // (1024 * 1024)}"
        else:
            info["gpu_name"] = "N/A (CPU only)"
            info["gpu_count"] = "0"
            info["gpu_memory_mb"] = "0"
        info["cudnn"] = str(torch.backends.cudnn.version()) if torch.backends.cudnn.is_available() else "N/A"
    except Exception as exc:  # noqa: BLE001
        info["torch"] = f"not importable: {exc}"
        info["cuda_available"] = "False"
        info["cuda_build"] = "N/A"
        info["gpu_name"] = "N/A"
        info["gpu_count"] = "0"
        info["gpu_memory_mb"] = "0"
        info["cudnn"] = "N/A"
    return info


def _collect() -> tuple[list[_ModuleStatus], dict[str, str]]:
    statuses = [
        _ModuleStatus(name=name, installed=bool(_probe(imp)), version=_probe(imp))
        for name, imp in _REQUIRED.items()
    ]
    info = _torch_info()
    return statuses, info


def _render(statuses: list[_ModuleStatus], info: dict[str, str]) -> str:
    lines: list[str] = []
    lines.append("=" * 64)
    lines.append("DCAT Environment Verification")
    lines.append("=" * 64)

    lines.append("\n[System]")
    lines.append(f"  Python          : {platform.python_version()}  ({sys.executable})")
    lines.append(f"  Platform        : {platform.platform()}")

    lines.append("\n[Torch / CUDA / GPU]")
    lines.append(f"  PyTorch          : {info.get('torch', 'N/A')}")
    lines.append(f"  CUDA available   : {info.get('cuda_available', 'N/A')}")
    lines.append(f"  CUDA build       : {info.get('cuda_build', 'N/A')}")
    lines.append(f"  cuDNN            : {info.get('cudnn', 'N/A')}")
    lines.append(f"  GPU name         : {info.get('gpu_name', 'N/A')}")
    lines.append(f"  GPU count        : {info.get('gpu_count', 'N/A')}")
    lines.append(f"  GPU memory (MB)  : {info.get('gpu_memory_mb', 'N/A')}")

    lines.append("\n[Dependencies]")
    header = f"  {'Package':<18} {'Status':<10} Version"
    lines.append(header)
    lines.append("  " + "-" * 52)
    for status in sorted(
        statuses,
        key=lambda s: (s.installed is False, s.name.lower()),
    ):
        state = "OK" if status.installed else "MISSING"
        lines.append(f"  {status.name:<18} {state:<10} {status.version}")

    missing = [s.name for s in statuses if not s.installed]
    lines.append("\n" + "=" * 64)
    if missing:
        lines.append(f"RESULT: FAIL - {len(missing)} missing package(s): {', '.join(missing)}")
    else:
        lines.append("RESULT: PASS - all required packages present.")
    lines.append("=" * 64)
    return "\n".join(lines)


def check_environment() -> tuple[bool, str]:
    """Run the environment probe.

    Returns:
        (all_present: bool, rendered_report: str)
    """
    statuses, info = _collect()
    report = _render(statuses, info)
    all_present = all(s.installed for s in statuses)
    return all_present, report


def main() -> int:
    """Console entry point. Exits with code 0 if all deps present, else 1."""
    all_present, report = check_environment()
    print(report)
    return 0 if all_present else 1


if __name__ == "__main__":
    raise SystemExit(main())
