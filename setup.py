from setuptools import setup, find_packages


setup(
    name='ImarisXtension',
    description='Reconstructrs the 3D image for the lesion site',
    version='0.1.0',
    packages=find_packages(),
    #platforms=['mac', 'unix'],
    python_requires='=3.7',
    install_requires=[
        'numpy==1.19.2',
        
    ],
    #entry_points={'console_scripts': ['moseq2-nlp = moseq2_nlp.cli:cli']}
)