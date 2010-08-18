prefService = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefService);
branch = prefService.getBranch("extensions.redminetoolbar.");
branch.deleteBranch("projects.name");
branch.deleteBranch("projects.url");
// and add them again
projects = [['https://simplesnet.com.br/suporte','tangrama'],];

for (var i = 0; i < projects.length; i++){
    var items = projects[i];
    branch.setCharPref("projects.url." + i, items[0]);
    branch.setCharPref("projects.name." + i, items[1]);
}