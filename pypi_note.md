bumpversion --current-version <version> minor --config-file setup.cfg
python setup.py sdist   
twine upload -r pypitest dist/django-async-image-upload-<version>.tar.gz  

