import threading

from sqlalchemy import Column, String

from Thedakkidaikkathaval.modules.sql import BASE, SESSION



class RakisChats(BASE):
    __tablename__ = "rakis_chats"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id

RakisChats.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()


def is_rakis(chat_id):
    try:
        chat = SESSION.query(RakisChats).get(str(chat_id))
        return bool(chat)
    finally:
        SESSION.close()

def set_rakis(chat_id):
    with INSERTION_LOCK:
        rakischat = SESSION.query(RakisChats).get(str(chat_id))
        if not rakischat:
            rakischat = RakisChats(str(chat_id))
        SESSION.add(rakischat)
        SESSION.commit()

def rem_rakis(chat_id):
    with INSERTION_LOCK:
        rakischat = SESSION.query(RakisChats).get(str(chat_id))
        if rakischat:
            SESSION.delete(rakischat)
        SESSION.commit()
