import os
import importlib.util
import sys

from pkg_resources import parse_requirements
from setuptools import find_packages, setup

module_name = 'enrollment'

# Возможно, модуль еще не установлен (или установлена другая версия), поэтому
# необходимо загружать __init__.py с помощью machinery.

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
    # long_description=open('README.rst').read(),
    # url='https://github.com/alvassin/backendschool2019',
    # platforms='all',
    # classifiers=[
    #     'Intended Audience :: Developers',
    #     'Natural Language :: Russian',
    #     'Operating System :: MacOS',
    #     'Operating System :: POSIX',
    #     'Programming Language :: Python',
    #     'Programming Language :: Python :: 3',
    #     'Programming Language :: Python :: 3.8',
    #     'Programming Language :: Python :: Implementation :: CPython'
    # ],
    python_requires='>=3.8',
    # packages=find_packages(exclude=['tests']),
    install_requires=load_requirements('requirements.txt'),
    # extras_require={'dev': load_requirements('requirements.txt.dev.txt')},
    # entry_points={
    #     'console_scripts': [
    #         # f-strings в setup.py не используются из-за соображений
    #         # совместимости.
    #         # Несмотря на то, что этот пакет требует Python 3.8, технически
    #         # source distribution для него может собираться с помощью более
    #         # ранних версий Python. Не стоит лишать пользователей этой
    #         # возможности.
    #         '{0}-api = {0}.api.__main__:main'.format(module_name),
    #         '{0}-db = {0}.db.__main__:main'.format(module_name)
    #     ]
    # },
    # include_package_data=True
    scripts=['app/main.py']
)
