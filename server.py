from flask import Flask, jsonify, request
from flask import send_from_directory
from os import listdir, path
import json

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def appstartup():
  try:
        responseJson = []

        applist = request.get_json()

        for i in range (0,len(applist)):
           with open("/home/icharts/icharts/charts/" + applist[i]["regionID"] + "/" + applist[i]["regionID"] + "model.json", "r") as json_data:
            data = json.load(json_data)
            version = data["version"]
            if (version > applist[i]["version"]):
              responseJson.append(data)

        return jsonify(responseJson)

  except Exception, e:
        return(str(e))


@app.route("/charts/", methods=['GET'])
def getAllCharts():
    try:
        responseJson = []
        workingDirPath = "/var/www/iChartsFlaskApp/iChartsFlaskApp/charts"
        for file in listdir(workingDirPath):
            modelDirectory = path.join(workingDirPath, file)
            modelFile = path.join(modelDirectory, file + "model.json")
            if path.isdir(modelDirectory) and path.isfile(modelFile):
                model = open(modelFile, "r")
                responseJson.append(json.load(model))
        return jsonify(responseJson)
    except Exception, e:
        return(str(e))

@app.route("/charts/<city>", methods=['GET'])
def downloadmodel(city):

    try:
        city = city.upper()
        with open("/home/icharts/icharts/charts/" + city + "/" + city + "model.json", "r") as json_data:
            data = json.load(json_data)
            return jsonify(data)

    except Exception, e:
        return(str(e))

@app.route("/charts/<city>/zip", methods=['GET'])
def downloadchart(city):

    try:
        city = city.upper()
        with open("/home/icharts/icharts/charts/" + city + "/" + city + "model.json", "r") as json_data:
            data = json.load(json_data)
            version = data["version"]
            return send_from_directory(directory="/home/icharts/icharts/charts/" + city + "/" + version, filename = city + ".zip")
    except Exception, e:
        return(str(e))


if __name__  == "__main__":
    app.run()
