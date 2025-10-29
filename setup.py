from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="django-language-manager",
    version="1.0.0",
    author="Muhammad Inaam",
    author_email="your.email@example.com",
    description="A plug-and-play Django app for multilingual websites with URL-based language switching and RTL support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Muhammadinaam/django-language-manager",
    packages=['language_manager'],
    package_dir={'language_manager': '.'},
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Internationalization",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Django>=3.2",
        "polib>=1.1.0",
    ],
    keywords="django i18n internationalization multilingual rtl arabic urdu language-switching translations",
)

