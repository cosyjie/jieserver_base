from pathlib import Path

SYSTEM_DIR = Path(__file__).resolve().parent.parent.parent

INSTALL_DIR = Path(SYSTEM_DIR, 'install')
PROJECTS_DIR = Path.joinpath(SYSTEM_DIR, 'projects')
SERVICE_APP_DIR = Path.joinpath(SYSTEM_DIR, 'serviceapp')
TEMP_DIR = Path.joinpath(SYSTEM_DIR, 'tmp')
APP_FILES = Path.joinpath(Path(__file__).resolve().parent.parent,'app_files')

MENU_POSITION = {
    'main_sidebar': '左侧主菜单',
    'content_menu': '栏目内',
}

PYENV_DIR = Path.joinpath(SYSTEM_DIR, 'pyenv')
PYENV_RUN_FILE = Path.joinpath(PYENV_DIR, 'libexec', 'pyenv')
PYENV_RUN_DIR = 'jieadminpanel3119'
PYENV_DEFAULT_PYTHON_RUN = Path.joinpath(PYENV_DIR, 'versions', PYENV_RUN_DIR, 'bin', 'python')
PYENV_DEFAULT_PIP_RUN = Path.joinpath(PYENV_DIR, 'versions', PYENV_RUN_DIR, 'bin', 'pip')

PYENV_DEFAULT_PYTHON = '3.11.9'
