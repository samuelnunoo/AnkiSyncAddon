import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

#Anki Stuff
from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo

import json
import time
import os


class GoogleAccess:
  def __init__(self):

    #Folder Parameters
    self.owner = 'samuelnunoo@mail.com'
    self.title = 'Anki'
    self.folder = None

    #Authentication Information
    os.chdir(os.path.dirname(__file__))
    self.gauth = GoogleAuth()
    self.gauth.LocalWebserverAuth()
    self.drive = GoogleDrive(self.gauth)

  def Sequence(self):
  

    
    files = self.getFiles(self.getFolderID())

    #Testing
    self.downloadFiles(files)
    converted_json = self.convertJSON('sync.json')
    showInfo(str(converted_json))
    self.updateDB(converted_json)
    showInfo('Database Updated')
    os.remove("sync.json")

  def getFolderID(self):
    while self.folder == None:
      self.folder = self.drive.ListFile(
      {'q': " '{0}' in owners and mimeType = 'application/vnd.google-apps.folder' and title = '{1}' ".format(
      self.owner, self.title)}).GetList()
    return self.folder[0]['id']

  def getFiles(self,folder_id):
    _q = {'q': "'{}' in parents and trashed=false".format(folder_id)}
    return self.drive.ListFile(_q).GetList()

  def downloadFiles(self,files):
    for file in files:
      file.GetContentFile('sync.json')

  def convertJSON(self,json_file):
    with open(json_file) as f:
      return json.load(f)

  def updateDB(self,new_list):
    mw.col.db.executemany("update notes set tags = ? where id = ? ",new_list)
    
    

class AnkiGui:
  def __init__(self):
    self.action = QAction("Card Sync", mw)
    self.action.triggered.connect(self.Start)
    mw.form.menuTools.addAction(self.action)

  def Start(self):
    drive = GoogleAccess()
    drive.Sequence()



gui = AnkiGui()
