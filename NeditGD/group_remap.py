from NeditGD import Editor, Object


def remap_groups(objects: list[Object], remap: dict[int, int],
                 keep_unchanged: bool=True) -> list[Object]:
    
    new_objects = []

    for obj in objects:
        new_obj = Object.copy(obj)
        changed = False

        if (groups := obj.groups) is not None:
            new_groups = []
            for group in groups:
                new_group = group
                if group in remap:
                    changed = True
                    new_group = remap[group]
                new_groups.append(new_group)
            new_obj.groups = new_groups
        
        if (parent_groups := obj.parent_groups) is not None:
            new_parent_groups = []
            for group in parent_groups:
                new_group = group
                if group in remap:
                    changed = True
                    new_group = remap[group]
                new_parent_groups.append(new_group)
            new_obj.parent_groups = new_parent_groups
        
        if obj.id == 3619:
            new_objects.append(new_obj)            
            continue

        if (target := obj.target) is not None:
            if target in remap:
                new_obj.target = remap[new_obj.target]
                changed = True
        if (target_pos := obj.target_pos) is not None:
            if target_pos in remap:
                new_obj.target_pos = remap[new_obj.target_pos]
                changed = True
        if (center_group_id := obj.center_group_id) is not None:
            if center_group_id in remap:
                new_obj.center_group_id = remap[new_obj.center_group_id]
                changed = True
        if (rotation_target := obj.rotation_target) is not None:
            if rotation_target in remap:
                new_obj.rotation_target = remap[new_obj.rotation_target]
                changed = True

        if keep_unchanged or changed:
            new_objects.append(new_obj)

    return new_objects

def remap_group_lists(objects: list[Object],
                 old: list[int], new: list[int]) -> list[Object]:
    if len(old) != len(new):
        raise Exception("Old and New groups don't match in length!")
    remap = dict(zip(old, new))
    return remap_groups(objects, remap)
    


def remap_group(objects: list[Object], old: int, new: int,
                keep_unchanged: bool=True) -> list[Object]:
    return remap_groups(objects, {old: new}, keep_unchanged)

def shift_groups(objects: list[Object],
                 old: list[int], offset: int) -> list[Object]:
    new = [o + offset for o in old]
    return remap_group_lists(objects, old, new)


def tmp() -> None:
    editor = Editor.load_current_level(False)
    editor.objects = shift_groups(editor.objects, range(500, 510), -10)
    editor.objects = shift_groups(editor.objects, range(520, 530), -50)
    editor.objects = shift_groups(editor.objects, range(400, 500), 100)
    editor.objects = shift_groups(editor.objects, range(400, 900), 100)

    editor.save_changes()

if __name__ == '__main__':
    tmp()

    # editor.objects = shift_groups(editor.objects, range(30, 36), 72)
    # editor.objects = remap_group (editor.objects, 20, 101)
    # editor.objects = shift_groups(editor.objects, range(36, 45), 72)
    # editor.objects = shift_groups(editor.objects, range(30, 36), 72)
    # editor.objects = remap_group (editor.objects, 21, 117)
    # editor.objects = remap_group_lists(editor.objects,
    #                     range(10, 19), range(118, 127))
    # editor.objects = remap_group_lists(editor.objects,
    #                     range(24, 28), range(130, 138, 2))
    # editor.objects = remap_group_lists(editor.objects,
    #                     range(48, 52), range(131, 138, 2))

    # editor.objects = remap_group (editor.objects, 21, 117)
    # editor.objects = shift_groups(editor.objects, range(300, 320), -90)
