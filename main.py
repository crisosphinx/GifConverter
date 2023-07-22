""" Conversion software for images to gif """

from __future__ import annotations
import sys
from time import sleep
from datetime import datetime
from pathlib import Path
from wand.image import Image

from . import __version__

ACCEPTABLE_TYPES = ['.gif', '.jpg', '.jpeg', '.png']
TIME = str(datetime.now()).replace(' ', '_').replace(':', '-')
LOGS = Path().cwd().joinpath('logs')
FILE = LOGS.joinpath(f'{TIME}_conv.log')

if not LOGS.exists():
    LOGS.mkdir()


def creds():
    """ Print the credits """
    print(__version__.TITLE)
    sleep(3)
    print(__version__.CREDITS)
    sleep(1)


def logger(to_write: str):
    """
    Log information to file

    :param to_write: String to write to file
    :type to_write: str
    """
    if not FILE.exists():
        with open(FILE, 'w', encoding='utf8') as file:
            file.write(to_write)
    else:
        write = []
        with open(FILE, 'r', encoding='utf8') as file:
            write = file.readlines()
        write.append(f'\n{to_write}')
        with open(FILE, 'w', encoding='utf8') as file:
            file.write(''.join(write))


def frame_specifier() -> int:
    """
    CLI will specify the amount of frames to use.

    :return: int
    """
    frames = 4
    frame_speed = input(f'Specify frame delay (24 frames a second) [default: {frames}]: ')
    if frame_speed.isdigit():
        frames = int(frame_speed)
    logger(f'Got frame delay count: {frames}')
    return frames


def name_specifier() -> str:
    """
    CLI will specify the name to use for the final file.

    :return: str
    """
    name = 'animated'
    filename = input('Enter file name [default: animated]: ')
    if len(filename) > 0:
        name = filename
    logger(f'Got name: {name}')
    return name


def is_list(arg) -> bool:
    """
    Determine if arg is a list.

    :param arg: Object to test against
    :type arg: any
    :return: bool
    """
    return arg.is_instance(list)


def match_file_type(path: Path) -> Path:
    """
    Match the file type and return a valid path.

    :param path: Path to check to see if the file is valid.
    :type path: Path
    :return: Path
    """
    if path.suffix in ACCEPTABLE_TYPES:
        logger(f'Matched: {path}')
        return path
    return Path()


def get_all_files_from_dir(arg: Path) -> list[Path] | Path:
    """
    Get all the files from a specified directory, if it is passed in.
    Otherwise, return the file.

    :param arg: Path to check.
    :type arg: Path
    :return: Union[list[Path], Path]
    """
    paths = []
    if not arg.is_dir():
        return arg
    for item in arg.glob('*.*'):
        paths.append(match_file_type(item))
    return paths


def clear_blanks(paths: list[Path]) -> list[Path]:
    """
    Clear the blank paths.

    :param paths: list of Paths to clear our empties from.
    :type paths: list[Path]
    :return: list[Path]
    """
    paths_to_return = []
    for each in paths:
        if each.as_posix() != '.':
            paths_to_return.append(each)
    return paths_to_return


def combine_images(image_to_create: Image, files: list[Path]) -> Image:
    """
    Combine images into a single image sequence.

    :param image_to_create: Image object
    :type image_to_create: Image
    :param files: Files to add to image object
    :type files: list[Path]
    :return: Image
    """
    for each in files:
        with Image(filename=each.as_posix()) as img:
            image_to_create.sequence.append(img)
    return image_to_create


def main(args: list[str], frame_delay: int, file_name: str):
    """
    Main function to run to convert all objects to an image sequence and animate it.

    :param args: Passed in file(s) or directory.
    :type args: list[str]
    :param frame_delay: Amount of frames to delay for each image.
    :type frame_delay: int
    :param file_name: File name to be used for the resulting image.
    :type file_name: str
    """
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
    FRAMES = frame_specifier()
    NAME = name_specifier()
    main(sys.argv[1:], FRAMES, NAME)
