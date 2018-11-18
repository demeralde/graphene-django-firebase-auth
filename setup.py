import os
from setuptools import setup


README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

setup(
    name='graphene_django_firebase_auth',
    version='1.0.0',
    author='Daniel Spajic',
    author_email='daniel@danieljs.tech',
    description=(
        "Authentication provider for graphene-django and Google Firebase's "
        "Authentication service."
    ),
    license='MIT',
    keywords='graphene django firebase auth',
    url='https://github.com/dspacejs/graphene-django-firebase-auth',
    packages=['firebase_auth'],
    install_requires=['django', 'firebase-admin'],
    long_description=README,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
    ],
)
