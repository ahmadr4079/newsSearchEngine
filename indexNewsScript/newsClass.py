import json
import glob

class NewsData:
    def getData(self):
        result = []
        for f in glob.glob('*.json'):
            with open(f) as jsonFile:
                result = result + json.load(jsonFile)
        return result