from tinyec import registry
from hashlib import sha256

# Use a small custom curve with cofactor > 1
curve = registry.get_curve('secp192r1')  # Example: has cofactor = 1, but for demo

def compress_point(point):
    return hex(point.x) + hex(point.y % 2)[2:]

# Simulate Bob generating a normal ECDH key pair
def generate_keypair():
    priv_key = 15  # Just for demo; normally random
    pub_key = priv_key * curve.g
    return priv_key, pub_key

# Attacker crafts a point of small order
# For simulation, we brute-force a low-order point manually
def find_small_order_point(order_limit=10):
    for i in range(1, order_limit):
        point = i * curve.g
        if point != None and (order := point_order(point)) is not None and order < order_limit:
            return point, order
    return None, None

def point_order(point):
    for i in range(1, 100):
        if i * point == None:
            return i
    return None

# Simulate victim computing ECDH without validating public point
def compute_shared_secret(priv_key, received_point):
    shared_point = priv_key * received_point
    return sha256(compress_point(shared_point).encode()).hexdigest()

# --- DEMO ---

print(f"Using curve: {curve.name}")

# Step 1: Bob's keypair
bob_priv, bob_pub = generate_keypair()
print(f"Bob's Private Key: {bob_priv}")
print(f"Bob's Public Key: {compress_point(bob_pub)}")

# Step 2: Attacker finds small-order point
malicious_point, malicious_order = find_small_order_point(order_limit=100)

print(f"Malicious Point of order {malicious_order}: {compress_point(malicious_point)}")

# Step 3: Bob computes shared secret with malicious point
leaked_secret = compute_shared_secret(bob_priv, malicious_point)
print(f"Leaked Shared Secret: {leaked_secret}")

# Since order is small, there are few possible values of shared secrets:
print("\nAll possible shared secrets for this small order point:")
for k in range(malicious_order):
    test_point = k * malicious_point
    shared = sha256(compress_point(test_point).encode()).hexdigest()
    print(f"  k={k} → {shared}")