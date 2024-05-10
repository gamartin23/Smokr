function generateJson() {
    var sheet = SpreadsheetApp.getActiveSheet();
    var dataRange = sheet.getRange(1, 1, sheet.getLastRow());
    var values = dataRange.getValues();
    var jsonData = [];
    for (var i = 0; i < values.length; i++) {
      var name = values[i][0];
      var id = "TC" + String(i + 1).padStart(3, "0");
      var jsonObject = {
        "id": id,
        "name": name,
        "android_state": "Untested",
        "ios_state": "Untested",
        "android_comment": "",
        "ios_comment": "",
        "related_issues": []
      };
      jsonData.push(jsonObject);
    }
    var jsonString = JSON.stringify(jsonData, null, 2); // Pretty-print for readability
    sheet.getRange("H2").setValue(jsonString);
  }