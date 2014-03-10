from setuptools import setup
import os, subprocess
exec_files = ['scripts/magicmock']
def update_exec(executable_files):
    try:
        py_exec = "#!%s" % subprocess.check_output(["which", "python"]).rstrip("\n")
        for exec_file in exec_files:
            filepath = os.path.join(os.getcwd(), exec_file)
            fp = open(filepath, 'rb')
            lines = fp.readlines()
            if len(lines) >= 1:
                line[0] = exec_file
            fp = open(filepath, 'wb')
            fp.writelines(lines)
    except Execption, e:
        print e
        raise Exception("Failed to update executable files. Cancel the process!")

update_exec(exec_files)
setup(
    name='magicmock',
    version='0.01',
    author='Mingze',
    author_email='mzxu@outlook.com',
    packages=['magicmock'],
    include_package_data=True,
    zip_safe=False,
    scripts=exec_files
    license="MIT",
    url='https://github.com/mzxu/magicmock',
    install_requires=["pyserial"],
    description='A generic mock server',
    long_description="Fake http request and response",
    )