from setuptools import setup, find_packages

setup(
    name="quick-design",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "mcp>=1.0.0",
        "google-generativeai==0.8.3",
        "python-dotenv==1.0.1",
        "httpx>=0.27.0",
        "python-pptx==0.6.23",
    ],
    entry_points={
        "console_scripts": [
            "quick-design=src.server:main",
        ],
    },
    python_requires=">=3.10",
)
