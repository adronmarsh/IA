# Kafka

## Ir a la carpeta de Kafka
```copyable
cd /usr/local/kafka/
```
----------------------------------------------------------------------------
## Crear Topic
```copyable
bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic testTopic
```

## Listar topics
```copyable
bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

## Editar topic
```copyable
bin/kafka-console-producer.sh --broker-list localhost:9092 --topic testTopic --from-beginning
```

## Ejecutar topic
```copyable
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic testTopic --from-beginning
```

## Borrar topic
```copyable
bin/kafka-topics.sh --delete --bootstrap-server localhost:9092
```

----------------------------------------------------------------------------

## Listar Zookeeper
```copyable
bin/kafka-topics.sh --list --zookeeper localhost:2181
```

## Crear Zookeeper
```copyable
bin/kafka-topics.sh --create --zookeeper localhost:2181 -replication-factor 1 --partitions 1 --topic testTopic
```

## Eliminar Zookeeper
```copyable
bin/kafka-topics.sh --delete --zookeeper localhost:2181 -topic testTopic
```

## Información Zookeeper
```copyable
bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic testTopic
```

----------------------------------------------------------------------------

## LEVANTAR VARIOS KAFKA

Vamos a copiar varias veces el fichero properties. Para ello:

### Ir a la carpeta de configuración
```copyable
cd /usr/local/kafka/config
```
### Copiar los ficheros properties
```copyable
cp server.properties server-0.properties
```
```copyable
cp server.properties server-1.properties
```
```copyable
cp server.properties server-2.properties
```
```copyable
cp server.properties server-3.properties
```
### Modificar los ficheros properties
#### server-0.properties
```copyable
sudo nano server-0.properties
```
```copyable
    broker.id=0
    listeners=PLAINTEXT://:9092
    log.dirs=/tmp/kafka-logs-0
    zookeeper.connect=localhost:2181 
```
#### server-1.properties
```copyable
sudo nano server-1.properties
```
```copyable
    broker.id=1
    listeners=PLAINTEXT://:9093
    log.dirs=/tmp/kafka-logs-1
    zookeeper.connect=localhost:2181 
```
#### server-2.properties
```copyable
sudo nano server-2.properties
```
```copyable
    broker.id=2
    listeners=PLAINTEXT://:9094
    log.dirs=/tmp/kafka-logs-2
    zookeeper.connect=localhost:2181 
```
#### server-3.properties
```copyable
sudo nano server-3.properties
```
```copyable
    broker.id=3
    listeners=PLAINTEXT://:9095
    log.dirs=/tmp/kafka-logs-3
    zookeeper.connect=localhost:2181 
```

# ARRANCAR LOS DISTINTOS SERVIDORES 

## PRIMERO ZOOKEEPER
```copyable
sudo /usr/local/kafka/bin/zookeeper-server-start.sh /usr/local/kafka/config/zookeeper.properties
```

## DESPUÉS LOS DIFERENTES BROKERS
```copyable
sudo /usr/local/kafka/bin/kafka-server-start.sh  /usr/local/kafka/config/server-0.properties
```
```copyable
sudo /usr/local/kafka/bin/kafka-server-start.sh  /usr/local/kafka/config/server-1.properties
```
```copyable
sudo /usr/local/kafka/bin/kafka-server-start.sh  /usr/local/kafka/config/server-2.properties
```
```copyable
sudo /usr/local/kafka/bin/kafka-server-start.sh  /usr/local/kafka/config/server-3.properties
```

----------------------------------------------------------------------------

## Creamos un Topic con 3 replicas:
```copyable
sudo /usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 3 --partitions 1 --topic topicf3p1
```
```copyable
sudo /usr/local/kafka/bin/kafka-topics.sh --list --zookeeper localhost:2181
```
```copyable
sudo /usr/local/kafka/bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic topicf3p1
```

----------------------------------------------------------------------------

## Ejemplo multinodo 1:

### Creamos 1 productor + 2 consumidores

1) Creamos un productor (consola a parte)
```copyable
sudo /usr/local/kafka/bin/kafka-console-producer.sh --broker-list localhost:9092,localhost:9093 --topic topicf3p1
```

2) Creamos el 1er consumidor (consola a parte)
```copyable
sudo /usr/local/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092,localhost:9093 --from-beginning --topic topicf3p1
```

3) Escribimos varios mensajes mediante el productor

4) Creamos el 2do consumidor (consola a parte)
```copyable
sudo /usr/local/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092,localhost:9093 --from-beginning --topic topicf3p1
```

----------------------------------------------------------------------------

### Creamos 1 productor + 3 consumidores

1) Creamos el 3er consumidor (consola a parte)
```copyable
sudo /usr/local/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092,localhost:9093 --topic topicf3p1
```

----------------------------------------------------------------------------
----------------------------------------------------------------------------

## Ejemplo Multinodo 2: 

### 1 productor + 2 consumidores en grupo- 1 partición

1) Paramos los productores y consumidores del ejercicio anterior

2) Creamos un nuevo topic
```copyable
$ kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 3 --partitions 1 --topic topicf3p1g
```
```copyable
$ kafka-topics.sh --list --zookeeper localhost:2181
```
```copyable
$ kafka-topics.sh --describe --zookeeper localhost:2181 --topic topicf3p1g
```

----------------------------------------------------------------------------

### 1 productor + 2 consumidores en grupo - 1 partición

1) Creamos un productor (nueva consola)
```copyable
kafka-console-producer.sh --broker-list localhost:9092,localhost:9093 --topic topicf3p1g
```

2) Creamos 1er consumidor (nueva consola)
```copyable
kafka-console-consumer.sh --bootstrap-server localhost:9092,localhost:9093 --topic topicf3p1g --consumer-property group.id=grupo1
```

3) Creamos 2do consumidor (nueva consola)
```copyable
kafka-console-consumer.sh --bootstrap-server localhost:9092,localhost:9093 --topic topicf3p1g --consumer-property group.id=grupo1
```

4) Desde el productor creamos varios mensajes
    
    · Verificar que los mensajes solo se ven en uno de los consumidores    
    · Verificar que hay un consumidor asignado a la particion leader

----------------------------------------------------------------------------
----------------------------------------------------------------------------

## Ejemplo Multinodo 3: 

### 1 productor + 2 consumidores en grupo de 2 particiones

1) Paramos los productores y consumidores del ejercicio anterior
2) Creamos un nuevo topic
```copyable
kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 3 --partitions 2 --topic topicf3p2g
```
```copyable
kafka-topics.sh --list --zookeeper localhost:2181
```
```copyable
kafka-topics.sh --describe --zookeeper localhost:2181 --topic topicf3p2g
```

----------------------------------------------------------------------------

### 1 productor + 2 consumidores en grupo 2 particiones

1) Creamos un productor (nueva consola)
```copyable
kafka-console-producer.sh --broker-list localhost:9092,localhost:9093 --topic topicf3p2g
```

2) Creamos 1er consumidor (nueva consola)
```copyable
kafka-console-consumer.sh --bootstrap-server localhost:9092,localhost:9093 --topic topicf3p2g --consumer-property group.id=grupo1
```

3) Creamos 2do consumidor (nueva consola)
```copyable
kafka-console-consumer.sh --bootstrap-server localhost:9092,localhost:9093 --topic topicf3p2g --consumer-property group.id=grupo1
```

4) Desde el productor creamos varios mensajes

    · Verificar que los mensajes se reparten entre los consumidores

----------------------------------------------------------------------------
----------------------------------------------------------------------------

## Ejemplo Multinodo 4: 

### Detener servidores

1) Paramos los productores y consumidores del ejercicio anterior

2) Creamos un nuevo topic
```copyable
sudo /usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 3 --partitions 2 --topic topic_server
```
```copyable
sudo /usr/local/kafka/bin/kafka-topics.sh --list --zookeeper localhost:2181
```
```copyable
sudo /usr/local/kafka/bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic topic_server
```

3) Paramos el server 0 (leader de la particion 1)

4) Verificamos que al hacer describe se modifica la lista de servidores