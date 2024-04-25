#include <WiFi.h>
#include <HTTPClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// WiFi credentials
const char* ssid = "compost360";
const char* password = "dayalbagh";

// ThingSpeak settings
const char* server = "api.thingspeak.com";
const String apiKey = "your api";

// Pins for sensors
const int ds18b20Pin = 4; // GPIO 4
const int soilMoisturePin = 32; // Analog pin for soil moisture sensor

// LED pin
const int ledPin = 2; // GPIO 2

// Define deep sleep time in seconds
const uint64_t deepSleepTime = 10 * 60 * 1000000; // 10 minutes in microseconds

// Create instances for DS18B20 sensor and OneWire bus
OneWire oneWire(ds18b20Pin);
DallasTemperature sensors(&oneWire);

// Variables to store data offline
float offlineTemperature = 0.0;
int offlineSoilMoisture = 0;

// Maximum number of WiFi connection attempts
const int maxConnectionAttempts = 30; // 30 attempts, each attempt 1 second apart

// Function to read soil moisture
int readSoilMoisture() {
  int sensor_analog = analogRead(soilMoisturePin);
  int moisture = (100 - ((sensor_analog / 4095.00) * 100));
  return moisture;
}

// Function to read temperature from DS18B20
float readTemperature() {
  sensors.requestTemperatures();
  return sensors.getTempCByIndex(0);
}

// Function to connect to WiFi with timeout
bool connectToWiFi() {
  Serial.print("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  int attempt = 0;
  while (WiFi.status() != WL_CONNECTED && attempt < maxConnectionAttempts) {
    delay(1000);
    Serial.print(".");
    attempt++;
  }
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("Connected!");
    return true;
  } else {
    Serial.println("Connection failed. Using offline data.");
    return false;
  }
}

// Function to send data to ThingSpeak
void sendDataToThingSpeak(float temperature, int soilMoisture) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    String url = "http://";
    url += server;
    url += "/update?api_key=";
    url += apiKey;
    url += "&field1=";
    url += String(temperature);
    url += "&field2=";
    url += String(soilMoisture);
    Serial.print("Sending data to ThingSpeak: ");
    Serial.println(url);
    http.begin(url);
    int httpCode = http.GET();
    if (httpCode > 0) {
      Serial.printf("HTTP code: %d\n", httpCode);
      if (httpCode == HTTP_CODE_OK) {
        Serial.println("Data sent successfully!");
        offlineTemperature = 0.0; // Clear offline data after successful transmission
        offlineSoilMoisture = 0;
      }
    } else {
      Serial.println("Error sending data to ThingSpeak!");
    }
    http.end();
  } else {
    Serial.println("WiFi not connected. Cannot send data to ThingSpeak!");
  }
}

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(115200);
  sensors.begin();
}

void loop() {
  // Read sensors
  float temperature = readTemperature();
  int soilMoisture = readSoilMoisture();
  
  // Attempt to connect to WiFi
  if (connectToWiFi()) {
    // Send data to ThingSpeak
    sendDataToThingSpeak(temperature, soilMoisture);
  } else {
    // Store data offline
    offlineTemperature = temperature;
    offlineSoilMoisture = soilMoisture;
  }
  
  // Blink LED to indicate the end of loop
  digitalWrite(ledPin, HIGH);
  delay(1000);
  digitalWrite(ledPin, LOW);
  delay(1000);
  
  // Enter deep sleep mode
  Serial.println("Entering deep sleep mode...");
  esp_deep_sleep(deepSleepTime);
}

