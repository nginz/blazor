from distutils.core import setup

setup(
    name='Blazor',
    version='0.1.2',
    author='Moustafa Badawy',
    author_email='moustafa.badawym@gmail.com',
    packages=['blazor'],
    url='http://pypi.python.org/pypi/Blazor/',
    license='LICENSE.txt',
    description='Voci V-Blaze Natural Language Processor.',
    long_description=open('README.md').read(),
    install_requires=[
        "pyyaml",
        "nltk",
        "simplejson"
    ],
)