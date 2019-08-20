from setuptools import find_packages, setup

with open('requirements.txt', 'r') as req:
    install_requires = req.read().split("\n")

setup(
    name='zhengli',
    packages=find_packages(),
    version='0.0.1',
    description='a library that organizes books for you',
    author='Sarah Hudspeth, Dingchao Zhang',
    install_requires=install_requires,
    python_requires='>=3.7.4',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
