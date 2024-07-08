import os

TOKEN = "6458079316:AAEPQhdJ1TAmzPE2LslKnp7tPkk3t6CQ9oQ"
OWNER = 594363938
CHANNEL_ID = -1001926046726
FRONTEND_URL = "no_env_var_error"

PASSWORD_ROBOKASSA = 'VGJ86ffNO8U1OPcjzw7v'
LOGIN_ROBOKASSA = 'BySviat'

try:
    TOKEN = os.getenv("TOKEN")
    OWNER = int(os.getenv("OWNER"))
    CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
    FRONTEND_URL = os.getenv("FRONTEND_URL")
    if TOKEN is None:
        raise Exception
except Exception as e:
    TOKEN = "6458079316:AAEPQhdJ1TAmzPE2LslKnp7tPkk3t6CQ9oQ"
    OWNER = 594363938
    CHANNEL_ID = -1001926046726
    FRONTEND_URL = "no_env_var_error"
    print(f"env error: {e}")

# TOKEN = "6639799208:AAESoTmmURUyw_PoWRnTWTAP1UqKlvbTb1g"
# CHANNEL_ID = -1972561438
# FRONTEND_URL = "https://sviats.shop"
