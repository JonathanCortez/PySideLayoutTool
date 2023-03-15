from setuptools import setup, find_packages

setup(name='pysidelayouttool',
      version='0.1.7',
      description='A pyside2 parameter layout tool/application.',
      url='https://github.com/JonathanCortez/PySideLayoutTool',
      author='Jonathan Cortez',
      author_email='jonathancdev@outlook.com',
      license='LGPL-3.0',
      install_requires=['PySide2', 'numpy'],
      package_data={'PySideLayoutTool.resources': ['data/*.uiproject', 'data/*.css', 'data/*.qss', 'Icons/*.svg'], 'PySideLayoutTool.UIEditorTemplates' : ['*.uiplugin']},
      packages=find_packages()
      )
