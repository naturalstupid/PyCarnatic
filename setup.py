import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="carnatic music guru", # Replace with your own username
    version="0.2.0",
    author="Sundar Sundaresan",
    author_email="get.in.touch.with.sundar@gmail.com",
    description="The goal of the carnatic music guru is to provide library for generating carnatic music lessons as notes, parse and play the carnatic music notes using various instruments, fit to the thaaLa",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/naturalstupid/carnatic_music_guru",
    # project_urls={
    #     "Bug Tracker": "https://bugs.example.com/HelloWorld/",
    #     "Documentation": "https://docs.example.com/HelloWorld/",
    #     "Source Code": "https://code.example.com/HelloWorld/",
    # },    
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    download_url='https://github.com/naturalstupid/carnatic_music_guru/archive/master.zip',
    install_requires=[
        'itertools',
        'operator',
        'collections',
        'enum',
    ]
)