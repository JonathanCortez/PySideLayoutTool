from setuptools import setup

setup(name='PySide Layout Tool',
      version='0.1.1',
      description='A pyside2 parameter layout tool/application.',
      url='https://github.com/JonathanCortez/PySideLayoutTool',
      author='Jonathan Cortez',
      author_email='jonathancdev@outlook.com',
      license='LGPL-3.0',
      install_requires=['PySide2', 'numpy'],
      packages=['Resources','UIEditorLib', 'UIEditorTemplates', 'UIEditorTemplates', 'UIEditorWindows']
      )
