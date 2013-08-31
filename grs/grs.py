import numpy as np
import cv2
import win32api as wa


from cfg.constants import *
from lib.grabber import FrameGrabber
from lib.detector import BProjectionDetector
from lib.tracker import CamShiftTracker
from lib.recognizer import HandRecognizer
from lib.handler import MouseHandler

class GRS(object):
    def __init__(self):
        print "initializing frame grabber"
        self._grabber = FrameGrabber()
        print "frame grabber initialized"

        print "learning skin color"
        self._learnHist()
        print "skin color learned"
        self._winname = "GRS"
        self._dilationFilter = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 4))

        #intialize detector
        self._detector = BProjectionDetector(self._hist)

        self._selection = (120, 120, 80, 80)
        #initialize tracker
        self._tracker = CamShiftTracker(( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_MAX_ITER, 10, 1))

        #initialize recognizer
        self._recognizer = HandRecognizer()

        self._handler = MouseHandler()

        self._fstartx = 100
        self._fstarty = 80

        dict = wa.GetMonitorInfo(1) #argument 1 for standard input Monitor
        _, _, xmax, ymax = dict['Monitor']

        #self._fwidth = int(0.4 * xmax)
        self._fwidth = 440
        self._fheight = 320
        #self._fheight = int(0.4 * ymax)

    def _learnHist(self):
        skin = cv2.imread(PROJECTDIR + DATAPATHNAME + SKINDIRNAME + SKINFILENAME)
        gray = cv2.cvtColor(skin, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
        hsv = cv2.cvtColor(skin, cv2.COLOR_BGR2HSV)
        self._hist = cv2.calcHist([hsv], [0, 1], mask, [36, 50], [0, 180, 0, 255])
        pass

    def _grabNext(self):
        self._frame = self._grabber.grabNext()

    def _preprocess(self):
        self._frame = cv2.medianBlur(self._frame, 3)
        self._frame = cv2.cvtColor(self._frame, cv2.COLOR_BGR2HSV)

    def _rearrangeSelection(self, (x, y, w, h)):
        if w > 1.5 * h:
            h = 1.3 * h
        return (int(x - 0.2 * w), int(y - 0.18 * h), int(1.8 * w), int(1.3 * h))

    def run(self):
        postures = ["fist", "open", "none"]
        back_project = False
        self._grabNext()
        while self._frame != None:

            #store image temporarily
            temp_frame = self._frame

            #preprocess the frame   1. median blur  2. conversion to hsv
            self._preprocess()

            #backproject the frame
            self._frame = self._detector.detect(self._frame)

            #apply erosion
            #self._frame = cv2.erode(self._frame, np.ones((3,3), np.uint8))

            #apply dilation
            #self._frame = cv2.dilate(self._frame, self._dilationFilter)

            retval, (x, y, w, h) = self._tracker.track(self._frame, self._selection)

            (x, y, w, h) = self._rearrangeSelection((x, y, w, h))
            if x > 0 and y >0 and w > 0 and h > 0 and (x + w) < self._frame.shape[1] and (y + h) < self._frame.shape[0]:
                self._selection = (x, y, w, h)

                #to write in image
                #cv2.putText(temp_frame, str(x) + str(y) + str(w) + str(h), (30, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (200, 0, 0))
                
                #recognize
                posture = self._recognizer.haarRecognize(temp_frame, self._selection)

                #print postures[posture]

                #handle mouse event
                self._handler.handle((x, y, w, h), posture)

            cv2.rectangle(temp_frame, (self._fstartx, self._fstarty), (self._fstartx + self._fwidth, self._fstarty + self._fheight), (0, 0, 255), 2)
            cv2.rectangle(temp_frame, (x, y), (x +w, y + h), (200, 0, 0), 2)
            cv2.circle(temp_frame, (int(x + w / 2.0), int(y + h / 2.0)), 2, (0, 255, 0), 1)
            if back_project:
                cv2.imshow(self._winname, self._frame)
            else:
                cv2.imshow(self._winname, temp_frame)

            c = cv2.waitKey(1)
            if c == 27:
                cv2.destroyWindow(self._winname)
                break
            elif c == ord('b'):
                back_project = not back_project

            self._grabNext()
        cv2.destroyAllWindows()
        pass

if __name__ == "__main__":
    grs = GRS()

    grs.run()
"""
from lib.grabber import FrameGrabber
from lib.detector import BProjectionDetector
from lib.tracker import CamShiftTracker
from lib.handler import MouseHandler
from lib.recognizer import HandRecognizer

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
        self.face_skins = []
        self.palm_skin = False
        self.skins = None
        self.selection = (120, 120, 80, 80)
        self.hist = None
        self.crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_MAX_ITER, 10, 1)

    def initialize(self):
        print "initializing grs.."
        self._get_face_rgn()
        self._get_face_skins()
        self._get_palm_rgn()
        self._fill_face_skin()
        self._fill_skins()
        self._learn_hist()
        print "Finished initializing"



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

    def _get_face_skins(self):
        crt_frame = self._grabber.capture.read()[1]
        for (x, y, w, h),n in self.faces:
            temp = crt_frame[int(1.1 * y):int(y + 0.2 * w), int(x + 0.2 * h):int(x + 0.65 * h)]
            src_gray = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
            ret, src_thresh = cv2.threshold(src_gray, 100, 255, cv2.THRESH_BINARY)
            src_thresh = cv2.cvtColor(src_thresh, cv2.COLOR_GRAY2BGR)
            face_skin = temp & src_thresh
            self.face_skins.append(face_skin)

    def _get_palm_rgn(self):
        _, frame = self._grabber.capture.read()
        cv2.namedWindow(self.winname, cv2.CV_WINDOW_AUTOSIZE)
        selection = self.selection
        while frame != None:
            cv2.rectangle(frame, selection[:2], (selection[0] + selection[3], selection[1] + selection[2]), (255, 0, 0), 2)
            cv2.imshow(self.winname, frame)
            c = cv2.waitKey(1)
            if c == 27:
                break
            elif c == 13:
                self.palm_skin = frame[selection[1]+2:selection[1] + selection[2]-2, selection[0]+2:selection[0] + selection[3]-2]
                break
            frame = self._grabber.capture.read()[1]
        cv2.destroyWindow(self.winname)

    def _fill_face_skin(self):
        palm_skin = self.palm_skin
        for face_skin in self.face_skins:
            for row in range(face_skin.shape[0]):
                for col in range(face_skin.shape[1]):
                    if any(face_skin[row, col]) == 0:
                        face_skin[row, col] = palm_skin[np.random.randint(0, high=palm_skin.shape[0]), np.random.randint(0, high=palm_skin.shape[1])]
        

    def _add_images(self, src1, src2):
        if src2 == None:
            return src1
        else:
            h1, w1 = src1.shape[:2]
            h2, w2 = src2.shape[:2]
            vis = np.zeros((max(h1, h2), w1 + w2, 3), np.uint8)
            vis[:h1, :w1] = src1
            vis[:h2, w1:w1 + w2]  = src2
            return vis

    def _fill_skins(self):
        for face_skin in self.face_skins:
            self.skins = self._add_images(face_skin, self.skins)
        self.skins = self._add_images(self.palm_skin, self.skins)
        palm_skin = self.palm_skin
        for row in range(self.skins.shape[0]):
            for col in range(self.skins.shape[1]):
                if any(self.skins[row, col]) == 0:
                    self.skins[row, col] = palm_skin[np.random.randint(0, high=palm_skin.shape[0]), np.random.randint(0, high=palm_skin.shape[1])]

    def _learn_hist(self):
        gray = cv2.cvtColor(self.skins, cv2.COLOR_BGR2GRAY)
        val, mask = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
        hsv = cv2.cvtColor(self.skins, cv2.COLOR_BGR2HSV)
        self.hist = cv2.calcHist([hsv], [0, 1], mask, [36,50], [0, 180, 0, 255])

    def run(self):

        #detector
        self._detector = BProjectionDetector(self.hist)

        #tracker
        self._tracker = CamShiftTracker(self.crit)

        #recognizer
        self._recognizer = HandRecognizer()

        #handler
        self._handler = MouseHandler()
        
        self._fc = cv2.cv.Load(PROJECTDIR + DATAPATHNAME + CLASSIFIERDIRNAME + "fist.xml")
        self._pc = cv2.cv.Load(PROJECTDIR + DATAPATHNAME + CLASSIFIERDIRNAME + "palm.xml")

        frame = self._grabber.grabNext()
        selection = self.selection
        while frame != None:
            temp = frame
            for (x, y, w, h),n in faces:
                cv2.rectangle(frame, (x,y), (x+w, y+2*h), (0, 0, 0), cv.CV_FILLED)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            frame = cv2.medianBlur(frame, 5)
            frame = cv2.calcBackProject([frame], [0, 1], self.hist, ranges=[0, 180, 0, 255], scale=1.0)
            #detection
            frame = self._detector.detect(frame)

            #tracking
            retval, window = self._tracker.track(frame, selection)
            #retval, window = cv2.CamShift(frame, selection, self.crit)
            #print "retval: ", retval

            if window[0] != 0 and window[1] != 0 and window[2] != 0 and window[3] != 0:
                selection = window
            #cv2.rectangle(frame, (int(selection[0] - 0.2 * selection[2]), int(selection[1] - 0.18 * selection[3])), (selection[0] + selection[3], int(selection[1] + 1.8 * selection[2])), (255, 255, 255), 3)
            cv2.rectangle(frame, (int(selection[0] - 0.2 * selection[2]), int(selection[1] - 0.18 * selection[3])), (int(selection[0] + 1.4 * selection[2]), int(selection[1] + selection[3])), (255, 255, 255), 3)

            x = int(selection[0] - 0.2 * selection[2])
            y = int(selection[1] - 0.18 * selection[3])
            w = int(1.8 * selection[2])
            h = int(1.3 * selection[3])

            print x, y, w, h
            if x > 0 and y > 0 and w > 0 and h > 0 and (x + w) < frame.shape[1] and (y + h) < frame.shape[0]:
                #preview = cv.GetSubRect(cv.fromarray(temp), (x, y, w, h))
                #preview = self._recognizer.recognize(temp[y:y+h, x:x+w])
                #preview = self._detector.detect(temp[y:y+h, x:x+w])
                preview = temp[y:y+h, x:x+w]
                #cv2.imshow("hand", np.array(preview))
                cv2.imshow("hand", preview)

            cv2.imshow(self.winname, frame)
            c = cv2.waitKey(1)
            if c == 27:
                cv2.destroyWindow(self.winname)
                cv2.destroyWindow("hand")
                break
            frame = self._grabber.grabNext()
        raw_input()
        cv2.destroyAllWindows()
if __name__ == "__main__":

    try:
        grs = GRS()

        #Initialize first
        grs.initialize()

        #Run the system
        grs.run()
    except IOError, ex:
        print ex.message

    raw_input()
"""