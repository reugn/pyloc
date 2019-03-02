import pytest

# flake8: noqa
from pyloc import *


@pytest.fixture(scope="module")
def wd(request):
    return request.fspath.join('..')


def test_ext_c(wd):
    source_file = wd.join("resources/config.c")
    assert (FileHandler(source_file).handle()
            == FileDetails(ext='c', n=1, comment=24, code=70, blank=21))


def test_ext_py(wd):
    source_file = wd.join("resources/abc.py")
    assert (FileHandler(source_file).handle()
            == FileDetails(ext='py', n=1, comment=103, code=98, blank=48))
