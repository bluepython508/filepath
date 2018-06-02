#!/bin/bash
path=${2:-'.'}
cd ${path}
rm -rf ${path}/dist
echo "Path is ${path}"
version=$(python package_version.py)
if [ -z ${1+x} ]; then
    read -p "Version (currently ${version}): " version
else
    version=$1
fi
echo "Version is ${version}"
echo "version='${version}'" > ${path}/package_version.py
echo 'print(version)' >> ${path}/package_version.py
python ${path}/setup.py sdist bdist_wheel
twine upload ${path}/dist/*
rm -rf ${path}/dist ${path}/build ${path}/*.egg-info