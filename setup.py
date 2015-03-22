from setuptools import setup

setup(
    name='trnzscrybe',
    version='0.3.1',
    
    description='Python module for music transcription',
    long_description="""A python module for music transcription, really.""",
    
    author='David Kant',
    author_email='david.kant@gmail.com',

    license='MIT',
    
    url='http://github.com/davidkant/trnzscrybe',
    download_url='http://github.com/davidkant/trnzscrybe/releases',
    
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Multimedia :: Sound/Audio :: Music :: Music Notation',
        'License :: OSI Approved :: MIT',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='music notation audio sound',

    packages=['trnzscrybe'],

    install_requires=[
        'abjad',
        'numpy',
    ],

    extras_require={
        'testing': 'nose'
    }
)