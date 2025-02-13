from sqlalchemy import create_engine, Column, Integer, Text, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    name = Column(Text)
    league = Column(Text)
    balance = Column(Float, default=0)
    status = Column(Integer, default=1) # 0 : block, 1 : unblock
    invited_by = Column(Integer)
    game_profile = Column(Text)
    joined_date = Column(DateTime)

class BlockList(Base):
    __tablename__ = "block_list"

    id = Column(Integer, primary_key=True, autoincrement=True)
    blocker_user = Column(Integer)
    blocked_user = Column(Integer)
    status = Column(Integer, default=0) # 0 : block, 1 : unblock, 2 : cant send message to channel

class DepositAndWithdraw(Base):
    __tablename__ = "deposit_and_withdraw"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(Integer)
    amount = Column(Float)
    type = Column(Text) # deposit or withdraw
    date = Column(DateTime)

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sender = Column(Integer)
    type = Column(Text) # direct, annonymous, channel, support, admin
    reciver = Column(Integer)
    message = Column(Text)
    date = Column(DateTime)

class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, default=1, primary_key=True)
    bot_on_off = Column(Integer, default=1)
    channel_photo_lock = Column(Integer, default=1)
    channel_video_lock = Column(Integer, default=1)
    channel_gif_lock = Column(Integer, default=1)
    channel_sticker_lock = Column(Integer, default=1)
    channel_audio_lock = Column(Integer, default=1)
    channel_voice_lock = Column(Integer, default=1)
    invite_coin = Column(Integer, default=5)
    like_challenge_number_one = Column(Integer, default=500)
    like_challenge_number_two = Column(Integer, default=250)
    like_challenge_number_three = Column(Integer, default=100)
    like_challenge_number_four = Column(Integer, default=50)
    minimum_withdraw = Column(Integer, default=100)
    maximum_duel = Column(Integer, default=50)
    minimum_duel = Column(Integer, default=5)
    daily_challenge_coin_dice = Column(Integer, default=5)
    daily_challenge_coin_dart = Column(Integer, default=5)
    daily_challenge_coin_bowling = Column(Integer, default=5)
    daily_challenge_coin_basketball = Column(Integer, default=5)
    daily_challenge_coin_football = Column(Integer, default=5)
    daily_challenge_coin_cazino = Column(Integer, default=10) 

class DailyChallenge(Base):
    __tablename__ = "daily_challenge"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(Integer)
    dice = Column(Integer)
    value = Column(Integer)
    date = Column(DateTime)

class Duel(Base):
    __tablename__ = "duel"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(Integer)
    amount = Column(Integer)
    emoji = Column(Text)
    status = Column(Integer)
    date = Column(DateTime)

class Like(Base):
    __tablename__ = "like"

    id = Column(Integer, primary_key=True, autoincrement=True)
    liker_user = Column(Integer)
    liked_user = Column(Integer)
    date = Column(DateTime)

DATABASE_URL = 'sqlite:///database.db'
engine = create_engine(DATABASE_URL, echo=True)

session = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)