# MINIKUBE
### Technologies used
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=for-the-badge&logo=kubernetes&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Apache Kafka](https://img.shields.io/badge/Apache%20Kafka-000?style=for-the-badge&logo=apachekafka)
![Mosquitto](https://img.shields.io/badge/mosquitto-%233C5280.svg?style=for-the-badge&logo=eclipsemosquitto&logoColor=white)


```bash
cd minikube-project
```
```bash
minikube start
minikube dashboard
```
Open new terminal
```bash
docker build -t ingestor ./cloud/ingestor
minikube image load ingestor
kubectl apply -f cloud/servicesk8s/ingestor.yml -f cloud/servicesk8s/kafka.yml -f cloud/servicesk8s/mosquitto-cloud.yml -f cloud/servicesk8s/zookeeper.yml
kubectl port-forward svc/mosquitto-svc 1883:1883
```
(per a poder accedir al mosquito desde el meu localhost al mosquito dins del minikube)
per al MQTT EXPLORER el port 1883 i localhost)

Open new terminal

```bash
kubectl apply -f cloud/servicesk8s/influx-db.yml
kubectl port-forward svc/influxdb-svc 8086:8086
```

Open new terminal

[InfluxDB UI](http://localhost:8086/)
user: admin
password: cloudpass

```bash
docker build -t p1-save ./cloud/save_raw
minikube image load p1-save
kubectl apply -f cloud/servicesk8s/save-raw-data.yml
```
```bash
docker build -t p2-clean ./cloud/clean
minikube image load p2-clean
kubectl apply -f cloud/servicesk8s/clean.yml
```

```bash
docker build -t p3-actuate ./cloud/actuate
minikube image load p3-actuate
kubectl apply -f cloud/servicesk8s/actuate.yml
```

```bash
docker build -t p4-aggregate ./cloud/aggregate
minikube image load p4-aggregate
kubectl apply -f cloud/servicesk8s/aggregate.yml
```
```bash
docker compose up --build
docker-compose -p <several-projects> up 
```
