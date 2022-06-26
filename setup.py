from setuptools import setup
import os

# setting root folder path
HERE = os.path.dirname(os.path.abspath(__file__))
with open("root.env", "w") as f:
    f.write(f"ROOT = '{HERE}'")

def parse_requirements(file_content):
    lines = file_content.splitlines()
    return [line.strip() for line in lines if line and not line.startswith("#")]

with open(os.path.join(HERE, "requirements.txt")) as f:
    requirements = parse_requirements(f.read())

setup(
    name='cte',
    packages=['cte'],
    package_dir={'cte': 'src'},
    description='Contextualized Table Extraction',
    author='Andrea Gemelli, Emanuele Vivoli',
    license='MIT',
    keywords="document analysis, dataset",
    python_requires=">=3.7",
    install_requires=requirements,
)
