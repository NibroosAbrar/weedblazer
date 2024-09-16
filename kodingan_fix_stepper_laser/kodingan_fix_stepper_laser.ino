#include <AccelStepper.h>

// Define pin connections for stepper motors
#define DIR_PIN_X 5
#define STEP_PIN_X 2
#define DIR_PIN_Y 6
#define STEP_PIN_Y 3
#define ENABLE_PIN 4
#define LASER_PIN 11

// Create stepper objects
AccelStepper stepperX(AccelStepper::DRIVER, STEP_PIN_X, DIR_PIN_X);
AccelStepper stepperY1(AccelStepper::DRIVER, STEP_PIN_Y, DIR_PIN_Y);

bool isLaserOn = false;
unsigned long lastLaserTime = 0;
unsigned long laserDelay = 1000;
int inputX = 0;

void setup() {
  Serial.begin(9600);
  pinMode(DIR_PIN_X, OUTPUT);
  pinMode(STEP_PIN_X, OUTPUT);
  pinMode(DIR_PIN_Y, OUTPUT);
  pinMode(STEP_PIN_Y, OUTPUT);
  pinMode(ENABLE_PIN, OUTPUT);
  pinMode(LASER_PIN, OUTPUT);

  // Disable stepper motors at startup
  digitalWrite(ENABLE_PIN, LOW);

  // Set maximum speed and acceleration for all steppers
  stepperX.setMaxSpeed(1000);
  stepperX.setAcceleration(100);
  stepperY1.setMaxSpeed(1000);
  stepperY1.setAcceleration(100);
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    int panjangsumbux, panjangsumbuy;
    sscanf(input.c_str(), "%d %d %d", &panjangsumbux, &panjangsumbuy, &inputX);

    // Calculate steps based on input
    float stepsX = abs(panjangsumbux) * 50.378;
    float stepsY = abs(panjangsumbuy) * 50.378;

    Serial.print("Panjang Sumbu x=");
    Serial.println(panjangsumbux);
    Serial.print("Panjang Sumbu y=");
    Serial.println(panjangsumbuy);

    digitalWrite(ENABLE_PIN, LOW); // Enable all motors

    int maxSteps = max(stepsX, stepsY);

    // Set direction based on the sign of the input
    // nilai x POSITIF = ke kanan
    // nilai x NEGATIF = ke kiri
    if (panjangsumbux < 0) {
      digitalWrite(DIR_PIN_X, LOW); // Set CCW direction for X axis motor
    } else {
      digitalWrite(DIR_PIN_X, HIGH); // Set CW direction for X axis motor
    }
    
    // nilai y POSITIF = maju
    // nilai y NEGATIF = mundur
    if (panjangsumbuy < 0) {
      digitalWrite(DIR_PIN_Y, LOW); // Set CCW direction for Y axis motor
    } else {
      digitalWrite(DIR_PIN_Y, HIGH); // Set CW direction for Y axis motor
    }

    for (int i = 0; i < maxSteps; i++) {
      if (i < stepsX) {
        digitalWrite(STEP_PIN_X, HIGH);
        delayMicroseconds(100);
        digitalWrite(STEP_PIN_X, LOW);
        delayMicroseconds(100);
      }
      if (i < stepsY) {
        digitalWrite(STEP_PIN_Y, HIGH);
        delayMicroseconds(100);
        digitalWrite(STEP_PIN_Y, LOW);
        delayMicroseconds(100);
      }
    }

    // Logic to control laser based on input from Serial
    if (inputX == 1 && !isLaserOn) {
      digitalWrite(LASER_PIN, HIGH); // Turn on the laser
      isLaserOn = true;
      lastLaserTime = millis();
    } else if (inputX == 0 && isLaserOn) {
      digitalWrite(LASER_PIN, LOW); // Turn off the laser
      isLaserOn = false;
    }

    digitalWrite(ENABLE_PIN, HIGH); // Disable all motors, stop movement
  }
}
