"""Smoke test: oks_connector core imports cleanly after namespace migration.

extractors/web.py 顶层 import trafilatura（可选依赖），不在此测；各提取器
的第三方依赖应是延迟 import，由具体路由触发。
"""
import subprocess
import sys


def test_core_imports():
    import oks_connector
    import oks_connector.raw_bundle_adapter as rba
    import oks_connector.route
    import oks_connector.validator
    import oks_connector.network
    import oks_connector._shared
    import oks_connector.constants
    assert hasattr(rba, "build_parser")
    assert hasattr(rba, "main")


def test_cli_help_runs():
    proc = subprocess.run(
        [sys.executable, "-m", "oks_connector.raw_bundle_adapter", "--help"],
        capture_output=True, text=True, check=False,
    )
    assert proc.returncode == 0, proc.stderr
    assert "usage" in proc.stdout.lower()
