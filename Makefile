create-container-network:
	docker network create automatedaftermath-net

create-postgres-server:
	docker run -d --net automatedaftermath-net --name automatedaftermath-postgres13 -p 5432:5432 -e POSTGRES_USER=automatedaftermath -e POSTGRES_PASSWORD=mysecretpassword -v pg13-aa:/var/lib/postgresql/data postgres:13

build-loader:
	docker build -t automatedaftermath-loader -f ./postgres_loader/Dockerfile .

run-loader:
	docker run -d --net automatedaftermath-net --name automatedaftermath-loader -v ${PWD}/postgres_loader/:/app/src automatedaftermath-loader