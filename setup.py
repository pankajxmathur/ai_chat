from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = [
        line.strip() for line in f.readlines()
        if line.strip() and not line.strip().startswith("#")
    ]

# get version from __version__ variable in ai_mcp_chat/__init__.py
from ai_mcp_chat import __version__ as version

setup(
    name="ai_mcp_chat",
    version=version,
    description="AI Chat interface with MCP support for Frappe",
    author="Pankaj Mathur",
    author_email="your.email@example.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)
