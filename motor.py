import RPi.GPIO as GPIO
import time
import mysql.connector

in1 = 24
in2 = 23
en = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
p = GPIO.PWM(en, 1000)
p.start(25)


def up(second):
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    time.sleep(second)
    stop()
    save_boolean_to_file(False)

def down(second):
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    time.sleep(second)
    stop()
    save_boolean_to_file(True)

def stop():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)

def save_boolean_to_file(boolean_value):
    with open("status.txt", 'w') as file:
        file.write(str(boolean_value))

def load_boolean_from_file():
    with open("status.txt", 'r') as file:
        boolean_value = file.read().strip()
        if boolean_value.lower() == 'true':
            return True
        elif boolean_value.lower() == 'false':
            return False
        else:
            raise ValueError("Invalid boolean.")

try:
    sql_conn = mysql.connector.connect(user='weerstation', password='Kjeltmeteent',
                          host='localhost',
                          database='weerstation')
except mysql.connector.Error as err:
    print("Fout bij het openen van de MySQL-verbinding:", err)
    exit()

cursor = sql_conn.cursor()

cursor.execute("SELECT light FROM weerstation ORDER BY id DESC LIMIT 1")
light = cursor.fetchone()

cursor.execute("SELECT rain FROM weerstation ORDER BY id DESC LIMIT 1")
rain = cursor.fetchone()

if float(light[0]) >= 0.05 and load_boolean_from_file() == False:
    down(3)
elif float(light[0]) < 0.05 and load_boolean_from_file() == True or float(rain[0]) > 0:
    up(3)


GPIO.cleanup()