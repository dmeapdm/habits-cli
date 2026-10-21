import habits


def test_package_is_importable():
    assert habits.__name__ == "habits"


def test_package_exposes_version():
    assert habits.__version__
