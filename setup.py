"""Packaging settings."""


from codecs import open
from os.path import dirname, join
from subprocess import call
from setuptools import Command, find_packages, setup
from unitmulti import __version__ as VERSION
from unitmulti import __release__ as RELEASE


def read(fname):
    return open(join(dirname(__file__), fname)).read()


class RunTests(Command):
    """Run all tests."""

    description = "run tests"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        errno = call(
            [
                "py.test",
                "--verbose",
                "--cov=unitmulti",
                "--cov-report=term-missing",
                "--cov-config=.coveragerc",
                "--junitxml=.junit.xml",
            ]
        )
        raise SystemExit(errno)


setup(
    name="unitmulti",
    version=VERSION + "." + RELEASE,
    description="Dummy Project",
    long_description=read("README.md"),
    url="https://github.com/tecnickcom/unitmulti",
    author="Tecnick.com LTD",
    author_email="info@tecnick.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: MIT",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
    ],
    keywords="unitmulti",
    packages=find_packages(exclude=["docs", "test*"]),
    data_files=[("info", ["VERSION", "RELEASE", "LICENSE", "README.md"])],
    install_requires=[],
    extras_require={
        "test": [
            "coverage",
            "pytest",
            "pytest-benchmark",
            "pytest-cov",
            "pycodestyle",
            "pylint",
            "pyflakes",
            "black",
        ]
    },
    cmdclass={"test": RunTests},
)
