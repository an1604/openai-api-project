from setuptools import setup, find_packages

setup(
    name='tool_chatbot',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # list of required packages
    ],
)

import os
os.makedirs("logs", exist_ok=True)
