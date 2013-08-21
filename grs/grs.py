import cv2
import numpy as np

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

        self.faces = None
        self.face_dxn_ctr = 8
        self.hc = None
        self.winname = "GRS"

    def initialize(self):
        print "initializing grs.."
        self._get_face_rgn()

    def _calc_ctr_obj(self, obj):
        return obj[0][0] + obj[0][3] / 2, obj[0][1] + obj[0][2] / 2

    def _get_face_rgn(self):
        print "Loading Haar classifier ..."
        self.hc = cv2.cv.Load(PROJECTDIR + DATAPATHNAME + CLASSIFIERDIRNAME + FACEDETECTCLASSIFIER)
        print "Classifier Loaded successfully"

        thresh_dist = 16
        start_of_dxn = True
        break_flag = False

        crt_frame = self._grabber.capture.read()[1]
        while crt_frame != None:
            crt_faces = cv2.cv.HaarDetectObjects(cv2.cv.fromarray(crt_frame), self.hc, cv2.cv.CreateMemStorage())
            print "No. of faces detected: ", len(crt_faces)
            for (x, y, w, h), n in crt_faces:
                cv2.rectangle(crt_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.imshow(self.winname, crt_frame)
            c = cv2.waitKey(1)
            if c == 27:
                break_flag = True
                cv2.destroyWindow(self.winname)
                break
            if start_of_dxn:
                print "This was start of detection"
                prev_faces = crt_faces
                start_of_dxn = not start_of_dxn
                print "start of dxn:", start_of_dxn
            else:
                print "This is not start of dxn"
                print "Checking faces"
                for pidx, prev_face in enumerate(prev_faces):
                    print "Previous faces at index is ", pidx, "with value", prev_face
                    present = False
                    px, py = self._calc_ctr_obj(prev_face)
                    print "px:", px, "py:", py
                    for cidx, crt_face in enumerate(crt_faces):
                        print "checking with crt_face at index", cidx, "with value", crt_face
                        cx, cy = self._calc_ctr_obj(crt_face)
                        print "===cx:", cx, "cy:", cy
                        if abs(cx - px) <= thresh_dist and abs(cy - py) <= thresh_dist:
                            present = True
                            print "Face matched with crt_face at index", cidx, "of value", crt_face
                            break
                        if not present:
                            print "No face is matched setting it to false"
                            prev_faces[pidx] = False
                faces = [face for face in prev_faces if face]
                prev_faces = faces
                print "***Faces are:", faces
                print "Nos. of faces", len(faces)
                print "===Face :", faces
                if len(faces) < 1:
                    self.face_dxn_ctr = 8
                    print "###No face detected"
                    start_of_dxn = True
                else:
                    self.face_dxn_ctr -= 1
                    print "Face dxn counter:", self.face_dxn_ctr
                    if self.face_dxn_ctr == 0:
                        cv2.destroyWindow(self.winname)
                        break
            crt_frame = self._grabber.capture.read()[1]
        self.faces = faces

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