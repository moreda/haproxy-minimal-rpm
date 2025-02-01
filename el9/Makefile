SHELL := /bin/bash
LC_ALL := C.utf8
TOPDIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
RPMTOPDIR ?= $(HOME)/rpmbuild
RPMSDIR ?= $(TOPDIR)RPMS
ARCH := $(shell rpm --eval "%{_arch}")
PKGS := haproxy

.PHONY: all $(PKGS)
.ONESHELL:
.EXPORT_ALL_VARIABLES:

all: $(PKGS)

$(PKGS): %: %.stamp

$(PKGS:=.stamp): %.stamp: %.spec
	# Prepare rpmbuild tree.
	mkdir -p $(RPMTOPDIR)/{SRPMS,SOURCES,BUILD} $(RPMSDIR)
	# link local directory from SOURCES.
	ln -nfs $(TOPDIR)files/local $(RPMTOPDIR)/SOURCES/local
	yum-builddep -y $(TOPDIR)$<
	rpmbuild \
		--define "_rpmdir $(TOPDIR)RPMS" \
		--define "_topdir $(RPMTOPDIR)" \
		--undefine=_disable_source_fetch \
		-bb $(TOPDIR)$<
	touch $@

clean:
	rm -rf RPMS *.stamp
