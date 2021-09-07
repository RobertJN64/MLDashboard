from setuptools import setup

setup(
    name='MLDashboard',
    url='https://github.com/RobertJN64/MLDashboard',
    author='Robert Nies',
    author_email='robertjnies@gamil.com',
    # Needed to actually package something
    packages=['MLDashboard'],
    # *strongly* suggested for sharing
    version='0.0.1',
    # The license can be anything you like
    license='MIT',
    description='Machine learning dashboard that integrates with tensorflow.',
    long_description=open('README.txt').read(),
)