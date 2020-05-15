

change_game_state_reason = {
    0: ("invalid_bed", ),
    1: ("end_raining", ),
    2: ("begin_raining", ),
    3: ("change_gamemode", ),
    4: ("exit_end", ),
    5: ("demo_message", ),
    6: ("arrow_hitting_player", ),
    7: ("fade_value", ),
    8: ("fade_time", ),
    10: ("play_elder_guardian_mob_appearance_effect_and_sound", ),
}

for val in change_game_state_reason:
    print(f"""        @staticmethod
        def {change_game_state_reason[val][0]}(value: float):
            pass
""")

