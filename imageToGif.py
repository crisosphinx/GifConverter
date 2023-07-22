import sys
from time import sleep
from typing import Union, List
from datetime import datetime
from pathlib import Path
from wand.image import Image

ACCEPTABLE_TYPES = ['.gif', '.jpg', '.jpeg', '.png']
TIME = str(datetime.now()).replace(' ', '_').replace(':', '-')
LOGS = Path().cwd().joinpath('logs')
FILE = LOGS.joinpath(f'{TIME}_conv.log')

if not LOGS.exists():
    LOGS.mkdir()


def creds():
    print('''
     _         _____  ___    ___       _____  _____     ___    _  ___   
(_)/'\_/`\(  _  )(  _`\ (  _`\    (_   _)(  _  )   (  _`\ (_)(  _`\ 
| ||     || (_) || ( (_)| (_(_)     | |  | ( ) |   | ( (_)| || (_(_)
| || (_) ||  _  || |___ |  _)_      | |  | | | |   | |___ | ||  _)  
| || | | || | | || (_, )| (_( )     | |  | (_) |   | (_, )| || |    
(_)(_) (_)(_) (_)(____/'(____/'     (_)  (_____)   (____/'(_)(_)    
    ''')
    sleep(3)
    print('''
Thank you for using this software.

ImageToGif was created to turn an
image sequence into a usable gif.

Any modifications to the software
in the future can be provided or
requested on the github of:

https://www.github.com/crisosphinx.


Copyright (c) 2023.


DISCLAIMER:

Jeff Miller (Jeff3DAnimation.com) assumes
no responsibility or liability for any
bugs, errors or destruction of files by
using this program.

The software contained is provided on an
"as is" basis with no guarantees of
full completeness, accuracy, usefulness
or timeliness...

If a bug does occur, please contact me
(Jeff Miller) at jeff3danimation@gmail.com.
    ''')
    sleep(1)


def logger(to_write: str) -> None:
    if not FILE.exists():
        FILE.open('w').write(to_write)
    else:
        write = FILE.open('r').readlines()
        write.append(f'\n{to_write}')
        FILE.open('w').write(''.join(write))


def frame_specifier() -> int:
    frames = 4
    frame_speed = input(f'Specify frame delay (24 frames a second) [default: {frames}]: ')
    if frame_speed.isdigit():
        frames = int(frame_speed)
    logger(f'Got frame delay count: {frames}')
    return frames


def name_specifier() -> str:
    name = 'animated'
    filename = input('Enter file name [default: animated]: ')
    if len(filename) > 0:
        name = filename
    logger(f'Got name: {name}')
    return name


def is_list(arg) -> bool:
    return type(arg) is list


def match_file_type(path: Path) -> Path:
    if path.suffix in ACCEPTABLE_TYPES:
        logger(f'Matched: {path}')
        return path
    else:
        return Path()


def get_all_files_from_dir(arg: Path) -> Union[List[Path], Path]:
    paths = list()
    if not arg.is_dir():
        return arg
    for item in arg.glob('*.*'):
        paths.append(match_file_type(item))
    return paths


def clear_blanks(paths: List[Path]) -> List[Path]:
    paths_to_return = list()
    for each in paths:
        if each.as_posix() != '.':
            paths_to_return.append(each)
    return paths_to_return


def combine_images(image_to_create: Image, files: List[Path]) -> Image:
    for each in files:
        with Image(filename=each.as_posix()) as img:
            image_to_create.sequence.append(img)
    return image_to_create


def main(args, frame_delay: int, file_name: str) -> None:
    if not is_list(args):
        logger('Something went wrong...')
        raise IOError("Something went wrong...")
    paths = [get_all_files_from_dir(Path(x)) for x in args]
    if len(paths) == 1:
        paths = paths[0]
    paths = clear_blanks(paths)
    logger(f'Files found: {paths}')

    gif = combine_images(Image(), paths)
    for cursor in range(len(paths)):
        with gif.sequence[cursor] as frame:
            frame.delay = 10 * frame_delay

    gif.type = 'optimize'
    gif.save(filename=f'{file_name}.gif')
    logger(f'Created file: {file_name}.gif')


if __name__ == '__main__':
    creds()
    _frames = frame_specifier()
    _name = name_specifier()
    main(sys.argv[1:], _frames, _name)
