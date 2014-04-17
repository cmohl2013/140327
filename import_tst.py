import sys
sys.path.append("/mnt/moehlc/home/idaf_library")
import mahotas
import libidaf.idafIO as io

path = '/mnt/moehlc/idaf/IDAF_Projects/140327_raman_bloodvessel_mri/data/segmented/angio_wt'

pattern = 'flowSkel'

fnames = io.getFilelistFromDir(path,pattern)