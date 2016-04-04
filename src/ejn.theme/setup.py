from setuptools import setup, find_packages
import os

version = '1.0'

setup(
    name='ejn.theme',
    version=version,
    description="The new theme for the Earth Journalism Network website",
    long_description=open(
        "README.md").read() + "\n" + open(
        os.path.join("docs", "HISTORY.txt")).read(),
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
    ],
    keywords='',
    author='Luca Pisani',
    author_email='luca.pisani@abstract.it',
    url='http://svn.plone.org/svn/collective/',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['ejn'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'z3c.jbot',
        'plone.app.theming',
        # -*- Extra requirements: -*-
        'pycountry'
    ],
    entry_points="""
    # -*- Entry points: -*-

    [z3c.autoinclude.plugin]
    target = plone
    """,
    paster_plugins=["ZopeSkel"],
)
