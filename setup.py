from distutils.core import setup

setup(
    name='Blazor',
    version='2.0.1',
    author='Moustafa Badawy',
    author_email='moustafa.badawym@gmail.com',
    packages=['blazor'],
    url='http://pypi.python.org/pypi/Blazor/',
    license='LICENSE.txt',
    description='Voci V-Blaze Natural Language Processor.',
    long_description=open('README.md').read(),
    install_requires=[
        "nltk"
    ],
)