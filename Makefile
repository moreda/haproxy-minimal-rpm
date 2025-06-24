.DEFAULT_GOAL := package

.PHONY: package clean
.ONESHELL:
.EXPORT_ALL_VARIABLES:

DISTS?=el8 el9
PLATFORM?=linux/amd64

package:
	for DIST in $(DISTS); do \
		docker build --platform $${PLATFORM} -t $${DIST}-rpm $${DIST}; \
		docker run \
			--platform $${PLATFORM} \
			--rm \
			-v $${PWD}/$${DIST}:/docker \
			-w /docker \
			$${DIST}-rpm make; \
	done

clean:
	for DIST in $(DISTS); do \
		rm -rf $${PWD}/$${DIST}/RPMS $${PWD}/$${DIST}/*.stamp; \
	done
