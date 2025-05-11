#define _POSIX_C_SOURCE 199309L
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "aes.h" 
typedef struct AES_ctx AES_ctx;    // from Tiny-AES-c (aes.h/aes.c)

static inline uint64_t diff_ns(const struct timespec *a, const struct timespec *b) {
    return (uint64_t)(b->tv_sec - a->tv_sec)*1000000000ULL + (b->tv_nsec - a->tv_nsec);
}

// PRESENT-80 S-box and P-layer tables
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

// Generate the 32 x 64-bit round keys from an 80-bit key
static void generate_round_keys(uint8_t rk[32][8], const uint8_t K[10]) {
    uint8_t state[10];
    memcpy(state, K, 10);
    for(int round = 1; round <= 32; round++) {
        memcpy(rk[round-1], state, 8);
        uint8_t tmp[10];
        for(int i=0;i<10;i++) tmp[i] = state[(i+7)%10];
        // S-box on high nibble
        tmp[0] = (uint8_t)((SBOX[tmp[0]>>4]<<4) | (tmp[0]&0x0F));
        // XOR round counter
        tmp[1] ^= (uint8_t)(round & 0x1F) << 3;
        memcpy(state, tmp, 10);
    }
}

// Encrypt one 64-bit block with PRESENT-80
static void present_encrypt(uint8_t out[8], const uint8_t in[8], uint8_t rk[32][8]) {
    uint8_t st[8];
    memcpy(st, in, 8);
    for(int r=0; r<31; r++) {
        // Add round key
        for(int i=0;i<8;i++) st[i] ^= rk[r][i];
        // S-box layer
        for(int i=0;i<8;i++){
            uint8_t hi = SBOX[st[i]>>4], lo = SBOX[st[i]&0x0F];
            st[i] = (hi<<4)|lo;
        }
        // P-layer
        uint8_t tmp2[8] = {0};
        for(int b=0;b<64;b++){
            uint8_t bit = (st[b/8]>>(b%8)) & 1;
            int pos = PBOX[b];
            tmp2[pos/8] |= bit << (pos%8);
        }
        memcpy(st, tmp2, 8);
    }
    // Final key addition
    for(int i=0;i<8;i++) out[i] = st[i] ^ rk[31][i];
}

int main(void) {
    const int N = 1000000;            // 1 million encryptions
    volatile uint8_t black_hole = 0;  // prevent loop elision

    // Prepare AES context (zero key)
    AES_ctx aes_ctx;
    uint8_t key128[16] = {0};
    AES_init_ctx(&aes_ctx, key128);

    // Prepare PRESENT keys (zero key)
    uint8_t key80[10] = {0}, rk80[32][8];
    generate_round_keys(rk80, key80);

    // Buffers
    uint8_t pt8[8], ct8[8], pt16[16];

    // PRESENT benchmark
    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);
    for(int i=0;i<N;i++){
        for(int j=0;j<8;j++) pt8[j] = rand() & 0xFF;
        present_encrypt(ct8, pt8, rk80);
        black_hole ^= ct8[0];
    }
    clock_gettime(CLOCK_MONOTONIC, &t1);
    double dt = diff_ns(&t0,&t1)/1e9;
    double rateP = N / dt;
    double mbP   = (8.0 * N) / dt / (1024.0*1024.0);

    // AES-128 benchmark
    clock_gettime(CLOCK_MONOTONIC, &t0);
    for(int i=0;i<N;i++){
        for(int j=0;j<16;j++) pt16[j] = rand() & 0xFF;
        AES_ECB_encrypt(&aes_ctx, pt16);
        black_hole ^= pt16[0];
    }
    clock_gettime(CLOCK_MONOTONIC, &t1);
    dt = diff_ns(&t0,&t1)/1e9;
    double rateA = N / dt;
    double mbA   = (16.0 * N) / dt / (1024.0*1024.0);

    // Print results
    printf("PRESENT : %.0f enc/s, %.2f MB/s\n", rateP, mbP);
    printf("AES-128 : %.0f enc/s, %.2f MB/s\n", rateA, mbA);

    // Use black_hole so compiler won't optimize it away
    if(black_hole == 0) printf("dummy: %02X\n", black_hole);

    return 0;
}
