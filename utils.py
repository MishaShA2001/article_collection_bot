"""All supporting functions for handling messages from users"""
from re import compile
from dataclasses import dataclass
from typing import Literal, Optional


URL_PATTERN = compile(r'\A(https?|ftp|file)://.+\Z')


@dataclass
class Event:
    action_datetime: str
    link: str
    action: Literal['save', 'get']


def check_link(text: str) -> bool:
    """
    :param text:
    :return:
    """
    result = URL_PATTERN.match(text)
    if result:
        return True
    return False


def check_natural_number(text: str) -> Optional[bool]:
    """
    :param text:
    :return:
    """
    try:
        if int(text) > 0:
            return True
        return False
    except ValueError:
        return False


def generate_event_message(events: list[Event]) -> str:
    """
    :param events:
    :return:
    """
    event_message = ''
    action_meaning = {
        'save': 'Вы сохранили статью',
        'get': 'Вы получили статью'
    }
    for event in events:
        event_message += (f'{event.action_datetime}: '
                          f'{action_meaning[event.action]} {event.link}\n')
    return event_message
