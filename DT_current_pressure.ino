#include <Wire.h>
#include <Adafruit_BMP085.h>

Adafruit_BMP085 bmp;
int sensorTA12 = A0; // Analog input pin that sensor is attached to
float nVPP;   // Voltage measured across resistor
float nCurrThruResistorPP; // Peak Current Measured Through Resistor
float nCurrThruResistorRMS; // RMS current through Resistor
float nCurrentThruWire;     // Actual RMS current in Wire

void setup() 
 {
   Serial.begin(9600); 
   pinMode(sensorTA12, INPUT);
        if (!bmp.begin()) {
   Serial.println("check bmp sensor");
   while (1) {}
  }
 }
 
 
 void loop() 
 {
   
     Serial.print(0.01*bmp.readPressure());
     Serial.print(",");
  
   nVPP = getVPP();
   

   
   nCurrThruResistorPP = (nVPP/200.0) * 1000.0;
   

   nCurrThruResistorRMS = nCurrThruResistorPP * 0.707;
   

   nCurrentThruWire = nCurrThruResistorRMS * 1000;

   


 
   Serial.print(nCurrentThruWire);

   
   Serial.println();
    
   
   

 }


 
float getVPP()
{
  float result;
  int readValue;             //value read from the sensor
  int maxValue = 0;          // store max value here
   uint32_t start_time = millis();
   while((millis()-start_time) < 500) //sample for 1 Sec
   {
       readValue = analogRead(sensorTA12);
       // see if you have a new maxValue
       if (readValue > maxValue) 
       {
           /*record the maximum sensor value*/
           maxValue = readValue;
       }
   }
   
   // Convert the digital data to a voltage
   result = (maxValue * 5.0)/1024.0;
  
   return result;
 }
