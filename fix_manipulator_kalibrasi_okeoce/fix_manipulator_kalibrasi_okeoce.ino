#include <AccelStepper.h>

// Define pin connections for stepper motors and laser
#define dirPinX 5
#define stepPinX 2
#define dirPinY 6
#define stepPinY 3
#define LASER_PIN 11

// Define steps per mm
const float stepsPerMmX = 80;
const float stepsPerMmY = 80;

// Initialize stepper motors
AccelStepper stepperX(AccelStepper::DRIVER, stepPinX, dirPinX);
AccelStepper stepperY(AccelStepper::DRIVER, stepPinY, dirPinY);

// Track the current position in steps
long currentPosX = 0;
long currentPosY = 0;

bool isLaserOn = false;
unsigned long laserStartTime = 0;
unsigned long laserDuration = 7000; // 7 seconds

void setup() {
  Serial.begin(9600);
  stepperX.setMaxSpeed(1000);
  stepperX.setAcceleration(500);
  stepperY.setMaxSpeed(1000);
  stepperY.setAcceleration(500);
  pinMode(LASER_PIN, OUTPUT);
  Serial.println("Masukkan koordinat piksel dalam format X,Y:");
}

void moveToPixel(int pixelX, int pixelY) {
  // Convert pixels to mm
  float targetMmX = pixelX * 0.984;
  float targetMmY = pixelY * 1.104;

  // Convert mm to steps
  long targetStepsX = targetMmX * stepsPerMmX;
  long targetStepsY = targetMmY * stepsPerMmY;

  // Calculate the absolute target positions
  long absoluteStepsX = targetStepsX;
  long absoluteStepsY = targetStepsY;

  // Move stepper to the absolute target steps
  stepperX.moveTo(absoluteStepsX);
  stepperY.moveTo(absoluteStepsY);

  // Run motors until the target position is reached
  while (stepperX.distanceToGo() != 0 || stepperY.distanceToGo() != 0) {
    stepperX.run();
    stepperY.run();
  }

  // Update current position
  currentPosX = absoluteStepsX;
  currentPosY = absoluteStepsY;

  // Set the last move time
  unsigned long lastMoveTime = millis();
  while (millis() - lastMoveTime < 7000) {
    // Laser on for 7 seconds after reaching coordinates
    digitalWrite(LASER_PIN, HIGH);
  }
  digitalWrite(LASER_PIN, LOW); // Turn off the laser after 7 seconds
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim();  // Remove unnecessary spaces

    // Split input by comma
    int commaIndex = input.indexOf(',');
    if (commaIndex > 0) {
      int pixelX = input.substring(0, commaIndex).toInt();
      int pixelY = input.substring(commaIndex + 1).toInt();

      // Move to the entered pixel coordinates
      moveToPixel(pixelX, pixelY);

      // Display the target coordinates on the Serial Monitor
      Serial.print("Pindah ke piksel: ");
      Serial.print(pixelX);
      Serial.print(", ");
      Serial.println(pixelY);
    } else {
      Serial.println("Format input salah. Masukkan dalam format X,Y.");
    }
  }
}
