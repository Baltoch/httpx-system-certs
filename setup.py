from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="httpx_system_certs",
    version="1.0.0",
    description="Patch httpx to use system certificates authority bundles by default",
    long_description=long_description,
    url="https://github.com/Baltoch/httpx-system-certs",
    author="Balthazar LEBRETON",
    author_email="balthazar.lebreton@gmail.com",
    license="MIT",
    packages=["httpx_system_certs"],
    install_requires=["truststore", "httpx"],
    data_files=[("/", ["httpx_system_certs.pth"])],
)
