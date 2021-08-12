## Pre-reqs

- Docker installed and running
- GNU Make to use `Makefile` on Windows: http://gnuwin32.sourceforge.net/packages/make.htm
- Copy `example.env` to a file named `.env` in the same directory. This file should not need to be modified for the flow described in this document.

### Storing data
- In the same directory as this file, create another directory named `data`. Within, place your `.accdb` files. You can download archives containing these files [here](https://nces.ed.gov/ipeds/use-the-data/download-access-database).
- Modify `files.py` to match the files you have present. Currently it is configured for multiple years of the IPEDS databases. **Comment out any lines with file names that you do not have present in `data`.**

## Setup

### Docker network
Create a Docker network so the containers can communicate. Run this command in the parent directory of this one:
```
make create-container-network
```

### Postgres container

Create a Postgres container by running this command in the parent directory of this one:
```
make create-postgres-server
```

#### Optional
If you want to directly query the database, connect to its container by running this command (you can also find the image in the Docker Desktop application and launch a CLI window from there):
```
docker exec -it container_id /bin/sh
```

And to start the Postgres CLI client:
```
psql automatedaftermath automatedaftermath
```

### Loader container

#### Create image
Build the loader application image by running this command in the parent directory of this one:
```
make build-loader
```

#### Run loader container
With the Postgres container running and the loader application built, place your `*.accdb` files in the `data` directory. Then run the following command to start the loader application, which will convert and store tables in the Postgres database:
```
make run-loader
```