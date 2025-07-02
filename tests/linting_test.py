import subprocess


def test_flake8():
    """Test flake8 linting on musculation/"""
    result = subprocess.run(["flake8", "musculation/"], capture_output=True, text=True)
    print(result.stdout)
    assert result.returncode == 0, f"Flake8 found issues:\n{result.stdout}"


def test_pylint():
    """Test pylint on musculation/"""
    result = subprocess.run(["pylint", "musculation/"], capture_output=True, text=True)
    print(result.stdout)
    assert result.returncode == 0, f"Pylint found issues:\n{result.stdout}"
