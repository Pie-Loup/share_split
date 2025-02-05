from bip_utils import (
    Bip39MnemonicValidator,
    Bip39SeedGenerator,
    Bip44,
    Bip44Coins,
    Bip44Changes
)

def generate_address(mnemonic: str, coin: Bip44Coins, passphrase: str = "") -> str:
    # Validate mnemonic
    Bip39MnemonicValidator().Validate(mnemonic)
    
    # Generate seed from mnemonic
    seed = Bip39SeedGenerator(mnemonic).Generate(passphrase)
    
    # Derive path for the specified coin
    bip_obj = (
        Bip44.FromSeed(seed, coin)
        .Purpose()       # m/44'
        .Coin()          # m/44'/{coin_type}'
        .Account(0)      # m/44'/{coin_type}'/0'
        .Change(Bip44Changes.CHAIN_EXT)  # m/44'/{coin_type}'/0'/0
        .AddressIndex(0) # m/44'/{coin_type}'/0'/0/0
    )
    
    # Return the address
    return bip_obj.PublicKey().ToAddress()

def show_public_addresses(seed: str, passphrase: str = "") -> str:
    if passphrase != "":
        print("passphrase protected addesses")
        # Generate Bitcoin address (BIP44 path: m/44'/0'/0'/0/0)
        btc_address = generate_address(seed, Bip44Coins.BITCOIN, passphrase)
        print("Bitcoin Address:", btc_address)

        # Generate Ethereum address (BIP44 path: m/44'/60'/0'/0/0)
        eth_address = generate_address(seed, Bip44Coins.ETHEREUM, passphrase)
        print("Ethereum Address:", eth_address)
    print("Main addesses (not passphrase protected)")
    # Generate Bitcoin address (BIP44 path: m/44'/0'/0'/0/0)
    btc_address = generate_address(seed, Bip44Coins.BITCOIN, "")
    print("Bitcoin Address:", btc_address)

    # Generate Ethereum address (BIP44 path: m/44'/60'/0'/0/0)
    eth_address = generate_address(seed, Bip44Coins.ETHEREUM, "")
    print("Ethereum Address:", eth_address)


# seed = "track vital video layer announce stage paddle harvest case unit donate surface tail raw draft bag immune sting tent beyond raven fold weird verify"
# eth_address_0_expected = '0xE7d017Fe2208b2f0508A313012A5C9729EE1668e'

# show_public_addresses(seed, 'testpassword123')
