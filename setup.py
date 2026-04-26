from setuptools import setup, find_packages

setup(
    name='beat_spec_visual',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'modusa',
        'matplotlib',
        'numpy',
        'librosa',
        'soundfile',
        'torch',
        'beat_this',
    ],
    author='Your Name',
    description='BeatSpecVisual: Beat detection and visualization system',
    url='https://github.com/yourusername/BeatSpecVisual',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)