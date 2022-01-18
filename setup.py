import os
from setuptools import setup, find_packages

# Declare your non-python data_preprocessing files:
# Files underneath configuration/ will be copied into the build preserving the
# subdirectory structure if they exist.
data_files = []


def add_files_in_folder(folder, output_files):
    for root, dirs, files in os.walk(folder):
        output_files.append((os.path.relpath(root, folder),
                        [os.path.join(root, f) for f in files]))


add_files_in_folder('data_preprocessing', data_files)


setup(
    name="WayfairModelServer",
    version="1.0",

    # declare your packages
    packages=find_packages(where="src", exclude=("test",)),
    package_dir={"": "src"},

    # include data_preprocessing files
    include_package_data=True,
    data_files=data_files,

    root_script_source_version="default-only",

    entry_points="""\
    [console_scripts]
    serve = wayfair.serving.serve:start_server
    client = wayfair.client.run_client:run
    """,
    test_command='pytest',
)
