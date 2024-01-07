from SaveLoad import read_level_objects, get_working_level

if __name__ == '__main__':
    objects = read_level_objects(get_working_level())
    for obj in objects:
        print('\t', obj)
