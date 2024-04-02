import requests
import json
import os

#Scripts with functions import
#from utilities import *
#from gtfs-flex-upload-clifford import *
#from pipelines-clifford import *
from Part1_Learning_Functions import *

token = authenticate3(USERNAME, PASSWORD)
project_groups = list_project_groups(token)
