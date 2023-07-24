from setuptools import setup, find_packages

# Read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='alpypeopt',
      version='0.0.1',
      license='Apache License, Version 2.0',
      author='Marc Escandell Mari',
      author_email='marcescandellmari@gmail.com',
      description='An open source library for connecting AnyLogic models with python-based sequential optimization packages',
      long_description=long_description,
      long_description_content_type="text/markdown",
      python_requires='>=3.9',
      packages=find_packages(),
      url='https://github.com/MarcEscandell/ALPypeOpt',
      keywords='alpypeopt',
      install_requires=[
            'py4j'
      ]
)