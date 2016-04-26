from setuptools import setup, find_packages
import os

version = '1.0'

long_description = '\n'.join([
    open("README.txt").read(),
    open(os.path.join("docs", "HISTORY.txt")).read()]
)

setup(
    name='ejn.policy',
    version=version,
    description="",
    long_description=long_description,
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
    ],
    keywords='',
    author='Zentraal',
    author_email='',
    url='https://github.com/zentraal/ejn-buildout',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['ejn'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'plone.app.users',
        'collective.registrationform'
    ],
    entry_points="""
    # -*- Entry points: -*-

    [z3c.autoinclude.plugin]
    target = plone
    """,
)
