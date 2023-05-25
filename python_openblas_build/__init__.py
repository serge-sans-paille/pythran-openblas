import os
import glob

__dir__ = os.path.dirname(__file__)

static_library = os.path.basename(glob.glob("lib*/*.*")[0])
include_dirs = os.path.join(__dir__,glob.glob("include/openblas*")[0])
library_dir = os.path.join(__dir__, glob.glob("lib*")[0])
