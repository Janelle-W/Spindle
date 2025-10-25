'''from setuptools import setup

APP = ['app/launcher.py']
DATA_FILES = [
    ('', ['app/spindlechatbot.png', 'app/icon.icns', 'app/llama-2-13b-chat.Q4_K_M.gguf']),
]
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'app/icon.icns',
    'packages': ['requests', 'flask', 'PIL'],
    'resources': ['app/assistant_api.py', 'app/llama_runner.py']
}

setup(
    app=APP,
    name='spindleAI',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
'''

'''
from setuptools import setup

APP = ['app/launcher.py']
DATA_FILES = [
    ('', ['app/spindlechatbot.png', 'app/icon.icns', 'app/llama-2-13b-chat.Q4_K_M.gguf']),
]
OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'app/icon.icns',
    'includes': ['tkinter', 'requests', 'flask', 'llama_cpp', 'PIL'],
    'resources': ['app/assistant_api.py', 'app/llama_runner.py']
}

setup(
    app=APP,
    name='spindleAI',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
'''

from setuptools import setup

APP = ['app/launcher.py']
DATA_FILES = [
    ('', ['app/spindlechatbot.png', 'app/icon.icns', 'app/llama-2-13b-chat.Q4_K_M.gguf']),
]
OPTIONS = {
    'iconfile': 'app/icon.icns',
    'includes': ['tkinter', 'requests', 'flask', 'llama_cpp', 'PIL'],
    'resources': ['app/assistant_api.py', 'app/llama_runner.py'],
    'plist': {
        'CFBundleName': 'spindleAI',
        'CFBundleIdentifier': 'com.yourname.spindleAI',
        'CFBundleShortVersionString': '0.1.0',
        'LSUIElement': True,  # hides terminal on launch
    }
}

setup(
    app=APP,
    name='spindleAI',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
