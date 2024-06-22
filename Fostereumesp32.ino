#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#define soil_moisture_pin 2
//All comments are written by Mahya Byantara
// Replace with your network credentials
const char* ssid = "SKHOOD 5G EXT";
const char* password = "Bismillah1378";

const char* serverName = "http://192.168.4.149:5000/post"; // Replace with your machine's local IP address

DHT dht(26, DHT11);

void setup() {
  Serial.begin(115200);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println();
  Serial.println("Connected to WiFi");

  // Initialize the DHT sensor
  dht.begin();
}

void loop() {
  // Read temperature and humidity values
  float temperatur = dht.readTemperature();
  float humidity = dht.readHumidity();

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    // Specify request destination
    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");

    // Create JSON payload
    String jsonPayload = "{\"temp\":" + String(temperatur) + ",\"hum\":" + String(humidity) + "}";

    // Send HTTP POST request
    int httpResponseCode = http.POST(jsonPayload);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
      Serial.print("Response: ");
      Serial.println(response);
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
      Serial.print("Error description: ");
      Serial.println(http.errorToString(httpResponseCode).c_str());
    }

    http.end();
  } else {
    Serial.println("Error in WiFi connection");
  }

  // Print sensor values to the Serial Monitor
  Serial.print("Temperature: ");
  Serial.print(temperatur);
  Serial.print(" C ");
  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.print(" % ");
  Serial.print("Moisture: ");
  Serial.println(analogRead(soil_moisture_pin));

  // Wait for 2 seconds before the next loop
  delay(2000);
}
