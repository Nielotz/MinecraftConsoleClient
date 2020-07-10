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

# PEPs to ignore.
excluded_PEPs = [
    "D203",
    "D212",
    "D103",  # Missing docstring in public function
    "unused-argument",
    "protected-access",
    "not-callable",
    "unused-variable"

]

files = [
    r"D:\SOFTORS\minecraft_console_client\minecraft_console_client\versions/v1_12_2",
]

exclude = [
    r"D:\SOFTORS\minecraft_console_client\minecraft_console_client\versions/v1_12_2\view"
]


def code_style_test(path):
    """Execute pycodestyle and returns result."""
    # https://github.com/PyCQA/pycodestyle

    options = "--max-doc-length=72"

    p = Popen(['pycodestyle', *options.split(), path],
              stdout=PIPE,
              stderr=PIPE)
    output = p.stdout.read().decode("utf-8")
    if len(output.strip()) == 0:
        return ""
    return "".join(("pycodestyle:".center(50, '-'), "\n", output))


def code_doc_test(path):
    """Execute pydocstyle and returns result."""
    # https://github.com/PyCQA/pydocstyle

    options = ""

    p = Popen(['pydocstyle', *options.split(), path], stdout=PIPE, stderr=PIPE)
    output = p.stdout.read().decode("utf-8")
    if len(output.strip()) == 0:
        return ""
    return "".join(("pydocstyle:".center(50, '-'), "\n", output))


def prospector(path):
    """Execute prospector and returns result."""
    # https://github.com/PyCQA/prospector

    # -s medium / high / veryhigh / lite(or sth, check in manual)
    # --absolute-paths
    options = "--full-pep8 --with-tool bandit -s veryhigh " \
              "-M -D --output-format text"

    p = Popen(['prospector', *options.split(), path], stdout=PIPE, stderr=PIPE)
    output = p.stdout.read().decode("utf-8")[22:-8]
    if len(output.strip()) == 0:
        return ""
    return "".join(("prospector:".center(50, '-'), "\n", output))


def check_file(path: str, tests_: (callable,)):
    """Check file using tests from tests_."""
    outputs = [f"[FILE]: {path}", "\n"]
    print(f"Checking file: {path}")
    for test in tests_:
        result = test(path)
        remove_idx = []
        split_result = result.split("\n")

        for idx, row in enumerate(split_result):
            for excluded in excluded_PEPs:
                if excluded in row:
                    remove_idx.append(idx - 1)
                    remove_idx.append(idx)
                    remove_idx.append(idx + 1)
                    break
        for idx in remove_idx[::-1]:
            if idx < len(split_result):
                split_result.pop(idx)
            if len(split_result) > idx != 0:
                if split_result[idx] == split_result[idx - 1]:
                    split_result.pop(idx)
        if len(split_result) < 2:
            continue

        if split_result[1] == "":
            continue

        outputs.append("\n".join(split_result))
    outputs.append("\n")
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
                outputs.append(check_files(full_file_path, excluded_files,
                                           tests_, recursively))
            continue

        if not os.path.isfile(full_file_path):
            continue

        if not filename.endswith('.py'):
            continue

        outputs.append(check_file(full_file_path, tests_))
    return "".join(outputs)


def run(files_: [str, ], excluded_files: [str, ], recursively: bool = True):
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


tests = {
    'code_style_test': code_style_test,
    'code_doc_test': code_doc_test,
    'prospector': prospector,
}

run(files, exclude, recursively=True)
