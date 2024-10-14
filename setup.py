from setuptools import setup, find_packages

setup(
    name='AutoRetweet',
    version='0.1.0',
    description='A Python package for automatically retweeting based on certain criteria.',
    author='Razif Rizqullah', 
    author_email='razifrizqullah@example.com',
    url='https://github.com/rizquuula',
    packages=find_packages(),
    install_requires=[
        'certifi==2024.8.30',
        'charset-normalizer==3.4.0',
        'idna==3.10',
        'oauthlib==3.2.2',
        'python-dotenv==1.0.1',
        'requests==2.32.3',
        'requests-oauthlib==2.0.0',
        'urllib3==2.2.3'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
