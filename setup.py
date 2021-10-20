from setuptools import setup

setup(
    name='MLDashboard',
    url='https://github.com/RobertJN64/MLDashboard',
    author='Robert Nies',
    author_email='robertjnies@gamil.com',
    # Needed to actually package something
    packages=['MLDashboard'],
    install_requires=[
        'matplotlib',
        'tensorflow',
        'numpy',
        'pillow'
    ],
    # *strongly* suggested for sharing
    version='1.1.0',
    # The license can be anything you like
    license='MIT',
    description='Machine learning dashboard that integrates with tensorflow. Great for monitoring training. Has tools for classification and images.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)