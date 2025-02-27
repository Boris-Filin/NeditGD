OBJECT_IDS = {
    'block': 1,
    'spike': 8,
    'col_t': 899,
    'move_t' : 901,
    'text': 914,
    'stop_t' : 1616,
    'pulse_t' : 1006,
    'alpha_t' : 1007,
    'toggle_t' : 1049,
    'spawn_t' : 1268,
    'rotate_t' : 1346,
    'scale_t' : 2067,
    'follow_t' : 1347,
    'shake_t': 1520,
    'animate_t' : 1585,
    'keyframe_t' : 3033,
    'follow_player_y_t' : 1814,
    'adv_follow_t' : 3016,
    'edit_adv_follow_t' : 3660,
    'retarget_adv_follow_t' : 3661,
    'setup_keyframe_t' : 3032,
    'a_move_t' : 3006,
    'a_rotate_t' : 3007,
    'a_scale_t' : 3008,
    'a_fade_t' : 3009,
    'a_tint_t' : 3010,
    'edit_a_move_t' : 3011,
    'edit_a_rotate_t' : 3012,
    'edit_a_scale_t' : 3013,
    'edit_a_fade_t' : 3014,
    'edit_a_tint_t' : 3015,
    'a_stop_t' : 3024,
    'change_bg_t' : 3029,
    'change_g_t' : 3030,
    'change_mg_t' : 3031,
    'touch_t' : 1595,
    'count_t' : 1611,
    'instant_count_t' : 1811,
    'pickup_t' : 1817,
    'time_t' : 3614,
    'event_t' : 3615,
    'control_t' : 3617,
    'item_edit_t' : 3619,
    'item_comp_t' : 3620,
}

def oid_from_alias(alias: str) -> int:
    return OBJECT_IDS.get(alias, -1)

def oid_to_alias(oid: int) -> str:
    for alias, oid2 in OBJECT_IDS.items():
        if oid2 == oid: return alias
    return str(oid)