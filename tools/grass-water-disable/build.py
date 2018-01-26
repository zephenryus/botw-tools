from cx_Freeze import setup, Executable

setup(
    name='Grass & Water Disable',
    options={
        'build_exe': {
            'packages': [],
        },
    },
    version='0.1',
    description='Disables water and grass layers in Breath of the Wild',
    executables=[Executable('grass-water-disable.py', base=None)]
)
