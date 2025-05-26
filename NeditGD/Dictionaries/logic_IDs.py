'''
This file includes various info regarding GD triggers. This should help with high-tech level creation.

Logic includes anything that can be remapped
- groups
- counter/timer IDs
- collision IDs
'''


GROUP_FIELDS = [
    'target',
    'target_pos',
    'center_group_id',
    'rotation_target',
    'gradient_bl',
    'gradient_br',
    'gradient_tl',
    'gradient_tr'
]

ITEM_FIELDS = [
    'target', # For item edit only
    'item_id',
    'block_b'
]

COLLISION_FIELDS = [
    'item_id',
    'block_b'
]

LOGIC_FIELDS = \
    GROUP_FIELDS + \
    ITEM_FIELDS + \
    COLLISION_FIELDS