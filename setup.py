from setuptools import setup

setup(
    name='MLDashboard',
    url='https://github.com/RobertJN64/MLDashboard',
    author='Robert Nies',
    author_email='robertjnies@gamil.com',
    # Needed to actually package something
    packages=['MLDashboard', 'MLDashboard.DashboardModules', 'MLDashboard.Examples'],
    install_requires=[
        'matplotlib',
        'tensorflow'
    ],
    # *strongly* suggested for sharing
    version='0.0.3',
    # The license can be anything you like
    license='MIT',
    description='Machine learning dashboard that integrates with tensorflow.',
    long_description=open('README.md').read(),
)