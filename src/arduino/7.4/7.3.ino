int red = 6;
int green = 5;
int blue = 3;

void setup()
{
  pinMode(red, OUTPUT);
  pinMode(green, OUTPUT);
  pinMode(blue, OUTPUT);
}
void loop()
{
  // Each loop, get a number between 0-100
  int curr = random(0,100);
  
  setColor(245, 20, 0); 
  delay(random(150,300));

  setColor(237, 28, 0); 
  delay(random(150,300));

  setColor(230, 34, 0); 
  delay(random(150,300));

  // 1 times out of 5, brighter flicker
  if(curr<=20) {
    setColor(235, 50, 0); 
    delay(random(50,100));
  }
  
  setColor(230, 34, 0); 
  delay(random(150,250));

  setColor(237, 28, 0); 
  delay(random(150,250));
}

// Quick helper function to change the color of all 3 channels
void setColor(int redValue, int greenValue, int blueValue) {
  analogWrite(red, redValue);
  analogWrite(green, greenValue);
  analogWrite(blue, blueValue);
}
