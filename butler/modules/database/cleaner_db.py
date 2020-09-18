import threading
from typing import Union

from sqlalchemy import Column, Integer, String, Boolean

from butler import SESSION, BASE


class CleanChatSettings(BASE):
    __tablename__ = "chat_clean_settings"
    chat_id = Column(String(14), primary_key=True)
    should_report = Column(Boolean, default=True)

    def __init__(self, chat_id):
        self.chat_id = str(chat_id)

    def __repr__(self):
        return "<Chat report settings ({})>".format(self.chat_id)

CleanChatSettings.__table__.create(checkfirst=True)

CHAT_LOCK = threading.RLock()

def chat_should_clean(chat_id: Union[str, int]) -> bool:
    try:
        chat_setting = SESSION.query(CleanChatSettings).get(str(chat_id))
        if chat_setting:
            return chat_setting.should_report
        return False
    finally:
        SESSION.close()


def set_chat_setting(chat_id: Union[int, str], setting: bool):
    with CHAT_LOCK:
        chat_setting = SESSION.query(CleanChatSettings).get(str(chat_id))
        if not chat_setting:
            chat_setting = CleanChatSettings(chat_id)

        chat_setting.should_report = setting
        SESSION.add(chat_setting)
        SESSION.commit()