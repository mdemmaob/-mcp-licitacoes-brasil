from setuptools import setup, find_packages

setup(
    name="mcp-licitacoes-brasil",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "mcp>=0.1.0",
        "httpx>=0.25.0",
        "pydantic>=2.5.0",
        "pyyaml>=6.0.0",
        "python-dotenv>=1.0.0"
    ],
) 