from sss_helper import build_shares, rebuild_from_hex, select_random_shares, rebuild_from_hex

def create_share_from_seed(seed_phrase, required_shares, total_shares):

    shares = build_shares(seed_phrase, required_shares, total_shares)

    shares_test = select_random_shares(shares, required_shares)

    try:
        # Try rebuild the seed with some sample shares before returning the shares
        assert seed_phrase == rebuild_from_hex(shares_test, required_shares=required_shares)
        print("Successfully created a recoverable seed from shares")
        return shares
    except Exception as e:
        print("Failed to recover seed from shares, unable to create shares from seed")
        print(e)

def rebuild_seed_from_shares(shares, required_shares, max_shares=10):
    try:
        secret = rebuild_from_hex(shares, required_shares, max_shares)
        print("Successfully created a recoverable secret from shares")
        return secret
    except Exception as e:
        print("Failed to recover secret from shares")
        print(e)
