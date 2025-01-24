from sslib import shamir
from itertools import permutations, combinations, product
import random
import sys
import termios
import tty
import os
import qrcode

prime_mod = 2**2203 - 1

def generate_tuples(n, min_val, max_val):
    # Create the range of numbers from min to max (inclusive)
    numbers = range(min_val, max_val + 1)
    # Generate all combinations of length n from the range
    return list(combinations(numbers, n))

def combine_tuples(list1, list2):
    result = []
    for tuple1, tuple2 in product(list1, list2):  # Iterate over all pairs of tuples
        combined = [pair for pair in zip(tuple1, tuple2)]  # Convert zip result to a list of tuples
        result.append(combined)  # Append list of tuples to the result
    return result

def select_random_shares(shares, required_shares):
    return random.sample(shares, required_shares)

def build_shares(seed_phrase, required_shares, distributed_shares):
    # Split secret into shares
    shares = []
    data = shamir.split_secret(
        seed_phrase.encode('ascii'),
        required_shares=required_shares,
        distributed_shares=distributed_shares,
        prime_mod=prime_mod

    )
    for share in data.get('shares'):
        shares.append(share[1].hex())
    return shares

def rebuild_from_hex(shares_hex, required_shares, max_shares=10):
    """
    Rebuild a secret using all possible combinations, permutations, and indices of shares.
    
    :param shares_hex: List of shares in hexadecimal format.
    :param mod_hex: Prime modulus in hexadecimal format.
    :param required_shares: Number of shares required to reconstruct the secret.
    :param max_shares: Maximum number of shares available.
    :return: Reconstructed secret if successful, otherwise None.
    """
    if required_shares > max_shares:
        raise ValueError("required_shares should be less than or equal to max_shares")
    if len(shares_hex) < required_shares:
        raise ValueError(f"Number of provided shares ({len(shares_hex)}) is less than required shares ({required_shares})")
    
    # Convert from hex to bytes
    shares_bytes = [bytes.fromhex(share) for share in shares_hex]

    possible_ranks = generate_tuples(required_shares, 1, max_shares)
    # Determine possible combinations of shares considering the required spacing
    for share_combination in combinations(shares_bytes, required_shares):
        # Try all permutations of the chosen combination
        for permuted_shares in permutations(share_combination):
            possible_orders = combine_tuples(possible_ranks, [permuted_shares])
            # Generate shares with correct starting index and spacing
            for order in possible_orders:
                data_rebuilt = {
                    'required_shares': required_shares,
                    'prime_mod': prime_mod,
                    'shares': order
                }
                try:
                    # Attempt to reconstruct the secret
                    rebuilt_secret = shamir.recover_secret(data_rebuilt).decode('ascii')
                    return rebuilt_secret  # Return the reconstructed secret if successful
                except UnicodeDecodeError:
                    continue  # If decoding fails, try the next permutation
    raise ValueError("Couldn't find a valid reconstruction")  # If no valid reconstruction is found, raise an error

def get_key_choice(*key_lists):
    """Wait for user to press a key from specified lists (returns list index + 1)
    or any key if no lists provided (returns key character)."""
    
    # Check if any key should be accepted
    any_key_mode = len(key_lists) == 0
    
    # Preprocess key lists if provided
    processed_lists = [[k.lower() for k in lst] for lst in key_lists] if not any_key_mode else []
    
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    
    try:
        tty.setcbreak(fd)
        while True:
            key = sys.stdin.read(1).lower()
            
            if any_key_mode:
                return key  # Return pressed character if in any-key mode
                
            for i, keys in enumerate(processed_lists):
                if key in keys:
                    return i + 1  # Return list index + 1 for matches
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def show_qr_code(data):
    qr = qrcode.QRCode()
    qr.add_data(data)
    qr.make()
    qr.print_ascii()

def secure_clear():
    """Multiple-pass clear of the terminal screen."""
    for _ in range(3):
        # Write over screen with blank lines
        print('\n' * os.get_terminal_size().lines, end='')
        # Use escape sequences
        sys.stdout.write('\033[2J\033[3J\033[H')
        sys.stdout.flush()
    # Finally do a system clear
    os.system('clear || cls || :')