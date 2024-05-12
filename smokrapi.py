from flask import Flask, request, jsonify
import os, sys
import json
import random
import copy
import string

app = Flask(__name__)

def resourcePath(relativePath):  # Function for relative paths
  basePath=getattr(sys,'_MEIPASS',os.path.dirname(os.path.abspath(__file__)))
  return os.path.join(basePath,relativePath)

# Load template data (assuming template.json exists)
template_data = None
try:
  with open(resourcePath('template.json'), 'r') as dataf:
    template_data = json.load(dataf)
except FileNotFoundError:
  print("Error: template.json not found!")

class SmokeData:
  def __init__(self):
    self.data = None
    self.load_template()
  
  def load_template(self):
    if template_data is None:
      print('Its none')
      return
    self.data = copy.deepcopy(template_data)
    self.generate_uuid()

  def generate_uuid(self):
    alphabet = string.ascii_uppercase
    self.uuid = ''.join(random.choice(alphabet) for _ in range(6))

  def get_data(self):
    return self.data

  def save_data(self, filename):
    try:
      with open(resourcePath(filename), 'w') as outfile:
        json.dump(self.data, outfile, indent=4)
    except Exception as e:
      return False, f"Failed to save data: {str(e)}"
    return True, "Data saved successfully."

smoke_data = SmokeData()  # Create an instance of SmokeData

@app.route("/new_smoke", methods=["GET"])
def new_smoke():
  smoke_data.load_template()  # Load data and generate UUID
  return smoke_data.get_data()

@app.route("/", methods=["GET"])
def get_all_items():
  if smoke_data.data is not None:
    return smoke_data.get_data()
  else:
    return jsonify({"message": "No data available yet. Use /new_smoke to create one."})

@app.route("/done", methods=["GET"])
def done():
  if smoke_data.data is None:
    return jsonify({"error": "No data to save"}), 400
  success, message = smoke_data.save_data(f"{smoke_data.uuid}.json")
  smoke_data.data = None  # Clear data after save
  smoke_data.uuid = None
  return jsonify({"message": message})

@app.route("/<int:item_id>", methods=["PUT"])
def update_item_completely(item_id):
  if smoke_data.data is None:
    return jsonify({"error": "No data available"}), 400
  
  try:
    item_to_update = smoke_data.data[item_id]
  except KeyError:
    return jsonify({"error": "Item not found"}), 404

  # Update item data as before
  item_to_update["android_state"] = request.json["android_state"]
  item_to_update["ios_state"] = request.json["ios_state"]
  item_to_update["comments"] = request.json["comments"]
  item_to_update["related_issues"] = request.json["related_issues"]
  return jsonify(smoke_data.get_data()), 200 # OK status code

@app.route("/debug/uuid")
def get_debug_uuid():
  if smoke_data.uuid is not None:
    return jsonify({"uuid": smoke_data.uuid})
  else:
    return jsonify({'message': 'No smoke test is being run'})

if __name__ == "__main__":
  app.run(debug=False)
