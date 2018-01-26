from cx_Freeze import setup, Executable

setup(
    name='hght Maker',
    options={
        'build_exe': {
            'packages': [],
        },
    },
    version='0.1',
    description='Generates hght files from images for Breath of the Wild',
    executables=[Executable('make-hght.py', base=None)]
)
