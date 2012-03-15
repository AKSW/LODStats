from setuptools import setup, find_packages
setup(name='lodstats',
      version='0.3',
      author = 'Jan Demter',
      author_email = 'jan@demter.de',
      url = 'http://aksw.org/projects/LODStats',
      description = 'Gather statistics from RDF files in various formats',
      long_description = """
          LODStats uses Redland (librdf) to access files adhering to the Resource
          Description Framework (RDF) and compute various configurable
          statistics about them.
          You will need to manually install librdf, i.e.
          sudo apt-get install python-librdf for Debian/Ubuntu.
          Extending LODStats with custom statistics is easily accomplished.
      """,
      classifiers = ['Development Status :: 3 - Alpha',
                     'License :: OSI Approved :: GNU General Public License (GPL)',
                     'Programming Language :: Python',
                     'Intended Audience :: Information Technology',
                     'Intended Audience :: Science/Research',
                     'Environment :: Console',
                     'Topic :: Software Development :: Libraries :: Python Modules',
                     'Topic :: Internet :: RDF',
                     'Topic :: Scientific/Engineering :: Information Analysis',
                     'Topic :: Internet :: WWW/HTTP',
                     'Topic :: Utilities',
                    ],
      packages=find_packages(),
      scripts=['scripts/lodstats'],
      package_data={'lodstats': ['rdf/*.rdf']},
      install_requires = ['requests', 'bitarray', 'sparqlwrapper'],
      )
