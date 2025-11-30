from setuptools import setup, find_packages # type: ignore

HYPHEN_E_DOT = '-e .'
from typing import List

def get_requirements(file_path: str) -> List[str]:

    with open(file_path) as file:
        requirements = file.readlines()
        requirements = [req.strip() for req in requirements if req.strip()]
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    return requirements

setup(   name='mlproject',
    version='0.0.1',
    author='Shadat Hossain',
    author_email='sahadat137839@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')

)