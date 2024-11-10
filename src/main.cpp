#include <Arduino.h>

// Definição dos pinos
int ledVerde = 8;     // LED verde conectado ao pino 8
int ledAmarelo = 9;   // LED amarelo conectado ao pino 9
int ledVermelho = 10; // LED vermelho conectado ao pino 10
int buzzerPin = A5;   // Buzzer conectado ao pino A5

// Frequências para diferentes notas (em Hz)
const int noteC = 262;  // Dó
const int noteE = 330;  // Mi
const int noteG = 392;  // Sol

void setup() {
  pinMode(ledVerde, OUTPUT);
  pinMode(ledAmarelo, OUTPUT);
  pinMode(ledVermelho, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  Serial.begin(9600);
}

void playTone(int frequency, int duration) {
  tone(buzzerPin, frequency, duration);
  delay(duration);
  noTone(buzzerPin);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    
    // Desliga todos os LEDs
    digitalWrite(ledVerde, LOW);
    digitalWrite(ledAmarelo, LOW);
    digitalWrite(ledVermelho, LOW);

    if (command == 'a') {
      digitalWrite(ledVerde, HIGH);
      playTone(noteC, 200);  // Toca Dó por 200ms
      Serial.println("LED verde ligado");
    } 
    else if (command == 'b') {
      digitalWrite(ledAmarelo, HIGH);
      playTone(noteE, 200);  // Toca Mi por 200ms
      Serial.println("LED amarelo ligado");
    } 
    else if (command == 'c') {
      digitalWrite(ledVermelho, HIGH);
      playTone(noteG, 200);  // Toca Sol por 200ms
      Serial.println("LED vermelho ligado");
    }
  }
}