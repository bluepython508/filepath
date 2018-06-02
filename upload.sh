#!/bin/bash
path=${1:-'.'}
cd ${path}
rm -rf ${path}/dist
echo "Path: ${path}"
version=$(python package_version.py)
read -p "Version (currently ${version}): " version
echo "version='${version}'" > ${path}/package_version.py
echo 'print(version)' >> ${path}/package_version.py
python ${path}/setup.py sdist bdist_wheel
twine upload ${path}/dist/*
rm -rf dist
