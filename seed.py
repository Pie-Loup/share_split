import mnemonic
### this file should help make sure the seed phrase is entered correctly
### by checking the public address of the reconstructed shares

# This is an example seed phrase
seed_phrase = "abandon abandon ability able about above absent absorb abstract absurd abuse access accident account accuse achieve acquire across act action actor actual adapt addactual adapt add ealkzfnmaezlkfnmaekzfjbnm emzkajfbnaemzkbfj"

# Generate the private key from the seed phrase
private_key = mnemonic.Mnemonic.to_seed(seed_phrase).hex()

# Print the private key
print(private_key)
