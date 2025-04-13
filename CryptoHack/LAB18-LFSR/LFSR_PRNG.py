import multiprocessing
from itertools import product


TAPS_R1 = [2, 7]
TAPS_R2 = [5, 11]

def lfsr_next(state, taps, width):
    feedback = 0
    for t in taps:
        feedback ^= (state >> t) & 1
    state = ((state << 1) | feedback) & ((1 << width) - 1)
    return state, state & 1

def generate_keystream(r1_state, r2_state, num_bytes):
    r1_bits = []
    r2_bits = []
    for _ in range(num_bytes * 8):
        r1_state, r1_bit = lfsr_next(r1_state, TAPS_R1, 12)
        r2_state, r2_bit = lfsr_next(r2_state, TAPS_R2, 19)
        r1_bits.append(r1_bit)
        r2_bits.append(r2_bit)

    keystream = []
    for i in range(num_bytes):
        r1_byte = sum(r1_bits[i*8+j] << (7-j) for j in range(8))
        r2_byte = sum(r2_bits[i*8+j] << (7-j) for j in range(8))
        keystream.append((r1_byte + r2_byte) % 255)
    return keystream

def init_globals(counter_, total_):
    global counter, total
    counter = counter_
    total = total_

def check_combination(args):
    r1, r2, ciphertext, known_plaintext = args

    ks = generate_keystream(r1, r2, len(ciphertext))
    decrypted = bytes(c ^ k for c, k in zip(ciphertext, ks))

    with counter.get_lock():
        counter.value += 1
        if counter.value % 100000 == 0:
            percent = (counter.value / total.value) * 100
            print(f"\r[=] Checked: {counter.value}/{total.value} ({percent:.2f}%)", end="", flush=True)

    if decrypted == known_plaintext:
        print(f"\n[+] Found match! R1: {bin(r1)}, R2: {bin(r2)}")
        return (r1, r2)
    return None

def main():
    plaintext = bytes.fromhex("89504E470D0A1A0A")
    ciphertext = bytes.fromhex("6015F55B46A5B41C")

    # Shared counters
    counter = multiprocessing.Value('i', 0)
    total = multiprocessing.Value('i', ((1 << 12) - 1) * ((1 << 19) - 1))

    print(f"[i] Total combinations: {total.value}")

    # Generator for combinations
    tasks = (
        (r1, r2, ciphertext, plaintext)
        for r1 in range(1, 1 << 12)
        for r2 in range(1, 1 << 19)
    )

    with multiprocessing.Pool(initializer=init_globals, initargs=(counter, total)) as pool:
        for result in pool.imap_unordered(check_combination, tasks, chunksize=500):
            if result:
                r1, r2 = result
                print(f"\n[✓] Found keys: R1 = {r1:012b}, R2 = {r2:019b}")
                return

    print("\n[!] No matching state found.")

if __name__ == "__main__":
    main()
