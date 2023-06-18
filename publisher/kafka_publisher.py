# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 8:59 AM 2023
this program read JSON file and play a role 
as publisher of clickstream events
@author: Duong Hoai Nam
"""

from kafka import KafkaProducer
import json
from kafka.admin import KafkaAdminClient, NewTopic
from time import sleep
from numpy import random
import settings

def on_success(metadata):
  print(f"Message produced to topic '{metadata.topic}' at offset {metadata.offset}")

def on_error(e):
  print(f"Error sending message: {e}")

if __name__ == "__main__":
  # Set sleep time
  sleeptime = random.uniform(1, 4)
  # Set up KafkaProducer 
  producer = KafkaProducer(bootstrap_servers=settings.BOOTSTRAP_SERVERS,
                          value_serializer=lambda m: json.dumps(m).encode('utf-8'))

  # Create topic in Kafka with Python-kafka admin client
  try:
      admin_client = KafkaAdminClient(bootstrap_servers=settings.BOOTSTRAP_SERVERS)
      topic_list = []
      topic_list.append(NewTopic(name=settings.KAFKA_TOPIC, num_partitions=1, replication_factor=1))
      admin_client.create_topics(new_topics=topic_list, validate_only=False)
      print("Topic {} created".format(settings.KAFKA_TOPIC))
  except Exception as err:
      print(f"Request for topic creation is failing due to {err}")

  # Send data to Kafka topic using json file
  # Produce asynchronously with callbacks
  with open(settings.FILE_PATH) as f:
      for line in f:
          send_data = producer.send(settings.KAFKA_TOPIC, json.loads(line))
          send_data.add_callback(on_success)
          send_data.add_errback(on_error)
          sleep(sleeptime)

  producer.flush()
  producer.close()


