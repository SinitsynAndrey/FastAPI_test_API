import importlib.util
import sys

from pkg_resources import parse_requirements
from setuptools import setup

module_name = 'enrollment'


spec = importlib.util.spec_from_file_location(module_name, '__init__.py')
module = importlib.util.module_from_spec(spec)
sys.modules[module_name] = module
spec.loader.exec_module(module)


def load_requirements(fname: str) -> list:
    requirements = []
    with open(fname, 'r') as f:
        for req in parse_requirements(f.read()):
            requirements.append(f'{req.name}{req.specifier}')
    return requirements


setup(
    name=module_name,
    version='0.0.1',
    author='Andrey Sinitsyn',
    author_email='andrey-sin@yandex.ru',
    description=module.__doc__,
    python_requires='>=3.8',
    install_requires=load_requirements('requirements.txt'),
    scripts=['core/main.py']
)
