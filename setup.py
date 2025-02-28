from setuptools import setup, find_packages

setup(
    name="rbgen",
    version="0.1.0",
    author='spa-dev',
    description="Random background generator for transparent images.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[ 
        "Pillow>=9.0.0",
        "numpy>=1.20.0",
        "scipy>=1.7.0"
    ],
    python_requires=">=3.8",
    entry_points={
    "console_scripts": [
        "rbgen=rbgen.main:main",
        ],
    },
)
