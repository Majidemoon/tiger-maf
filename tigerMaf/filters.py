from telethon import events
from tigerMaf import STEP, ADMIN, COMMANDS_LIST
from telethon.tl.types import (
    DocumentAttributeAnimated, 
    DocumentAttributeVideo, 
    MessageMediaDocument, 
    DocumentAttributeSticker, 
    MessageMediaDice,
    MessageMediaWebPage
)

def is_private(event : events.NewMessage.Event):
    return event.is_private

def forward_check(event : events.NewMessage.Event):
    return event.fwd_from

def step(event, step_name : str):

    if isinstance(event , events.NewMessage.Event):
        if event.raw_text in COMMANDS_LIST:
            return False

    if not STEP.get(str(event.sender_id)):
        STEP[str(event.sender_id)] = ("home", )

    if STEP.get(str(event.sender_id))[0] == step_name:
        return True

    return False

def is_text(event : events.NewMessage.Event):
    if event.raw_text:
        return True
    return False

def is_photo(event : events.NewMessage.Event):
    if event.photo:
        return True
    return False

def is_media(event : events.NewMessage.Event):
    if event.media:
        message = event.message
        if isinstance(message.media, MessageMediaWebPage):
            return False
        return True
    return False

def is_video(event : events.NewMessage.Event):
    if event.video:
        if not is_gif(event) and not is_sticker(event):
            return True
    return False

def is_gif(event : events.NewMessage.Event):

    message = event.message

    if isinstance(message.media, MessageMediaDocument):
        document = message.media.document
        has_video_attr = False
        is_animated = False

        for attr in document.attributes:
            if isinstance(attr, DocumentAttributeVideo) and attr.nosound:
                has_video_attr = True
            if isinstance(attr, DocumentAttributeAnimated):
                is_animated = True
        
        # Condition for GIF
        if has_video_attr and is_animated:
            return True
        else:
            return False
        
    return False

def is_sticker(event : events.NewMessage.Event):
    
    message = event.message

    if isinstance(message.media, MessageMediaDocument):
        document = message.media.document
        
        for attr in document.attributes:
            if isinstance(attr, DocumentAttributeSticker):
                return True

    return False

def is_audio(event : events.NewMessage.Event):
    if event.audio:
        return True
    return False

def is_voice(event : events.NewMessage.Event):

    message = event.message

    if isinstance(message.media, MessageMediaDocument):
        if message.media.voice:
            return True
    return False

def is_dice(event : events.NewMessage.Event, emoji : str):
    
    message = event.message

    if message.media:
        if isinstance(message.media, MessageMediaDice):
            if message.media.emoticon == emoji:
                return True
    return False

def is_sudo(event):

    return event.sender_id == ADMIN
