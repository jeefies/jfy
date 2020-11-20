from setuptools import setup

with open('requirements.txt') as f:
    deps = tuple(map(lambda x : x.strip(), f.read().split()))

with open('README.md') as f:
    long_des = f.read()

setup(
        name = 'dependences',
        pacakges = ['dps'],
        version = '0.0.1',
        url = 'https://github.com/jeefies/jfy',
        description = 'dependecs for jfy web'
        author = 'jeefy',
        author_email = 'jeefy163@163.com',
        long_description = long_des,
        python_requires = '>3.4',
        package_data = {'': ['*.go', '*.so', '*.dll']},
        long_description_content_type = 'text/markdown',
        install_requires = deps
        )
