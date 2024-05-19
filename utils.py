"""All supporting functions for handling messages from users"""
from re import compile
from dataclasses import dataclass
from typing import Literal

from content.messages import messages


LINK_PATTERN = compile(
    r'(?:https?://|ftps?://|www\.)(?:(?![.,?!;:()]*(?:\s|$))\S){2,}')


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
    result = LINK_PATTERN.match(text)
    if result:
        return True
    return False


def generate_event_message(events: list[Event]) -> str:
    """
    :param events:
    :return:
    """
    if events:
        event_message = messages['get_history_default']
        action_meaning = {
            'save': 'я сохранил статью',
            'get': 'я отдал статью'
        }
        for event in events:
            event_message += (f'{event.action_datetime}: '
                              f'{action_meaning[event.action]} {event.link}\n')
        return event_message
    return messages['get_history_failure']
