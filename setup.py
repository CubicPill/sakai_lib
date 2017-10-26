from setuptools import setup, find_packages

setup(
    name='sakailib',
    version='v1.0.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'BeautifulSoup4',
        'html5lib'
    ],
    url='https://github.com/cubicpill/sakai_lib',
    license='GPL v3.0',
    author='CubicPill',
    author_email='cubicpill@gmail.com',
    description='A wrapper for Sakai site @SUSTech'
)
