from lib.grabber import FrameGrabber

from cfg.constants import PROJECTDIR
from cfg.constants import DATAPATHNAME
from cfg.constants import CLASSIFIERDIRNAME
from cfg.constants import FACEDETECTCLASSIFIER
from cfg.constants import NNTRAINERFILENAME

class GRS(object):
    
    def __init__(self):

        #intitalize object to grab frame from capturing device
        self._grabber = FrameGrabber()

    def initialize(self):
        print "initializing grs.."

if __name__ == "__main__":
    try:
        grs = GRS()
    except IOError, ex:
        print ex.message
    except Exception, ex:
        print ex.message
    else:
        grs.initialize()
    raw_input()