from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder',
    version='0.0.1',
    description='Clean code',
    author='Anastasiia Makarova',
    author_email='amakarova121@gmail.com',
    license='MIT',
    packages=find_namespace_packages(),
    #include_package_data=True
    entry_points={'console_scripts': ['clean-folder=clean_folder.clean:main']}
)