from setuptools import setup, find_packages

setup(
    name="noted",
    version="0.1",
    author="Osman Mesut Ozcan",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn[standard]",
        "databases",
        "sqlalchemy",
        "aiosqlite",
        "typer",
    ],
    entry_points={
        "console_scripts": [
            "noted=noted.cli:main",
        ],
    },
)
