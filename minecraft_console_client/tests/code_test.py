"""Module performing whole bunch of code related tests.

Based on https://github.com/PyCQA

Requirements:
    pip install pip --upgrade

    pip install pycodestyle
    pip install --upgrade pycodestyle

    pip install pydocstyle

    pip install prospector
"""

import os
import pathlib

from subprocess import Popen, PIPE

check_list = {
    'code_style_test': True,
    'code_doc_test': True,
    'prospector': True,
}


def code_style_test(path):
    """Execute pycodestyle and returns result."""
    # https://github.com/PyCQA/pycodestyle

    options = "--max-doc-length=72"

    p = Popen(['pycodestyle', *options.split(), path],
              stdout=PIPE,
              stderr=PIPE)

    return "".join(("pycodestyle:".center(50, '-'),
                    "\n",
                    p.stdout.read().decode("utf-8")))


def code_doc_test(path):
    """Execute pydocstyle and returns result."""
    # https://github.com/PyCQA/pydocstyle

    options = ""

    p = Popen(['pydocstyle', *options.split(), path], stdout=PIPE, stderr=PIPE)

    return "".join(("pydocstyle:".center(50, '-'),
                    "\n",
                    p.stdout.read().decode("utf-8")))


def prospector(path):
    """Execute prospector and returns result."""
    # https://github.com/PyCQA/prospector

    # -s medium / high / veryhigh / lite(or sth, check in manual)
    # --absolute-paths
    options = "--full-pep8 --with-tool bandit " \
              "-M -D --output-format text"

    p = Popen(['prospector', *options.split(), path], stdout=PIPE, stderr=PIPE)

    return "".join(("prospector:".center(50, '-'),
                    "\n",
                    p.stdout.read().decode("utf-8")[22:-8]))


tests = {
    'code_style_test': code_style_test,
    'code_doc_test': code_doc_test,
    'prospector': prospector,
}


def check_file(path: str, tests_: (callable,)):
    """Check file using tests from tests_."""
    outputs = []
    print(f"Checking file: {path}")
    for test in tests_:
        result = test(path)
        outputs.append(result)

    return "".join(outputs)


def check_files(path: str, tests_: [callable, ]):
    """Check files using tests from tests_."""
    outputs = []
    if os.path.isfile(path=path):
        return check_file(path, tests_)

    for filename in os.listdir(path=path):
        full_file_path = os.path.join(path, filename)

        if os.path.isdir(full_file_path):
            check_files(full_file_path, tests_)
            continue

        if not os.path.isfile(full_file_path):
            continue

        if not filename.endswith('.py'):
            continue

        outputs.append(check_file(full_file_path, tests_))
    return "".join(outputs)


def run():
    """Run tests."""
    path_to_project_folder = pathlib.Path().absolute()  # .parent.absolute()
    path_to_project_folder = \
        r"D:\SOFTORS\minecraft_console_client\m" \
        r"inecraft_console_client\tests\code_test.py"

    print(f"\nPath: {path_to_project_folder}\n\n")

    tests_ = []

    for test, enabled in check_list.items():
        if enabled:
            tests_.append(tests[test])

    if len(tests_) == 0:
        raise RuntimeError("No tests selected!")

    output = check_files(path_to_project_folder, tests_)
    with open("code_test_log.txt", "w+") as f:
        f.write(output.replace(chr(13), ''), )  # Remove CR (enters).


run()
