from app.config import settings

base_url = "http://proxy/etherpad"
domain = f"http://localhost"
listAllPads = f"{base_url}/api/1/listAllPads?apikey={settings.ETHERPAD_API_KEY}"


def createAuthorIfNotExistsFor(authorName, authorMapper):
    return f"{base_url}/api/1/createAuthorIfNotExistsFor?apikey={settings.ETHERPAD_API_KEY}&name={authorName}&authorMapper={authorMapper}"


def createGroupIfNotExistsFor(groupMapper):
    return f"{base_url}/api/1/createGroupIfNotExistsFor?apikey={settings.ETHERPAD_API_KEY}&groupMapper={groupMapper}"


def createGroupPad(groupID, padName):
    return f"{base_url}/api/1/createGroupPad?apikey={settings.ETHERPAD_API_KEY}&groupID={groupID}&padName={padName}&text=This is the first sentence in the pad"


def createSession(groupID, authorID, validUntil=2022201246):
    return f"{base_url}/api/1/createSession?apikey={settings.ETHERPAD_API_KEY}&groupID={groupID}&authorID={authorID}&validUntil={validUntil}"


def iframeUrl(sessionID, groupID, padName):
    return f"{domain}/etherpad/auth_session?sessionID={sessionID}&groupID={groupID}&padName={padName}"


def getSessionInfo(sessionID):
    return f"{base_url}/api/1/getSessionInfo?apikey={settings.ETHERPAD_API_KEY}&sessionID={sessionID}"


def listSessionsOfGroup(groupID):
    return f"{base_url}/api/1/listSessionsOfGroup?apikey={settings.ETHERPAD_API_KEY}&groupID={groupID}"


def listSessionsOfAuthor(authorID):
    return f"{base_url}/api/1/listSessionsOfAuthor?apikey={settings.ETHERPAD_API_KEY}&authorID={authorID}"


def getHTML(padID):
    return f"{base_url}/api/1/getHTML?apikey={settings.ETHERPAD_API_KEY}&padID={padID}"

def setHTML(padID, html):
    return f"{base_url}/api/1/setHTML?apikey={settings.ETHERPAD_API_KEY}&padID={padID}&html={html}"


def getRevisionsCount(padID):
    return f"{base_url}/api/1/getRevisionsCount?apikey={settings.ETHERPAD_API_KEY}&padID={padID}"


def padUsers(padID):
    return f"{base_url}/api/1/padUsers?apikey={settings.ETHERPAD_API_KEY}&padID={padID}"


def getLastEdited(padID):
    return f"{base_url}/api/1/getLastEdited?apikey={settings.ETHERPAD_API_KEY}&padID={padID}"
