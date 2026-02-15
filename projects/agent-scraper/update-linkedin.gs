function addLinkedInColumn() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName("Sheet2");
  
  // LinkedIn data - company name to LinkedIn URL mapping
  var linkedinData = {
    "Cyprian Star Estates": "https://www.linkedin.com/in/stephanie-natiotis-0a98621ab/",
    "ANDREAS CHARALAMBOUS PROPERTIES": "https://cy.linkedin.com/in/andreas-charalambous-a4384665",
    "KALAMON HOMES": "https://www.linkedin.com/in/maria-constantinou-2a6216b6/",
    "DESTATE LTD": "https://www.linkedin.com/in/elena-stavrou-56aa2016/",
    "First class Homes LTD": "https://cy.linkedin.com/in/anna-philippou-40286363",
    "Foytina Real Estate Agency": "https://www.linkedin.com/in/kyriakos-foutas-812a535b/",
    "Next Home Estate Agency": "https://www.linkedin.com/in/andreas-nicolaou-934b72ab/",
    "P.Pericleous Real Estate": "https://www.linkedin.com/in/pericles/",
    "SOTIRIS AVRAAM": "https://www.linkedin.com/in/sotiris-avraam-and-sons-ba6603248/"
  };
  
  // Add header in column G
  sheet.getRange("G1").setValue("LinkedIn");
  
  // Get all company names from column A
  var lastRow = sheet.getLastRow();
  var companies = sheet.getRange("A2:A" + lastRow).getValues();
  
  // Fill in LinkedIn URLs
  for (var i = 0; i < companies.length; i++) {
    var company = companies[i][0].trim().toUpperCase();
    var linkedin = "";
    
    // Check each key in linkedinData
    for (var key in linkedinData) {
      if (company === key.toUpperCase() || company.includes(key.toUpperCase()) || key.toUpperCase().includes(company)) {
        linkedin = linkedinData[key];
        break;
      }
    }
    
    sheet.getRange("G" + (i + 2)).setValue(linkedin);
  }
  
  Logger.log("LinkedIn column added successfully!");
}
