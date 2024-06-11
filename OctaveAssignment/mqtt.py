import paho.mqtt.client as paho
USERNAME = 'octave'
PASSWORD = 'x9MT*qXj!bRRpG'
HOSTNAME = 'ec2-34-241-251-27.eu-west-1.compute.amazonaws.com'
PORT = 1883

client = paho.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.connect(HOSTNAME, PORT)
QOS = 1
TOPIC = "/warnings"