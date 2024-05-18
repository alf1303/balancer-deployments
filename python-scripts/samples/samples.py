from SETTINGS import JoinKind

ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"

deploy_sample = {
    "name": "BOBA-USDT pool v8",
    "symbol": "BOBA-USDTv8",
    "swapFeePercentage": 1*10**12,
    "tokens": {
        "0x410C18429418e0c3a7B271C66B23A393eB9B7012": {
            "weight": 0.4,
            "rateProvider": ZERO_ADDRESS,
            "assetManager": ZERO_ADDRESS
        },
        "0x792211D33a174Bab4FFF5BBb956275aB11CDCeB2": {
            "weight": 0.6,
            "rateProvider": ZERO_ADDRESS,
            "assetManager": ZERO_ADDRESS
        }
    }
}

init_sample = {
    "poolId": "0x03e46cfa22cabfda5e319c29b9ac647974f9bde7000200000000000000000008", # FILL
    "joinKind": JoinKind.INIT,
    "fromInternalBalance": False,
    "tokens": {
        "0x410C18429418e0c3a7B271C66B23A393eB9B7012": {
            "amount": 65
        },
        "0x792211D33a174Bab4FFF5BBb956275aB11CDCeB2": {
            "amount": 44,
        }
    }
}

# handles also a single token join, you must still pass all token addresses for proper indexing,
# just set amount to 0
join_sample = {
    "poolId": "0x03e46cfa22cabfda5e319c29b9ac647974f9bde7000200000000000000000008", # FILL
    "joinKind": JoinKind.EXACT_TOKENS_IN_FOR_BPT_OUT,
    "fromInternalBalance": False,
    "tokens": {
        "0x410C18429418e0c3a7B271C66B23A393eB9B7012": {
            "amount": 100
        },
        "0x792211D33a174Bab4FFF5BBb956275aB11CDCeB2": {
            "amount": 200,
        }
    }
}