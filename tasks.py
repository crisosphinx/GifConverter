import shutil
from pathlib import Path
from invoke.tasks import task


@task()
def build(ctx):
    ctx.run('pyinstaller -F --uac-admin --icon="./resources/ToGif.ico" --clean main.py')
    dist_dir = Path('dist')
    dist_file = dist_dir.joinpath('main.exe')
    dist_file.rename('dist/ImageToGif.exe')
    readme = Path('readme.txt')
    shutil.copy2(readme, dist_dir.joinpath(readme))
