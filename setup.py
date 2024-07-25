import sys
from cx_Freeze import setup, Executable

# Определите базу для Windows
base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

# Настройки иконки
icon = 'appIcon.ico' if sys.platform == 'win32' else 'appIcon.icns'

# Общие опции для сборки
build_exe_options = {
    'include_files': ['appIcon.ico', 'appIcon.icns'],  # Включите иконку в сборку
    'packages': [],  # Укажите дополнительные пакеты, если необходимо
    'excludes': []   # Укажите исключаемые пакеты, если необходимо
}

# Настройки для macOS
bdist_mac_options = {
    'iconfile': 'appIcon.icns',  # Укажите иконку для macOS
    'bundle_name': 'HAMAUTO',      # Укажите имя бандла для macOS
}

# Создание списка с объектом Executable
executables = [
    Executable('main.py', base=base, icon=icon)
]

setup(
    name='HAMAUTO',
    version='0.1',
    description='Autobot for hamster',
    options={
        'build_exe': build_exe_options,
        'bdist_mac': bdist_mac_options   # Добавьте настройки для macOS
    },
    executables=executables
)