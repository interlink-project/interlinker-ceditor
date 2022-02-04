from app.config import settings
import os

base_url = f"http://{settings.ETHERPAD_SERVICE}"

listAllPads = f"{base_url}/api/1.2.15/listAllPads?apikey={settings.ETHERPAD_API_KEY}"


def createAuthorIfNotExistsFor(authorName, authorMapper):
    return f"{base_url}/api/1.2.15/createAuthorIfNotExistsFor?apikey={settings.ETHERPAD_API_KEY}&name={authorName}&authorMapper={authorMapper}"


def createGroupIfNotExistsFor(groupMapper):
    return f"{base_url}/api/1.2.15/createGroupIfNotExistsFor?apikey={settings.ETHERPAD_API_KEY}&groupMapper={groupMapper}"


def createGroupPad(groupID, padName):
    return f"{base_url}/api/1.2.15/createGroupPad?apikey={settings.ETHERPAD_API_KEY}&groupID={groupID}&padName={padName}&text="


def deletePad(padID):
    return f"{base_url}/api/1.2.15/deletePad?apikey={settings.ETHERPAD_API_KEY}&padID={padID}"


def createSession(groupID, authorID, validUntil=2022201246):
    return f"{base_url}/api/1.2.15/createSession?apikey={settings.ETHERPAD_API_KEY}&groupID={groupID}&authorID={authorID}&validUntil={validUntil}"


def getSessionInfo(sessionID):
    return f"{base_url}/api/1.2.15/getSessionInfo?apikey={settings.ETHERPAD_API_KEY}&sessionID={sessionID}"


def listSessionsOfGroup(groupID):
    return f"{base_url}/api/1.2.15/listSessionsOfGroup?apikey={settings.ETHERPAD_API_KEY}&groupID={groupID}"


def listSessionsOfAuthor(authorID):
    return f"{base_url}/api/1.2.15/listSessionsOfAuthor?apikey={settings.ETHERPAD_API_KEY}&authorID={authorID}"


def getHTML(padID):
    return f"{base_url}/api/1.2.15/getHTML?apikey={settings.ETHERPAD_API_KEY}&padID={padID}"


def setHTML(padID, html):
    return f"{base_url}/api/1.2.15/setHTML?apikey={settings.ETHERPAD_API_KEY}&padID={padID}&html={html}"


def getRevisionsCount(padID):
    return f"{base_url}/api/1.2.15/getRevisionsCount?apikey={settings.ETHERPAD_API_KEY}&padID={padID}"


def padUsers(padID):
    return f"{base_url}/api/1.2.15/padUsers?apikey={settings.ETHERPAD_API_KEY}&padID={padID}"


def getLastEdited(padID):
    return f"{base_url}/api/1.2.15/getLastEdited?apikey={settings.ETHERPAD_API_KEY}&padID={padID}"


if settings.MODE_INTEGRATED or settings.MODE_PRODUCTION:
    domain_url = f"{settings.PROTOCOL}{settings.SERVER_NAME}/{settings.ETHERPAD_HOST}"
else:
    port = os.getenv("ETHERPAD_SOLODEVPORT", "9010")
    domain_url = f"http://localhost:{port}"

def iframeUrl(padID) -> str:
    return f"{domain_url}/p/{padID}"