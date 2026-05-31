from setuptools import setup, find_namespace_packages

setup(
    name="wppull-agent",
    version="0.1.0",
    description="WordPress REST API content extractor for static-site migration — pulls posts, pages, and media to Markdown. By tehkimguan.com.",
    long_description=open("../README.md").read() if __import__("os").path.exists("../README.md") else "",
    long_description_content_type="text/markdown",
    author="Teh Kim Guan",
    author_email="kimguan.teh@outlook.com",
    url="https://github.com/tehkimguan/my-website-agent",
    packages=find_namespace_packages(include=["kg_cli.*"]),
    install_requires=[
        "click>=8.0.0",
        "requests>=2.28.0",
    ],
    entry_points={
        "console_scripts": [
            "wppull=kg_cli.wppull.wppull_cli:main",
        ],
    },
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
    ],
)
