import argparse
import base64
import msal
import sys
from typing import List

POLICY = "b2c_1_fjcloud_genai_susi"


def build_authority(tenant: str) -> str:
    return f"https://{tenant}.b2clogin.com/{tenant}.onmicrosoft.com/{POLICY}"  # B2C authority


def to_base64_token_cache(cache: msal.SerializableTokenCache) -> str:
    raw = cache.serialize()  # FULL cache (accounts + refresh tokens etc.)
    return base64.b64encode(raw.encode("utf-8")).decode("utf-8")


def interactive_auth(
    tenant: str, client_id: str, scopes: List[str], cache: msal.SerializableTokenCache
):
    """Perform silent then interactive auth; return MSAL result dict."""
    authority = build_authority(tenant)
    app = msal.PublicClientApplication(
        client_id, authority=authority, token_cache=cache
    )
    accounts = app.get_accounts()
    if accounts:
        silent = app.acquire_token_silent(scopes, accounts[0])
        if silent and ("access_token" in silent or "id_token" in silent):
            return silent
    # interactive
    result = app.acquire_token_interactive(scopes=scopes)
    if not result or ("access_token" not in result and "id_token" not in result):
        raise RuntimeError("Authentication failed; no token returned.")
    return result


def main():
    parser = argparse.ArgumentParser(description="Print Base64 MSAL token cache")
    parser.add_argument("--tenant", required=True)
    parser.add_argument("--client-id", required=True)
    args = parser.parse_args()

    tenant = args.tenant
    client_id = args.client_id

    # Fixed scopes for B2C authentication
    scopes = [f"https://{tenant}.onmicrosoft.com/{client_id}/.default"]

    cache = msal.SerializableTokenCache()

    try:
        result = interactive_auth(tenant, client_id, scopes, cache)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    # Produce Base64 of full cache (accounts, refresh etc.)
    b64_cache = to_base64_token_cache(cache)
    # Output ONLY the base64 string (no prefixes) for easy copying
    print(b64_cache)


if __name__ == "__main__":
    main()
