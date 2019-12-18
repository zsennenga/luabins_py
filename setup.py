import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='luabins_py',
    version='1.0.0',
    packages=['luabins'],
    url='https://github.com/zsennenga/luabins_py',
    license='MIT License',
    author='Zach Ennenga',
    author_email='astrozees@gmail.com',
    description='A library to encode/decode luabins serialized data in python',
    long_description=long_description,
    long_description_content_type='text/markdown',
)
