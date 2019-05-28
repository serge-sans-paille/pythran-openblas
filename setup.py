import os
from setuptools import setup, Distribution
from distutils.command.build_clib import build_clib
from sys import platform

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
            tar.extractall()

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

        subprocess.check_call(["cmake",
                               '-G', generator,
                               '-DCMAKE_BUILD_TYPE=Release',
                               '-DDYNAMIC_ARCH={}'.format(dynamic_arch),
                               '-DNOFORTRAN=1',
                               '-DNO_LAPACK=1',
                               '-DBUILD_SHARED_LIBS=OFF',
                               os.path.join(cwd, 'OpenBLAS-{version}'.format(version=OpenBLASVersion)),
                               "-DCMAKE_INSTALL_PREFIX="+os.path.join(cwd, 'build', 'lib', name)])
        subprocess.check_call(builder)
        subprocess.check_call(["cmake", "--build", '.', '--target', 'install'])

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
      cmdclass={'build_clib': MyBuildCLib})

