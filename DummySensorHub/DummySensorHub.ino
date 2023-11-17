void setup() {
  Serial.begin(115200);
}

void loop() {
  while (Serial.available() == 0) {
  }

  String input = Serial.readString();
  if (input == "read") {
    char phBuffer[7];
    float randpH = rand()%14 + (float)(rand()%100)/100;
    dtostrf(randpH, 0, 3, phBuffer);
    String ph = phBuffer;
    char tempBuffer[8];
    float randTemp = rand() % 34 - 2 + (float)(rand()%100)/100;
    dtostrf(randTemp, 0, 3, tempBuffer);
    String temp = tempBuffer;
    char dissolvedOxygenBuffer[8];
    float randDissolvedOxygen = rand() % 401 + (float)(rand()%100)/100;
    dtostrf(randDissolvedOxygen, 0, 3, dissolvedOxygenBuffer);
    String dissolvedOxygen = dissolvedOxygenBuffer;
    String pressure = String(rand() % 9026);
    String msg =
        ph + "&" + temp + "&" + dissolvedOxygen + "&" + pressure + "\0";
    Serial.println(msg);
  }
  else if(input == "SysCheck") {
    Serial.println("1111");
  }
}
