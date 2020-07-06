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
    options = "--full-pep8 --with-tool bandit --absolute-paths" \
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


def check_files(path: str,
                excluded_files: [str, ],
                tests_: [callable, ],
                recursively: bool):
    """Check files using tests from tests_."""
    outputs = []
    if os.path.isfile(path=path):
        return check_file(path, tests_)

    for filename in os.listdir(path=path):
        full_file_path = os.path.join(path, filename)

        if full_file_path in excluded_files:
            continue

        if os.path.isdir(full_file_path):
            if recursively:
                check_files(full_file_path, excluded_files,
                            tests_, recursively)
            continue

        if not os.path.isfile(full_file_path):
            continue

        if not filename.endswith('.py'):
            continue

        outputs.append(check_file(full_file_path, tests_))
    return "".join(outputs)


def run(files_: [str, ], excluded_files: [str, ],  recursively: bool = True):
    """Run tests."""
    for file in files_:
        if file in excluded_files:
            continue

        print(f"\nPath: {file}\n\n")

        tests_ = []

        for test, enabled in check_list.items():
            if enabled:
                tests_.append(tests[test])

        if len(tests_) == 0:
            raise RuntimeError("No tests selected!")

        output = check_files(file, excluded_files, tests_, recursively)
        with open("code_test_log.txt", "w+") as f:
            f.write(output.replace(chr(13), ''), )  # Remove CR (enters).


files = [
    r"D:\SOFTORS\minecraft_console_client\minecraft_console_client\bot.py"
]

exclude = [
    r"D:\SOFTORS\minecraft_console_client\minecraft_console_client\__init__.py"

]
run(files, exclude,  recursively=False)
