# Dockerized Mercurial Server

This is a mercurial-server, modified, patched and prepared to work dockerized based on Alpine Linux container with minimal resources footprint.

## Original mercurial-server

Original sources of mercurial-server can be obtained here: https://bitbucket.org/lshift/mercurial-server
Also you can get additional info on original mercurial-server here: http://tech.labs.oliverwyman.com/open-source/mercurial-server/
All rights on original sources belongs to its authors.

## Patches

This mercurial-server sources copy contains some patches based on several not integrated pull requests from original repo and also some other fixes made by me (f.e. fixed logging). Also this sources is slightly reorganized and some additional custom scripts added to run mercurial-server in dockerized environment.

## Usage

You can find general usage instructions in **mercurial-server-manual.html** that I've precompiled from original sources and placed here. In some future I will try to find time to correct and expand this manual according to dockerized usage specifics.

Now, the simplest way to use it is to create a container from latest available prebuilt image in Docker Hub (https://hub.docker.com/r/darksimpson/mercurial-server) or from image build by itself from this sources, map an SSH port, map two volumes (for keys and repos) and start container. At first run all the things and preparations will be done by startup script automatically. After that you will only need to place your admin SSH pubkey to newly created root subdir of keys volume and restart container to refresh available keys. After that you can use your mercurial-server sertup as it is generally described in mercurial-server-manual.html

For simpler container setup you can use Docker Compose file something like this one:
```
version: '2'

services:
  mercurial-server:
    image: 'darksimpson/mercurial-server'
    network_mode: bridge
    ports:
      - '8022:8022'
    volumes:
      - './repos_data:/var/lib/mercurial-server/repos'
      - './keys_data:/etc/mercurial-server/keys'
```
