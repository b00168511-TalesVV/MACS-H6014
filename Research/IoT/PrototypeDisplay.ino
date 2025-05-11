#include <Arduino.h>
#include <Wire.h>
#include <ESP8266WiFi.h>            // for ESP.getCycleCount()
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <string.h>                 // for memcpy
#include "aes.h"                    // tiny-AES-c header

// I2C pins for onboard OLED
#define SDA_PIN 14  // D6 = GPIO12
#define SCL_PIN 12  // D5 = GPIO14

// OLED setup
#define SCREEN_W 128
#define SCREEN_H 64
Adafruit_SSD1306 display(SCREEN_W, SCREEN_H, &Wire);

// PRESENT-80 S-box and P-layer (unchanged) …
static const uint8_t SBOX[16] = {
  0xC,0x5,0x6,0xB,0x9,0x0,0xA,0xD,
  0x3,0xE,0xF,0x8,0x4,0x7,0x1,0x2
};
static const uint8_t PBOX[64] = {
     0,16,32,48, 1,17,33,49,
     2,18,34,50, 3,19,35,51,
     4,20,36,52, 5,21,37,53,
     6,22,38,54, 7,23,39,55,
     8,24,40,56, 9,25,41,57,
    10,26,42,58,11,27,43,59,
    12,28,44,60,13,29,45,61,
    14,30,46,62,15,31,47,63
};

// Key expansion & encrypt routines (unchanged) …
static void generate_round_keys(uint8_t rk[32][8], const uint8_t K[10]) {
  uint8_t state[10];
  memcpy(state, K, 10);
  for(int round = 1; round <= 32; round++) {
    memcpy(rk[round-1], state, 8);
    uint8_t tmp[10];
    for(int i = 0; i < 10; i++) tmp[i] = state[(i + 7) % 10];
    tmp[0] = (uint8_t)((SBOX[tmp[0] >> 4] << 4) | (tmp[0] & 0x0F));
    tmp[1] ^= (uint8_t)(round & 0x1F) << 3;
    memcpy(state, tmp, 10);
  }
}

static void present_encrypt(uint8_t out[8], const uint8_t in[8], uint8_t rk[32][8]) {
  uint8_t st[8];
  memcpy(st, in, 8);
  for(int r = 0; r < 31; r++) {
    for(int i = 0; i < 8; i++) st[i] ^= rk[r][i];
    for(int i = 0; i < 8; i++) {
      uint8_t hi = SBOX[st[i] >> 4], lo = SBOX[st[i] & 0x0F];
      st[i] = (hi << 4) | lo;
    }
    uint8_t tmp2[8] = {0};
    for(int b = 0; b < 64; b++) {
      uint8_t bit = (st[b/8] >> (b%8)) & 1;
      int pos = PBOX[b];
      tmp2[pos/8] |= bit << (pos%8);
    }
    memcpy(st, tmp2, 8);
  }
  for(int i = 0; i < 8; i++) out[i] = st[i] ^ rk[31][i];
}

// Globals
uint8_t rk80[32][8];
uint8_t K80[10] = {0};
AES_ctx aes_ctx;
uint8_t K128[16] = {0};
volatile uint8_t black_hole;
uint8_t pt8[8], ct8[8], pt16[16];

void setup() {
  Serial.begin(115200);
  delay(100);

  // Init I²C & OLED
  Wire.begin(SDA_PIN, SCL_PIN);
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("OLED init failed");
    while (1);
  }
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0,0);
  display.println("Benchmarking...");
  display.display();
  delay(500);

  // Prepare keys
  black_hole = 0;
  AES_init_ctx(&aes_ctx, K128);
  generate_round_keys(rk80, K80);

  const int N = 50000;
  uint32_t t0, dt;
  float rateP, rateA;

  // --- PRESENT-80 benchmark ---
  t0 = ESP.getCycleCount();
  for (int i = 0; i < N; i++) {
    for (int j = 0; j < 8; j++) pt8[j] = random(256);
    present_encrypt(ct8, pt8, rk80);
    black_hole ^= ct8[0];
    yield();
  }
  dt = ESP.getCycleCount() - t0;
  rateP = N / (dt / 80e6f);

  // --- AES-128 benchmark ---
  t0 = ESP.getCycleCount();
  for (int i = 0; i < N; i++) {
    for (int j = 0; j < 16; j++) pt16[j] = random(256);
    AES_ECB_encrypt(&aes_ctx, pt16);
    black_hole ^= pt16[0];
    yield();
  }
  dt = ESP.getCycleCount() - t0;
  rateA = N / (dt / 80e6f);

  // --- Display on OLED ---
  display.clearDisplay();
  // Line 1
  display.setCursor(0,  0);
  display.print("PRESENT: ");
  display.print((int)rateP);
  display.print(" e/s");
  // Line 2 (y = 8px)
  display.setCursor(0,  8);
  display.print("AES128  : ");
  display.print((int)rateA);
  display.print(" e/s");
  // Line 3 (y = 16px)
  char buf[10];
  sprintf(buf, "0x%02X", black_hole);
  display.setCursor(0, 16);
  display.print("dummy  : ");
  display.print(buf);

  display.display();

  // Also send to Serial
  Serial.printf("PRESENT: %.0f enc/s\n", rateP);
  Serial.printf("AES128  : %.0f enc/s\n", rateA);
  Serial.printf("dummy  : %s\n", buf);
}

void loop() {
  // nothing to do
}
