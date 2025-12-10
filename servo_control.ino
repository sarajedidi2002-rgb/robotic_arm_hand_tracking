#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
Adafruit_PWMServoDriver pca = Adafruit_PWMServoDriver();
const int PULSE_MIN = 500; // microseconds for 0
const int PULSE_MAX = 2500; // microseconds for 180
const int ANGLE_MIN = 0;
const int ANGLE_MAX = 180;
unsigned long previousMillis = 0;
int blinkInterval = 0; // in milliseconds
bool ledState = false;
void setup() {
Serial.begin(9600);
pinMode(LED_BUILTIN, OUTPUT);
pca.begin();
pca.setPWMFreq(50); // 50Hz for servos
delay(10);
}
void loop() {
if (Serial.available()) {
String data = Serial.readStringUntil('\n');
int fingers[5] = {0}; // Thumb, Index, Middle, Ring, Pinky
int index = 0;
// Parse comma-separated string into the array
while (data.length() > 0 && index < 5) {
int commaIndex = data.indexOf(',');
String value;
if (commaIndex == -1) {
value = data;
data = "";
} else {
value = data.substring(0, commaIndex);
data = data.substring(commaIndex + 1);
}
fingers[index++] = value.toInt();
}
// Update all servos based on finger status
for (int i = 0; i < 5; i++) {
if (fingers[i] == 1) {
setServoAngle(i, ANGLE_MAX); // Finger up
} else {
setServoAngle(i, ANGLE_MIN); // Finger down
}
}
// Determine blink interval based on finger priority
if (fingers[4] == 1) { // Pinky ? 5 times per second
blinkInterval = 100;
} else if (fingers[3] == 1) { // Ring ? 4 times per second
blinkInterval = 125;
} else if (fingers[2] == 1) { // Middle ? 3 times per second
blinkInterval = 167;
} else if (fingers[1] == 1) { // Index ? 2 times per second
blinkInterval = 250;
} else {
blinkInterval = 0;
digitalWrite(LED_BUILTIN, LOW);
}
}
// Handle blinking
if (blinkInterval > 0) {
unsigned long currentMillis = millis();
if (currentMillis - previousMillis >= blinkInterval) {
previousMillis = currentMillis;
ledState = !ledState;
digitalWrite(LED_BUILTIN, ledState ? HIGH : LOW);
}
}
}
void setServoAngle(uint8_t channel, int angle) {
int pulse_us = map(angle, 0, 180, PULSE_MIN, PULSE_MAX);
int pwm_val = map(pulse_us, 0, 20000, 0, 4095); // 20ms = 50Hz frame
pca.setPWM(channel, 0, pwm_val);
}
