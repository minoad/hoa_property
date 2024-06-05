import pytest

from hoa_property import config


def test_config():
    # Validate the Config attributes
    assert config.PROJECT_NAME == 'hoa_property', "PROJECT_NAME does not match the environment variable"
    assert config.ENVIRONMENT == 'dev', "ENVIRONMENT does not match the environment variable"


if __name__ == "__main__":
    pytest.main()
