from setuptools import setup, find_packages

description = """PySide Layout Tool is an open-source graphical user interface (GUI) tool developed using Python and 
the PySide2 library for creating and editing layouts in PySide-based applications. The tool provides a simple and 
intuitive interface for designing and manipulating widgets and layouts, which are the building blocks of PySide 
applications. The PySide Layout Tool allows users to create, edit, and save layouts in various file formats, 
including JSON and XML. It also provides a preview mode that allows users to see how the layout will look. The tool 
provides a wide range of layout options, including grid layout, horizontal layout, vertical layout, and stacked 
layout. The tool is designed to simplify the layout creation process and make it more efficient. Users can drag and 
drop widgets onto the canvas and adjust their position and size using the mouse. The tool also provides alignment and 
spacing options to help users create a neat and organized layout. """


setup(name='PySideLayoutTool',
      version='0.3.4',
      description='PySide Layout Tool is an open-source graphical user interface (GUI) tool developed using PySide2',
      long_description=description,
      maintainer='Jonathan Cortez',
      url='https://github.com/JonathanCortez/PySideLayoutTool',
      author='Jonathan Cortez',
      author_email='jonathancdev@outlook.com',
      license='LGPL-3.0',
      install_requires=['PySide2>=5.15.2.1', 'Markdown'],
      package_data={'PySideLayoutTool.resources': ['data/*.uiproject', 'data/*.css', 'data/*.qss', 'data/*.md', 'Icons/*.svg', '*.qrc'],
                    'PySideLayoutTool.UIEditorTemplates': ['*.uiplugin']},
      packages=find_packages(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
          'Natural Language :: English',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: Microsoft :: Windows :: Windows 11',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Software Development :: User Interfaces'
      ],
      )
