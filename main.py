from sss_helper import get_key_choice, secure_clear, show_qr_code
from manage_seed import create_share_from_seed, rebuild_seed_from_shares
from protect_share import encrypt, decrypt
import getpass
from seed import show_public_addresses

class InvalidTag(Exception):
    pass

print("Hello there. What do you want to do?")
print("1. Create shares from a seed phrase")
print("2. Rebuild a seed phrase from shares")
print("3. Encrypt a share protected with a password")
print("4. Decrypt a share to protect it with a password")
action = get_key_choice(['1'], ['2'], ['3'], ['4'])
if action == 1:
    seed_phrase = getpass.getpass("Enter seed phrase, then press Enter: ")
    required_shares = int(input("Enter the number of shares required to reconstruct the seed: "))
    total_shares = int(input("Enter the total number of shares: "))

    print("Do you want to show the corresponding public addresses? (y/n)")
    result_verify = get_key_choice(['y'], ['n'])
    if result_verify == 1:
        show_public_addresses(seed_phrase)

    shares = create_share_from_seed(seed_phrase, required_shares, total_shares)

    password = getpass.getpass("Enter password to encrypt the shares, leave empty to skip: ")
    encrypted_shares = []
    for share in shares:
        encrypted_shares.append(encrypt(password, share))
    if password!='':
        password = getpass.getpass("Re-enter password to confirm: ")
        print("Encrypting shares")
    decrypted_shares = []
    for encrypted_share in encrypted_shares:
        try:
            decrypted_shares.append(decrypt(password, encrypted_share))
        except InvalidTag as e:
            print(f"Error while decoding, wrong password supplied?: {e}")
            break
        
    try:
        assert decrypted_shares == shares
        print("Shares encrypted successfully")
    except AssertionError:
        print("Error: Decryption failed")
        exit(1)
        
    print("Do you want to show the shares? (y/n)")
    result_show = get_key_choice(['y'], ['n'])
    if result_show == 1:
        for i, encrypted_share in enumerate(encrypted_shares):
            print(f"Share {i + 1}: {encrypted_share}")
            print("Do you want to show the QR code for this share? (y/n)")
            result_qr = get_key_choice(['y'], ['n'])
            if result_qr == 1:
                show_qr_code(encrypted_share)
    print("Press any key to flush the terminal")
    get_key_choice()
    secure_clear()
elif action == 2:
    input_shares = []
    print("Enter the shares, one by one. Press enter when you are finished.")
    i = 1
    while True:
        share = input(f"Enter share {i}: ")
        if share == '':
            break
        input_shares.append(share)
        i += 1
    password = getpass.getpass("Enter password to decrypt the shares, leave empty if they are not encrypted: ")
    decrypted_shares = []
    if password != '':
        for input_share in input_shares:
            try:
                decrypted_shares.append(decrypt(password, input_share))
            except ValueError as e:
                print(f"Error while decoding: {e}")
                exit(1)
    else:
        decrypted_shares = input_shares

    recovered_secret = rebuild_seed_from_shares(decrypted_shares, len(decrypted_shares), 15)
    if recovered_secret is not None:
        print("Do you want to show the secret? (y/n)")
        result_secret = get_key_choice(['y'], ['n'])
        if result_secret == 1:
            print(recovered_secret)
        print("Press any key to flush the terminal")
    else:
        print("Make sure you have entered enough shares and that all the shares are from the same set")


    get_key_choice()
    secure_clear()

elif action == 3:
    encrypted_share = input("Enter the encrypted share: ")
    password = getpass.getpass("Enter password to decrypt the share: ")
    decrypted_share = decrypt(password, encrypted_share)
    print(f"Decrypted share: {decrypted_share}")
    print("Press any key to flush the terminal")
    get_key_choice()
    secure_clear()

elif action == 4:
    clear_share = input("Enter the clear share: ")
    password = getpass.getpass("Enter password to encrypt the share: ")
    encrypted_share = encrypt(password, clear_share)
    print(f"Encrypted share: {encrypted_share}")
    print("Press any key to flush the terminal")
    get_key_choice()
    secure_clear()
