from collections import Counter
import math

# Frequency of English letters
ENGLISH_FREQ = {
    'A': 8.12, 'B': 1.49, 'C': 2.71, 'D': 4.32, 'E': 12.02,
    'F': 2.30, 'G': 2.03, 'H': 5.92, 'I': 7.31, 'J': 0.10,
    'K': 0.69, 'L': 3.98, 'M': 2.61, 'N': 6.95, 'O': 7.68,
    'P': 1.82, 'Q': 0.11, 'R': 6.02, 'S': 6.28, 'T': 9.10,
    'U': 2.88, 'V': 1.11, 'W': 2.09, 'X': 0.17, 'Y': 2.11, 'Z': 0.07
}

def decrypt_vigenere(ciphertext, key):
    plaintext = ''
    key = key.upper()
    key_len = len(key)
    for i, c in enumerate(ciphertext):
        if c.isalpha():
            shift = ord(key[i % key_len]) - ord('A')
            decrypted_char = chr((ord(c) - ord('A') - shift) % 26 + ord('A'))
            plaintext += decrypted_char
        else:
            plaintext += c
    return plaintext

def score_english_likeness(text):
    text = ''.join(filter(str.isalpha, text.upper()))
    if not text:
        return 0
    freq = Counter(text)
    total = sum(freq.values())
    score = 0
    for char in ENGLISH_FREQ:
        observed = (freq[char] / total) * 100 if total > 0 else 0
        expected = ENGLISH_FREQ[char]
        score += (observed - expected) ** 2
    return -score  # Lower score = better match, so we return negative

def split_columns(ciphertext, key_len):
    columns = ['' for _ in range(key_len)]
    for i, c in enumerate(ciphertext):
        if c.isalpha():
            columns[i % key_len] += c
    return columns

def best_shift_for_column(column):
    best_shift = 0
    best_score = float('-inf')
    for shift in range(26):
        decrypted = ''.join(chr((ord(c) - ord('A') - shift) % 26 + ord('A')) for c in column)
        score = score_english_likeness(decrypted)
        if score > best_score:
            best_score = score
            best_shift = shift
    return best_shift

def predict_key(ciphertext, max_key_len=12):
    ciphertext = ''.join(filter(str.isalpha, ciphertext.upper()))
    best_key = ''
    best_score = float('-inf')
    for key_len in range(1, max_key_len + 1):
        columns = split_columns(ciphertext, key_len)
        key = ''
        for col in columns:
            shift = best_shift_for_column(col)
            key += chr(shift + ord('A'))
        decrypted = decrypt_vigenere(ciphertext, key)
        score = score_english_likeness(decrypted)
        if score > best_score:
            best_score = score
            best_key = key
    return best_key

# -------------------- DEMO ---------------------

ciphertext = "LXFOPVEFRNHR"  # Encrypted with key "LEMON"
predicted_key = predict_key(ciphertext, max_key_len=10)

print(f"Predicted Key: {predicted_key}")
print(f"Decrypted Message: {decrypt_vigenere(ciphertext, predicted_key)}")