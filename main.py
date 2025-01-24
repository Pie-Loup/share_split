from sss_helper import get_key_choice, secure_clear, show_qr_code
from manage_seed import create_share_from_seed, rebuild_seed_from_shares
from protect_share import encrypt, decrypt
import getpass
        
print("Hello there. What do you want to do?")
print("1. Create shares from a seed phrase")
print("2. Rebuild a seed phrase from shares")
print("3. Decrypt a share protected with a password")
action = get_key_choice(['1'], ['2'], ['3'])
if action == 1:
    seed_phrase = getpass.getpass("Enter seed phrase, then press Enter: ")
    required_shares = int(input("Enter the number of shares required to reconstruct the seed: "))
    total_shares = int(input("Enter the total number of shares: "))

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
        decrypted_shares.append(decrypt(password, encrypted_share))
    try:
        assert decrypted_shares == shares
        print("Shares encrypted successfully")
    except AssertionError:
        print("Error: Decryption failed, wrong password")
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
            decrypted_shares.append(decrypt(password, share))
    else:
        decrypted_shares = input_shares
    required_shares = int(input("Enter the number of shares required to rebuild the seed: "))
    max_shares = input("Enter the maximum number of shares to use, leave empty if you don't know: ")
    max_shares = int(max_shares if max_shares != '' else 10)

    recovered_secret = rebuild_seed_from_shares(input_shares, required_shares, max_shares)
    print("Do you want to show the secret? (y/n)")
    result_secret = get_key_choice(['y'], ['n'])
    if result_secret == 1:
        print(recovered_secret)
    print("Press any key to flush the terminal")
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
