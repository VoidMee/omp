"""
    Created on August 18, 2013

    @author: Surendra Lama

    [Module 'constants"]
        Parent packages - cfg -> grs
        Sub-packages - None

    Description:
    This module is considered for initializing
    definitions for the system.

"""
#=================================================

#START [Global Definitions] ======================

global ROOTFRAMENAME
#global SYSLOGFRAMENAME
#global EVENTLOGFRAMENAME

global DATAPATHNAME
global CLASSIFIERDIRNAME
#global SYSTEMLOGDIRNAME

global FACEDETECTCLASSIFIER
#global SYSLOGFILENAME
#global EVENTLOGFILENAME

#END [Global Defintions] =========================

global MAXCAMERAINDEX


#=================================================
#START [Global Assign] ===========================

ROOTFRAMENAME = "GRS-Dev"
DATAPATHNAME = "./data/"
CLASSIFIERDIRNAME = "classifier"
FACEDETECTCLASSIFIER = "haarcascade_frontalface_default.xml"
#SYSLOGFILENAME = "sys_log.txt"
#SYSLOGFRAMENAME = "System Log"
#EVENTLOGFILENAME = "event_log.txt"
#EVENTLOGFRAMENAME = "Event Log"

MAXCAMERAINDEX = 3

#END [Global Assign] =============================

__all__ = [
           "ROOTFRAMENAME",
           "DATAPATHNAME",
           "CLASSIFIERDIRNAME",
           "FACEDETECTCLASSIFIER",
           "MAXCAMERAINDEX"
           ]