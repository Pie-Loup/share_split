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
    
    # Derive account-level xpub (e.g., m/44'/0'/0' for Bitcoin)
    bip_account = (
        Bip44.FromSeed(seed, coin)
        .Purpose()     # m/44'
        .Coin()        # m/44'/{coin_type}'
        .Account(0)    # m/44'/{coin_type}'/0'
    )
    xpub = bip_account.PublicKey().ToExtended()
    
    # Derive address (m/44'/{coin_type}'/0'/0/0)
    bip_address = (
        bip_account
        .Change(Bip44Changes.CHAIN_EXT)  # m/44'/{coin_type}'/0'/0
        .AddressIndex(0)                 # m/44'/{coin_type}'/0'/0/0
    )
    address = bip_address.PublicKey().ToAddress()
    
    return address, xpub

def show_public_addresses(seed: str, passphrase: str = "") -> str:
    if passphrase != "":
        print("passphrase protected addesses")
        # Generate Bitcoin address (BIP44 path: m/44'/0'/0'/0/0)
        btc_address, xpub_btc = generate_address(seed, Bip44Coins.BITCOIN, passphrase)
        print("Bitcoin xpub:", xpub_btc)
        print("Bitcoin Address 0:", btc_address)

        # Generate Ethereum address (BIP44 path: m/44'/60'/0'/0/0)
        eth_address, xpub_eth = generate_address(seed, Bip44Coins.ETHEREUM, passphrase)
        print("Ethereum xpub:", xpub_eth)
        print("Ethereum Address 0:", eth_address)
    print("Main addesses (not passphrase protected)")
    # Generate Bitcoin address (BIP44 path: m/44'/0'/0'/0/0)
    btc_address, xpub_btc = generate_address(seed, Bip44Coins.BITCOIN, "")
    print("Bitcoin xpub:", xpub_btc)
    print("Bitcoin Address 0:", btc_address)

    # Generate Ethereum address (BIP44 path: m/44'/60'/0'/0/0)
    eth_address, xpub_eth = generate_address(seed, Bip44Coins.ETHEREUM, "")
    print("Ethereum xpub:", xpub_eth)
    print("Ethereum Address 0:", eth_address)


# seed = "track vital video layer announce stage paddle harvest case unit donate surface tail raw draft bag immune sting tent beyond raven fold weird verify"
# eth_address_0_expected = '0xE7d017Fe2208b2f0508A313012A5C9729EE1668e'

# show_public_addresses(seed, 'testpassword123')
