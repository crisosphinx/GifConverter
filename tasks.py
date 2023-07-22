""" Tasks file for making things easier to test """
import shutil
from pathlib import Path
from invoke.tasks import task


@task()
def lint(ctx):
    """
    Linting step.

    :param ctx: Context
    :type ctx: Context
    """
    ctx.run('pylint *')


@task()
def build(ctx):
    """
    Build step.

    :param ctx: Context
    :type ctx: Context
    """
    ctx.run('pyinstaller -F --uac-admin --icon="./resources/ToGif.ico" --clean main.py')
    dist_dir = Path('dist')
    dist_file = dist_dir.joinpath('main.exe')
    dist_file.rename('dist/ImageToGif.exe')
    readme = Path('readme.txt')
    shutil.copy2(readme, dist_dir.joinpath(readme))
