from setuptools import setup, find_packages
import os.path

versionfile = open(os.path.join('collective', 'realestatebroker', 'version.txt'))
version = versionfile.read().strip()
versionfile.close()

readmefile = open(os.path.join('collective', 'realestatebroker', 'README.txt'))
readme = readmefile.read().strip()
readmefile.close()

installfile = open(os.path.join('docs', 'INSTALL.txt'))
install = installfile.read().strip()
installfile.close()

historyfile = open(os.path.join('collective', 'realestatebroker', 'HISTORY.txt'))
history = historyfile.read().strip()
historyfile.close()

long_description= """%s


%s


%s
""" % (readme, install, history)


setup(name='collective.realestatebroker',
      version=version,
      description="An easy and professional way to publish real estate objects on your Plone website",
      long_description= long_description,
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
          'archetypes.schemaextender==1.0b1',
          'Products.contentmigration==1.0b4',
          'Products.PloneFlashUpload',
          'Products.Maps',
          # ReportLab needs http://ftp.schooltool.org/schooltool/eggs/
          # in the find-links parameter of your buildout.cfg
          'ReportLab', 
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
