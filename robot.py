#import Wire
#import Adafruit_PWMServoDriver
import board                                         # Importación de las bibliotecas necesarias para la utilización de la placa (controlador servo PCA9685 de Adafruit)
import busio
import Jetson.GPIO as GPIO
import adafruit_pca9685
import time
i2c = busio.I2C(board.SCL, board.SDA)
from adafruit_servokit import Servokit


#declaro variables globales
MIN_PULSE_WIDTH = 650                               # Mínimo del ancho de pulso 
MAX_PULSE_WIDTH = 2350                              # Máximo del ancho de pulso
FREQUENCY = 50

#Instancio el Driver del controlador de servos 
#Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver
pca.frecuency = FRECUENCY
pwm = adafruit_pca9685.PCA9685(i2c)                 # pwm= modulación por ancho de pulso.
kit =ServoKit(channels=16)                          # Tarjeta pca9685 ,con 16 canales, es el controlador de servos.

# Configurar el SetUP
time.sleep(5)                                       # Retrasar 5 segundos para llevar el controlador a la posición inicial
pwm.frequency = FRECUENCY
GPIO.setmode(GPIO.BOARD)

hand = pwm.chanels[1]                               # Asignar un canal a cada servo, en la placa controladora.
wrist = pwm.chanels[2]   
elbow = pwm.chanels[3]
shoulder = pwm.chanels[4]
base = pwm.chanels[5]

potWrist = pwm.chanels[6]                           # Asignar un canal a cada potenciómetro de entre los pines disponibles, de los 40 de la Jetson.
potElbow = pwm.chanels[7]                        
potShoulder = pwm.chanels[8]
potBase = pwm.chanels[9]

pwm.setPWMFreq(FREQUENCY)
pwm.setPWM(32, 0, 90)                               # Configurar la garra de la pinza a 90 grados (garra cerrada = posición de inicio)  en Jetson: x= 32
GPIO.setup(chanel, GPIO.IN)                         # El canal tiene que ser un pin válido en Jetson
pwm.begin()

def moveMotor(controlIn,motorOut):
  pulse_wide, pulse_width, potVal = -7              # -7 , podría ser cualquier número que pudiera indica que los resultados de  los tres valores, serán números enteros.
  # potVal = analogRead(controlIn)                    # En Arduino
  potVal = GPIO.input(controlIn)                    # En Jetson
  pulse_wide = map(potVal, 800, 240, MIN_PULSE_WIDTH, MAX_PULSE_WIDTH)
  pulse_width = int(float(pulse_wide) / 1000000 * FREQUENCY * 4096)
  pwm.setPWM(motorOut, 0, pulse_width)
  pwm = GPIO.PWM(motorOut,pulse_widht)

While (True):
  moveMotor(potWrist, wrist)                        # Asignar los movimientos de los motoservos a lo correspondientes potenciómetros
  moveMotor(potElbow, elbow)
  moveMotor(potShoulder, shoulder)
  moveMotor(potBase, base)
  pushButton = GPIO.input(8)                       # Del canal que sea por ejemplo el 13
  if(pushButton == GPIO.LOW):

    pwm.setPWM(hand, 0, 180)                        # Mantener la garra cerrada cuando no de presiona el motor
    print("Grab")
  else:
    pwm.setPWM(hand, 0, 90)                         # Abrir la garra cuando se presiona el botón
    print("Release")
    
GPIO.cleanup()





