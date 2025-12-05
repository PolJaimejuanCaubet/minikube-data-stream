## MINIKUBE
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
