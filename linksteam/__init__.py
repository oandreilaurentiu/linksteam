import ts3lib, ts3defines, devtools
from ts3plugin import ts3plugin
from json import loads
from PythonQt.QtCore import Qt, QUrl
from PythonQt.QtGui import QMessageBox, QDialog, QDesktopServices
from PythonQt.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

class testplugin(ts3plugin):
    name = "Link Steam"
    requestAutoload = False
    version = "1"
    apiVersion = 21
    author = "OhanesianAndreiLaurentiu"
    description = "Link Steam, add a feature in teamspeak 3 where you can click a steam link and is open in your steam client instead of your default browser."
    offersConfigure = False
    commandKeyword = ""
    infoTitle = ""
    menuItems = []
    hotkeys = []
    domains = [
        "steamcommunity.com",
        "store.steampowered.com"
    ]
    updateurl = "https://raw.githubusercontent.com/oandreilaurentiu/linksteam/master/version.json"
    repourl = "https://github.com/{}/{}/releases".format(author, name)

    def __init__(self):
        ts3lib.printMessageToCurrentTab("Steamlinker " + self.version + " loaded")
        self.nwmc = QNetworkAccessManager()
        self.nwmc.connect("finished(QNetworkReply*)", self.updateReply)
        self.nwmc.get(QNetworkRequest(QUrl(self.updateurl)))

    def updateReply(self, reply):
        version = loads(reply.readAll().data().decode('utf-8'))["version"]
        if version != self.version:
            x = QDialog()
            x.setAttribute(Qt.WA_DeleteOnClose)
            _x = QMessageBox.question(x, "{} v{} by {}".format(self.name, self.version, self.author), "Noua versiune v{} la linksteam a fost gasita, dai update acum?".format(version), QMessageBox.Yes, QMessageBox.No)
            if _x == QMessageBox.Yes:
                QDesktopServices.openUrl(QUrl(self.repourl))

    def onTextMessageEvent(self, schid, targetMode, toID, fromID, fromName, fromUniqueIdentifier, message, ffIgnored):
        for url in self.domains:
            if url in message:
                ts3lib.printMessageToCurrentTab("[URL=steam://openurl/" + message[5:-6] + "]Open in Steam.[/URL]")
                return
