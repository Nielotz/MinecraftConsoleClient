"""Provide action_list containing references to functions to run when received given packet ID."""

action_list = {
    "status": {
    },
    "login": {  # Sample based on 1.12.2:
        # 0: login.disconnect,
        # 1: Clientbound._encryption_request,
        # 2: login.login_success,
        # 3: login.set_compression,
    },
    "play": {
    }
}
