import os
from Editor import Editor


SUBDIRECTORY = '\\Level_instances\\'
PATH = os.getcwd() + SUBDIRECTORY

# Write data to a file in plaintext
def save_to_file(name: str, data: str) -> None:
    os.makedirs(PATH, exist_ok=True)
    print('[Nedit]: Saving current level data to:', SUBDIRECTORY + name)
    fw = open(PATH + name, "w")
    fw.write(data)
    fw.close()

# Load data from a plaintext file
def load_from_file(name: str) -> str:
    fr = open(PATH + name, "r")
    data = fr.read()
    fr.close()
    print('[Nedit]: Data loaded from:', SUBDIRECTORY + name)
    return data

# Load the current level and save its contents to a text file
def record_current_level(name: str, msg: str) -> None:
    editor = Editor.load_current_level()
    data = editor.get_robtop_string()
    save_to_file(name, msg + '#' + data)

# Load data from a text file and save to the current levle
def overload_current_level(name: str) -> None:
    msg, data = load_from_file(name).split('#')
    print(f'[Nedit]: Save description: \"{msg}\"')
    editor = Editor.load_from_robtop(data)
    editor.save_changes()

# Read the message of a savefile
def read_message(name: str) -> None:
    msg = load_from_file(name).split('#')[0]
    print(f'[Nedit]: Save description:\n{msg}')

# A printed menu with all the options
def menu() -> None:
    saves = None
    if os.path.exists(PATH):
        saves = os.listdir(PATH)
        print_saves(saves)

    print('[Nedit]: Select options:\n'
          '  (1): Save current level\n'
          '  (2): OVERWRITE current level with a save\n'
          '  (3): Read save message\n'
          '  (4): QUIT\n')
    inp = input()

    if inp == '1':
        name = input('[Nedit]: Please select a name for the save: ')
        msg = input('[Nedit]: Enter an optional save description: ')
        record_current_level(name, msg)

    elif inp == '2' and saves:
        print('[Nedit]: WARNING: This will overwrite the most '
              'recent level in your custom levels list! Make sure'
              'you have put an empty level there!')
        confirm = input('[Nedit]: Enter \'OK\' to continue:\n')
        if confirm.lower() != 'ok':
            print('[Nedit]: Confirmation failed!')
            quit()
        print('[Nedit]: Please select one of the listed saves to load!')
        name = input().lower()
        if not name in map(str.lower, saves):
            print('[Nedit]: Save not found!')
            quit()
        overload_current_level(name)

    elif inp == '2':
        print('[Nedit]: You have no levels saved!')

    elif inp == '3':
        print('[Nedit]: Please select one of the listed saves to read!')
        name = input().lower()
        if not name in map(str.lower, saves):
            print('[Nedit]: Save not found!')
            quit()
        read_message(name)
    
    quit()

# Print all of the save names in the folder
def print_saves(saves: list[str]) -> None:
    print()
    print(f'[Nedit]: {len(saves) if saves else "No"}'
          f' save{"" if len(saves) == 1 else "s"}'
          f' found{":" if saves else "."}')
    for (i, save) in enumerate(saves):
        print(f'  > {save}')
    print()



if __name__ == '__main__':
    menu()
