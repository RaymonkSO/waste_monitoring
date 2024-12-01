#include <RTClib.h>
#include <GxEPD2_BW.h>
#include <Fonts/FreeMonoBold9pt7b.h>
#include <SPI.h>
#include <MFRC522.h>
#include "WiFiEsp.h"
#include "ThingSpeak.h"
#include  "TimeLib.h"
#include <Servo.h>

#define SERVO_PIN 2
#define ESP_BAUDRATE 115200
// Define the display and its pins
#define ENABLE_GxEPD2_GFX 0
#define MAX_DISPLAY_BUFFER_SIZE 800
#define MAX_HEIGHT(EPD) (EPD::HEIGHT <= MAX_DISPLAY_BUFFER_SIZE / (EPD::WIDTH / 8) ? EPD::HEIGHT : MAX_DISPLAY_BUFFER_SIZE / (EPD::WIDTH / 8))

#define SS_PIN 53
#define RST_PIN 5

MFRC522 mfrc522(SS_PIN, RST_PIN);
Servo myservo;

Servo objServo;

const int trigPin = 30;
const int echoPin = 32;
const int sensorPin = A0; // Analog input pin connected to the sensor
RTC_DS1307 rtc;
int count = 2;
int flag = 0;
const int tempSensorPin = A2; // Analog pin for temperature sensor
const int reflectiveSensorPin = A1; // Analog pin for reflective optical sensor
const int redLed1 = 11; // Digital pin for the first red LED
const int redLed2 = 12; // Digital pin for the second red LED
const int redLed3 = 13; // Digital pin for the third red LED
const float tempThreshold1 = 40.0; // Temperature threshold in Celsius for one red LED
const float tempThreshold2 = 50.0; // Temperature threshold in Celsius for two red LEDs
const float tempThreshold3 = 65.0; // Temperature threshold in Celsius for three red LEDs
const int reflectiveThreshold = 500; // Reflective threshold (adjust as needed)

const int FILL = A3;
const int PRES = A4;

bool card1Detected = false; // Flag to track if specific card is detected
int countCard2 = 0; // Counter for the second card
const byte cardID1[4] = {0xFC, 0x81, 0x2E, 0x18}; // Specific RFID card ID
const byte cardID2[4] = {0xD1, 0x2C, 0x37, 0x19}; // Second card's RFID

int unlockAngle = 0; // Angle to unlock the door
int lockAngle = 90; // Angle to lock the door


char ssid[] = "EE3070_P1615_1"; 
char pass[] = "EE3070P1615"; 
int status = WL_IDLE_STATUS; // the Wifi radio's status
WiFiEspClient client; //create a wifi client

long ChannelNumber;
char * WriteAPIKey;


void setup() {
  objServo.attach(SERVO_PIN);
  //Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  
  pinMode(redLed1, OUTPUT);
  pinMode(redLed2, OUTPUT);
  pinMode(redLed3, OUTPUT);

  pinMode(PRES, OUTPUT);
  pinMode(FILL, INPUT);
  analogWrite(PRES,0);
  analogWrite(FILL,0);
  delay(500);
  SPI.begin();
  mfrc522.PCD_Init();
  myservo.attach(6); // Using pin 9 for servo control
  myservo.write(lockAngle); // Initialize servo to lock position
  Serial.begin(115200);
  Serial1.begin(ESP_BAUDRATE);
  WiFi.init(&Serial1);
  if(WiFi.status() != WL_CONNECTED){
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    while(WiFi.status() != WL_CONNECTED){
      WiFi.begin(ssid, pass); // Connect to WPA/WPA2 network
      Serial.print(".");
      delay(1000);
    }
  }
  ThingSpeak.begin(client); // Initialize ThingSpeak
   // Wait to stabilize*/
}

void loop() {
  long startMillis = millis();
  int area = 100;
  int height = 30;
  float fill = (height - distance()) / 19.5 * 100;
  float weight =press() / 10;
  if(weight < 0)
    weight = 0;
  if(fill < 0)
    fill = 0;
  if(fill > 100)
    fill = 100;
  analogWrite(PRES,int(weight*10));
  analogWrite(FILL,int(fill));
  Serial.println(weight);
  Serial.println(fill);

  if(fill > 90 && flag == 0){
    close();
    flag = 1;
  }
  else if(fill < 90 && flag == 1){
    open();
    flag = 0;
  }
  
  if (count >= 2){
    setdata(weight,1);
    setdata(fill,2);
    while(upload() != 200){
      delay(15000);
      setdata(weight,1);
      setdata(fill,2);
    }
    count = 1;
  }
  else 
    count ++;

  while (millis() - startMillis <= 60000)  //test whether the period has elapsed
  {
    int x = rfid();
    if(x != 0){
      if(upload() != 200)
        setdata(x,3);
    }
    if(fire() == 1){
      //spray
    }
    
  }
  

}

float distance(){
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  long duration = pulseIn(echoPin, HIGH);
  float distance = duration * 0.034 / 2;
  Serial.print("distance : ");
  Serial.println(distance);
  return distance;
  
}


float press(){
  int sensorValue = analogRead(sensorPin); 
  float voltage = sensorValue * (5.0 / 1023.0); 
  float pressure = (voltage - 0.5) * 100.0; 
  return pressure;
}



void setdata(float data, int n) {
  //n = {weight, distance,rfid}
  ChannelNumber = 2669837;
  WriteAPIKey = "W4UABP4XTRAT17SC";
    ThingSpeak.setField(n, data); 
}

int upload(){
  int x = ThingSpeak.writeFields(ChannelNumber, WriteAPIKey);
  if(x == 200){
    Serial.println("Channel update successful.");
  }
  else{
    Serial.println("Problem updating channel. HTTP error code " + String(x));
  }
  return x;
}

int fire(){
// Read the temperature sensor value
  int tempSensorValue = analogRead(tempSensorPin);

  // Convert the analog reading to voltage (0-5V)
  float voltage = tempSensorValue * (5.0 / 1023.0);

  // Convert the voltage to temperature in Celsius
  // For LM35, the output voltage is 10mV per °C
  float temperatureC = voltage * 100.0;

  // Read the reflective optical sensor value
  int reflectiveSensorValue = analogRead(reflectiveSensorPin);

  // Print the sensor readings to the serial monitor
  //Serial.print("Temperature: ");
  //Serial.print(temperatureC);
  //Serial.print(" °C, Reflective Value: ");
  //Serial.println(reflectiveSensorValue);

  // Check if the temperature exceeds the thresholds or if the reflectivity indicates smoke
  if (temperatureC > tempThreshold3) {
    // Turn on all three red LEDs
    digitalWrite(redLed1, HIGH);
    digitalWrite(redLed2, HIGH);
    digitalWrite(redLed3, HIGH);
    return 1;
  } else if (temperatureC > tempThreshold2) {
    // Turn on two red LEDs
    digitalWrite(redLed1, HIGH);
    digitalWrite(redLed2, HIGH);
    digitalWrite(redLed3, LOW);
} else if (temperatureC > tempThreshold1) {
    // Turn on one red LED
    digitalWrite(redLed1, HIGH);
    digitalWrite(redLed2, LOW);
    digitalWrite(redLed3, LOW);
  } else if (reflectiveSensorValue > reflectiveThreshold) {
    // Turn on one red LED (indicating smoke detection)
    digitalWrite(redLed1, HIGH);
    digitalWrite(redLed2, HIGH);
    digitalWrite(redLed3, HIGH);
  } else {
    // Turn off all red LEDs
    digitalWrite(redLed1, LOW);
    digitalWrite(redLed2, LOW);
    digitalWrite(redLed3, LOW);
  }

  // Wait for a short period before the next reading
  return 0;
}

void open(){
  objServo.writeMicroseconds(1150);
  delay(1500);
  objServo.writeMicroseconds(1500);
}

void close(){
  objServo.writeMicroseconds(1850);
  delay(1500);
  objServo.writeMicroseconds(1500);
}

int rfid() {
  //Serial.println("RFID test");
  if (!mfrc522.PICC_IsNewCardPresent()) {
    return 0;
  }
  if (!mfrc522.PICC_ReadCardSerial()) {
    return 0;
  }

  byte cardID[4];
  for (byte i = 0; i < 4; i++) {
    cardID[i] = mfrc522.uid.uidByte[i];
  }

  if (memcmp(cardID, cardID1, 4) == 0) {
    if (!card1Detected) {
      // Specific card detected for the first time
      Serial.println("Spcific RFID card detected. Unlocking the door.");
      myservo.write(unlockAngle); // Unlock the door
      card1Detected = true;
      setdata(1,3);
      delay(1000);
      return 1;
    } else {
      // Specific card detected again
      Serial.println("Specific RFID card detected again. Locking the door.");
      myservo.write(lockAngle); // Lock the door
      delay(1000);
      card1Detected = false; // Reset flag for the next detection
    }
  } 
  else {
    Serial.println("Unknown card. Access denied.");
  }

  return 0;
}


