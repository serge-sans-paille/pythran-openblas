import os
from setuptools import setup, Extension
from setuptools.command.build_clib import build_clib
from wheel.bdist_wheel import bdist_wheel as bdist_wheel_


class bdist_wheel(bdist_wheel_):
    def get_tag(self):
        _, _, plat_name = bdist_wheel_.get_tag(self)
        return 'py2.py3', 'none', plat_name


from sys import platform
from shutil import copyfile, copytree
import glob

OpenBLASVersion = '0.3.23'
ProjectVersion = f"{OpenBLASVersion}preview1"
name = 'python_openblas_build'


class MyBuildCLib(build_clib):

    def download(self):
        import tarfile
        try:
            import urllib.request as request
        except ImportError:
            import urllib as request

        fname = "v{version}.tar.gz".format(version=OpenBLASVersion)
        if os.path.isfile(fname):
            print("File present skip download")
        else:
            print("Downloading OpenBLAS version {}".format(OpenBLASVersion))
            request.urlretrieve(
                "https://github.com/xianyi/OpenBLAS/archive/v{version}.tar.gz".format(version=OpenBLASVersion), fname)

        print("Extracting OpenBLAS version {}".format(OpenBLASVersion))
        with tarfile.open(fname, "r:gz") as tar:
            def is_within_directory(directory, target):

                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)

                prefix = os.path.commonprefix([abs_directory, abs_target])

                return prefix == abs_directory

            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):

                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")

                tar.extractall(path, members, numeric_owner=numeric_owner)

            safe_extract(tar)

    def run(self):
        self.download()

        import subprocess
        ccache_build = [
            "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
            "-DCMAKE_Fortran_COMPILER_LAUNCHER=ccache",
        ]
        additional_args = ccache_build if os.getenv("ACTIVE_CCACHE") else []

        print("Building OpenBLAS version {}".format(OpenBLASVersion))
        if platform == "win32":
            dynamic_arch = 0
            builder = ["cmake", "--build", "."]
            additional_args += [
                "-DBINARY=64",
                "-DINTERFACE64=1"
            ]
        else:
            dynamic_arch = 1
            builder = ["make", "-j2"]
            if platform == "darwin":
                additional_args += ["-DCMAKE_Fortran_COMPILER=gfortran"]

        try:
            os.makedirs(self.build_temp)
        except OSError:
            pass

        cwd = os.getcwd()
        os.chdir(self.build_temp)
        # this is clumsy <3
        guess_libplat = glob.glob(os.path.join(cwd, 'build', 'lib*'))[0]
        install_prefix = os.path.join(guess_libplat, 'python_openblas_build')
        subprocess.check_call(["cmake",
                               "-DCMAKE_BUILD_TYPE=Release",
                               "-DDYNAMIC_ARCH={}".format(dynamic_arch),
                               "-DUSE_THREAD=0",
                               "-DUSE_OPENMP=0",
                               "-DBUILD_SHARED_LIBS=OFF",
                               os.path.join(cwd, 'OpenBLAS-{version}'.format(version=OpenBLASVersion)),
                               "-DCMAKE_INSTALL_PREFIX=" + install_prefix, ] + additional_args)
        subprocess.check_call(builder)
        subprocess.check_call(["cmake", "--build", '.', '--target', 'install'])

        guess_libblas = glob.glob(os.path.join(install_prefix, 'lib*', '*openblas*'))[0]
        target_libblas = guess_libblas.replace('openblas', 'python_openblas_build').replace("_64.", ".")
        copyfile(guess_libblas, os.path.basename(target_libblas))

        os.chdir(cwd)


setup(name=name,
      version=ProjectVersion,
      packages=[name],
      libraries=[(name, {'sources': []})],
      description='Python packaging of OpenBLAS',
      long_description='Binary distribution of OpenBLAS static libraries',
      author='khaled-besrour',
      author_email='khaledbesrour2@gmail.com',
      url='https://github.com/kbesrour-ma/' + name.replace('_', '-'),
      license="BSD 3-Clause",
      ext_modules=[Extension("python_openblas_build.placeholder", ['python_openblas_build/placeholder.c'])],
      cmdclass={'build_clib': MyBuildCLib, 'bdist_wheel': bdist_wheel})
