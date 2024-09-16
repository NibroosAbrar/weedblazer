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
unsigned long laserStartTime = 0;
unsigned long laserDuration = 15000; // 15 seconds

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
    int panjangsumbux, panjangsumbuy, inputX;
    sscanf(input.c_str(), "%d %d %d", &panjangsumbux, &panjangsumbuy, &inputX);

    // Calculate steps based on input
    long stepsX = panjangsumbux;
    long stepsY = panjangsumbuy;

    Serial.print("Panjang Sumbu x=");
    Serial.println(panjangsumbux);
    Serial.print("Panjang Sumbu y=");
    Serial.println(panjangsumbuy);

    digitalWrite(ENABLE_PIN, LOW); // Enable all motors

    // Set direction based on the sign of the input
    stepperX.moveTo(stepsX);
    stepperY1.moveTo(stepsY);

    // Run motors until they reach the target position
    while (stepperX.distanceToGo() != 0 || stepperY1.distanceToGo() != 0) {
      stepperX.run();
      stepperY1.run();
    }

    // Logic to control laser based on input from Serial
    if (inputX == 1) {
      digitalWrite(LASER_PIN, HIGH); // Turn on the laser
      isLaserOn = true;
      laserStartTime = millis();
    }
    digitalWrite(ENABLE_PIN, HIGH); // Disable all motors, stop movement
  }

  // Check if laser has been on for the duration
  if (isLaserOn && millis() - laserStartTime >= laserDuration) {
    digitalWrite(LASER_PIN, LOW); // Turn off the laser
    isLaserOn = false;
  }
}
