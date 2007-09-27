from setuptools import setup, find_packages

version = '1.9'

setup(name='collective.realestatebroker',
      version=version,
      description="An easy and professional way to publish real estate objects on your Plone website",
      long_description="""\
""",
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='realestate makelaar plone',
      author='Reinout van Rees (Zest software)',
      author_email='reinout@zestsoftware.nl',
      url='http://plone.org/products/realestatebroker',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
