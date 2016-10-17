# OpenBuildService source service to process .spec.j2 templates with renderspec
[![Build Status](https://travis-ci.org/openSUSE/obs-service-renderspec.svg?branch=master)](https://travis-ci.org/openSUSE/obs-service-renderspec)

An Open Build Service source service for rendering .spec.j2 templates with 
[renderspec](https://pypi.python.org/pypi/renderspec)


## Requirements
`python-requests`, `python-six` and `renderspec`.

## Testing
The tests can be called with:

    python tests/test_base.py
