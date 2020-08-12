#include <WiFi.h>
#include <IOXhop_FirebaseESP32.h>
#define FIREBASE_HOST "manisir-84cd8.firebaseio.com" 
#define FIREBASE_AUTH "ReiazJsk0Tna5G10dYXk0smosv1GH4FN14FwuSW5"
#define WIFI_SSID "vivo V9 1723"
#define WIFI_PASSWORD "esp32devkitv1"
//------------DEFINING PINS---------
int relayPin = 23;
const int currentPin = 33;//ADC2 PIN
const int ldrPin = 32;//ADC2 PIN
//----------------------------------
const int voltage=12;//DC power supply
int sensitivity = 185;//5A ACS712
int offsetVoltage = 2500;//5000mV/2
//----------------------------------
int adcValue= 0;
double adcVoltage = 0;
double currentValue = 0;
float power=0.0;
String toggle="";
float maxcurrent=0.0,mincurrent=0.0,finalcurrent=0.0;
//----------------------------------
void setup() {
  pinMode(ldrPin, INPUT);
  pinMode(relayPin, OUTPUT);
  Serial.begin(9600);
  delay(2000);
  
  WiFi.begin(WIFI_SSID,WIFI_PASSWORD);
  Serial.print("Connecting to..");
  Serial.print(WIFI_SSID);
  while (WiFi.status() != WL_CONNECTED) 
  {
    Serial.print(".");
    delay(500);
   }
  Serial.println();
  Serial.print("Connected to ");
  Serial.println(WIFI_SSID);
  Serial.print("IP Address is : ");
  Serial.println(WiFi.localIP());//print local IP address
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  check();   
  
}

void loop() 
{
   
    toggle=Firebase.getString("Toggle");
    Serial.println(toggle);
    int ldrStatus = analogRead(ldrPin);
    if (isnan(ldrStatus)) 
    {
      Serial.println("Failed to read from LDR sensor!");
      return;
    }
    if(toggle =="Auto")
    {
       if(ldrStatus>800)//bright -> turn OFF the lights
        {
          Serial.print("Light Intensity ");//printing the intensity of light
          Serial.println(ldrStatus);
          digitalWrite(relayPin, LOW); //deactivating the relay
          Serial.println("Light OFF"); 
          power =0;
          Serial.print("Power(W)");//printing power
          Serial.println(power);
          Firebase.set("/Power",power);
        }
       else//dark ->turn ON the lights
        {
          Serial.print("Light Intensity ");
          Serial.println(ldrStatus);
          digitalWrite(relayPin, HIGH);
          Serial.println("Light ON");
          finalcurrent=abs(maxcurrent-mincurrent);
          Serial.print("\t Final Current(A) = ");
          Serial.println(finalcurrent,3);
          power=voltage*finalcurrent;
          Serial.print("\t Power(W) = ");
          Serial.println(power,3);
          Firebase.set("/Power",power);
        }
    }
    else if(toggle == "On")
    {
      Serial.print("Light Intensity ");
      Serial.println(ldrStatus);
      digitalWrite(relayPin, HIGH);
      Serial.println("Light ON");
      finalcurrent=abs(maxcurrent-mincurrent);
      Serial.print("\t Final Current(A) = ");
      Serial.println(finalcurrent,3);
      power=voltage*finalcurrent;
      Serial.print("\t Power(W) = ");
      Serial.println(power,3);
      Firebase.set("/Power",power);
    }
    else if(toggle == "Off")
    {
      Serial.print("Light Intensity ");
      Serial.println(ldrStatus);
      digitalWrite(relayPin, LOW); 
      Serial.println("Light OFF"); 
      power = 0;
      Serial.print("Power(W)");
      Serial.println(power);
      Firebase.set("/Power",power);
    }
  
  delay(2000);
 }
float calculations()
{
  float Samples=0.0,AcsValue=0.0,AvgAcs=0.0;
  for (int x = 0; x < 150; x++)//Get 150 samples
  { 
  AcsValue = analogRead(currentPin);//Reads current sensor values   
  Samples = Samples + AcsValue;  //Adds samples together
  delay (3); // lets ADC settle before next sample with a time gap of 3ms
  }
  AvgAcs=Samples/150.0;//Taking Average of 150 samples
  adcVoltage = (AvgAcs / 4096) * 3300;//0-4095 being range sensed by ESP32(12 bit resolution of the analog pins)
  currentValue = abs((adcVoltage - offsetVoltage) / sensitivity);
  Serial.print("Raw Sensor Value = " );
  Serial.print(AvgAcs);
  Serial.print("\t Voltage(mV) = ");
  Serial.print(adcVoltage,3);
  Serial.print("\t Current = ");
  Serial.println(currentValue,3);
  return(currentValue);
}
float check()
{
  digitalWrite(relayPin,HIGH);
  maxcurrent = calculations();
  delay(500);
  digitalWrite(relayPin,LOW);
  mincurrent = calculations();
  delay(500);
}
