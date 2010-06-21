
from distutils.core import setup

setup(
    name='nebpublisher',
    version='1.0.1',
    description='Event integration with Nagios in Python',
    author='Intelie',
    author_email='developers@intelie.com.br',
    url='http://www.intelie.com.br',
    packages=['nebpublisher', 'nebpublisher.utils'],
    scripts=['nebpublisher.py'],
    data_files=[('/etc/init.d', ['nebpublisher.sh']),
                ('nebpublisher/conf','nebpublisher/conf/log.ini')],
)
