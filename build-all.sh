#!/usr/bin/env bash 

set -xe

DEBUG_MODE="1"
RELEASE_NUMBER="1"
VERSION_NUMBER="2.0.0"

BUILD_ARRAY=`ls -d chihaya-*/`

if [[ ! -z "${BUILD_ONLY}" ]];then
	BUILD_ARRAY=`ls -d */|egrep "${BUILD_ONLY}"`
fi

#for Build in `find ./ -type d -maxdepth 1`
for Build in ${BUILD_ARRAY}
do
	echo $Build
	cd "$Build"
	DOCKER_IMAGE=`cat dockerimage`
	echo "${DOCKER_IMAGE}"
	stat dockerimage && \
		( docker image inspect  "${DOCKER_IMAGE}" || docker build . -t "${DOCKER_IMAGE}" )
	stat build && docker run -it \
	        -e COMPRESSION="${COMPRESSION}" \
	        -e DEBUG_MODE="${DEBUG_MODE}" \
	        -e RELEASE_NUMBER="${RELEASE_NUMBER}" \
	        -e VERSION_NUMBER="${VERSION_NUMBER}" \
	        -v `pwd`/srv:/srv \
	                "${DOCKER_IMAGE}"
	cd -
done

set +xe
