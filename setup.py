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

OpenBLASVersion = '0.3.6'
name = 'pythran_openblas'


class MyBuildCLib(build_clib):
    def run(self):
        try:
            import urllib.request as request
        except ImportError:
            import urllib as request
        fname = "v{version}.tar.gz".format(version=OpenBLASVersion)
        print("Downloading OpenBLAS version {}".format(OpenBLASVersion))
        request.urlretrieve("https://github.com/xianyi/OpenBLAS/archive/v{version}.tar.gz".format(version=OpenBLASVersion), fname)
        import tarfile
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

        import subprocess
        print("Building OpenBLAS version {}".format(OpenBLASVersion))
        dynamic_arch = int(platform != "win32")
        if platform == "win32":
            dynamic_arch = 0
            generator = "Visual Studio 14 Win64"
            builder = ["cmake", "--build", '.']
        else:
            dynamic_arch = 1
            generator = "Unix Makefiles"
            builder = ['make', '-j2']

        try:
            os.makedirs(self.build_temp)
        except OSError:
            pass

        cwd = os.getcwd()
        os.chdir(self.build_temp)
        # this is clumsy <3
        guess_libplat = glob.glob(os.path.join(cwd, 'build', 'lib*'))[0]
        install_prefix = os.path.join(guess_libplat, 'pythran_openblas')
        subprocess.check_call(["cmake",
                               '-G', generator,
                               '-DCMAKE_BUILD_TYPE=Release',
                               '-DDYNAMIC_ARCH={}'.format(dynamic_arch),
                               '-DNOFORTRAN=1',
                               '-DNO_LAPACK=1',
                               '-DBUILD_SHARED_LIBS=OFF',
                               os.path.join(cwd, 'OpenBLAS-{version}'.format(version=OpenBLASVersion)),
                               "-DCMAKE_INSTALL_PREFIX="+install_prefix])
        subprocess.check_call(builder)
        subprocess.check_call(["cmake", "--build", '.', '--target', 'install'])

        guess_libblas = glob.glob(os.path.join(install_prefix, 'lib*', '*openblas*'))[0]
        target_libblas = guess_libblas.replace('openblas', 'pythran_openblas')
        copyfile(guess_libblas, os.path.basename(target_libblas))

        os.chdir(cwd)

setup(name=name,
      version=OpenBLASVersion,
      packages=[name],
      libraries=[(name, {'sources': []})],
      description='Python packaging of OpenBLAS',
      long_description='Binary distribution of OpenBLAS static libraries',
      author='serge-sans-paille',
      author_email='serge.guelton@telecom-bretagne.eu',
      url='https://github.com/serge-sans-paille/' + name.replace('_', '-'),
      license="BSD 3-Clause",
      ext_modules=[Extension("pythran_openblas.placeholder", ['pythran_openblas/placeholder.c'])],
      cmdclass={'build_clib': MyBuildCLib,'bdist_wheel': bdist_wheel})

