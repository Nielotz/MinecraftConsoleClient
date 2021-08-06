"""Provide action_list containing references to functions to run when \
received given packet ID."""

# Sample:
action_list = {
    "status": {
        0x00: print,
        1: print
    },
    "login": {
    },
    "play": {
    }
}
