from setuptools import setup, find_packages

setup(
    name="crmproject",
    version="0.1",
    packages=find_packages(),
    package_dir={'': '.'},  # Explicitly look in current directory
    python_requires='>=3.6',
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'flask-login'
    ],
)