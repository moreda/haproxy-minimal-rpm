# README

Build HAProxy RPM packages using Docker.

Features:

- Compatible with EL8 and EL9 distributions
- Targets the `linux/amd64` platform (you can also set `linux/arm64`)
- Lua and Prometheus support enabled

To generate packages under `{el8|el9}/RPMS`, simply run `make` on the top directory.

This is a minimalistic approach that "works for me (TM)". Thank you to @DBezemer. His work served as the foundation for this project.
