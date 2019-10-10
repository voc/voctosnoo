from distutils.core import setup

setup(
    name="voctosnoo",
    version="0.1.0",
    author="Necro",
    author_email="necro@koeln.ccc.de",
    packages=["voctosnoo"],
    include_package_data=True,
    #url="http://pypi.python.org/pypi/MyApplication_v010/",
    license="LICENSE",
    description="Useful towel-related stuff.",
    # long_description=open("README.txt").read(),
    # Dependent packages (distributions)
    install_requires=[
        "feedparser",
        "praw",
        "python-daemon"
    ],
)
