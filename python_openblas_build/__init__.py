import os
import glob

__dir__ = os.path.dirname(__file__)

static_library = os.path.basename(glob.glob(f"{__dir__}/lib*/*.*")[0])
include_dirs = glob.glob(f"{__dir__}/include/openblas*")[0]
library_dir = glob.glob(f"{__dir__}/lib*")[0]
