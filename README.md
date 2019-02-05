# unitmulti

*Convert base unit values to multiples and submultiples*

* **category**    Library
* **copyright**   2019 Tecnick.com LTD
* **license**     see [LICENSE](LICENSE)
* **link**        https://github.com/tecnickcom/unitmulti


## Description

Convert base unit values to multiples and submultiples.

For example:

```
12345 B -> 12.1 KiB
 1000 m ->  1.0 Km
```

## Quick Start

This project includes a Makefile that allows you to test and build the project in a Linux-compatible system with simple commands.

To see all available options:
```
make help
```

To test the project inside a Python 2.7 virtual environment:
```
make vtest
```

To build a Conda development environment:  
```
make conda_dev
. activate
```

To test inside a `conda_dev` environment using setuptools:  
```
make test
```

To build and test the project inside a Conda environment:  
```
make build
```

The coverage report is available at:  
```env-unitmulti/conda-bld/coverage/htmlcov/index.html```

To build the project inside a Docker container (requires Docker):
```
make dbuild
```

An arbitrary make target can be executed inside a Docker container by specifying the "MAKETARGET" parameter:
```
MAKETARGET='build' make dbuild
```
The list of make targets can be obtained by typing ```make```


The base Docker building environment is defined in the following Dockerfile:
```
resources/Docker/Dockerfile.dev
```

To format the code (please use this command before submitting any pull request):
```
make format
```

## Useful Docker commands

To manually create the container you can execute:
```
docker build --tag="tecnickcom/unitmultidev" .
```

To log into the newly created container:
```
docker run -t -i tecnickcom/unitmultidev /bin/bash
```

To get the container ID:
```
CONTAINER_ID=`docker ps -a | grep tecnickcom/unitmultidev | cut -c1-12`
```

To delete the newly created docker container:
```
docker rm -f $CONTAINER_ID
```

To delete the docker image:
```
docker rmi -f tecnickcom/unitmultidev
```

To delete all containers
```
docker rm $(docker ps -a -q)
```

To delete all images
```
docker rmi $(docker images -q)
```
