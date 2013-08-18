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



#=================================================
#START [Global Assign] ===========================

ROOTFRAMENAME = "GRS-Dev"
DATAPATHNAME = "./data/"
CLASSIFIERDIRNAME = "classifier"
CLASSIFIERFILENAME = "haarcascade_frontalface_default.xml"
#SYSLOGFILENAME = "sys_log.txt"
#SYSLOGFRAMENAME = "System Log"
#EVENTLOGFILENAME = "event_log.txt"
#EVENTLOGFRAMENAME = "Event Log"

#END [Global Assign] =============================

__all__ = [
           "ROOTFRAMENAME",
           "DATAPATHNAME",
           "CLASSIFIERDIRNAME",
           "FACEDETECTCLASSIFIER"
           ]
