from distutils.core import setup

setup(
    name='sakailib',
    version='v1.0.3',
    packages=['sakailib'],
    install_requires=[
        'bs4',
        'html5lib'
    ],
    url='https://github.com/cubicpill/sakai_lib',
    license='GPL v3.0',
    author='CubicPill',
    author_email='cubicpill@gmail.com',
    description='A wrapper for Sakai site @SUSTech'
)
