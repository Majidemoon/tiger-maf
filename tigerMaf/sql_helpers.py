from tigerMaf import SessionLocal
from tigerMaf.models import User, BlockList, DepositAndWithdraw, Message, Settings, DailyChallenge, Duel, Like
from datetime import datetime, timedelta
from sqlalchemy import func, desc

def create_user(user_id, invited_by=None):
    session = SessionLocal()

    try:
        user = User(user_id=user_id, joined_date=datetime.now(), invited_by=invited_by)
        session.add(user)
        session.commit()

    except Exception as e:
        session.rollback()
        print(e)

    finally:
        session.close()


def get_user(user_id, name="", id=0):
    session = SessionLocal()
    if name:
        user = session.query(User).filter_by(name=name).first()
    elif id:
        user = session.query(User).filter_by(id=id).first()
    else:
        user = session.query(User).filter_by(user_id=user_id).first()
    session.close()
    return user

def update_user_name_and_league(user_id, name, league, game_profile, status=1):
    session = SessionLocal()
    user = session.query(User).filter_by(user_id=user_id).first()
    user.name = name
    user.league = league
    user.game_profile = game_profile
    user.status = status
    session.commit()
    session.close()

def check_name(name, user_id):
    """
    returns true if name is not used

    Args:
        name (str): name to check
    
    Returns:
        bool: true if name is not used
    """
    session = SessionLocal()
    user = session.query(User).filter_by(name=name).first()
    session.close()
    if user:
        if user.user_id == user_id:
            return True
        return False
    else:
        return True
    

def get_ubu(blocker, blocked):
    session = SessionLocal()
    
    ubu = session.query(BlockList).filter_by(blocker_user=blocker, blocked_user=blocked).first()

    session.close()
    return ubu

def ubu(blocker, blocked):
    session = SessionLocal()

    ubu = session.query(BlockList).filter_by(blocker_user=blocker, blocked_user=blocked).first()

    if not ubu:
        ubu = BlockList(blocker_user=blocker, blocked_user=blocked, status=0)
        session.add(ubu)
        status = "blocked"
    
    elif ubu.status == 0:
        ubu.status = 1
        status = "unblocked"
    else:
        ubu.status = 0
        status = "blocked"

    
    session.commit()
    session.close()
    return status

def update_balance(user_id, amount):
    session = SessionLocal()
    user = session.query(User).filter_by(user_id=user_id).first()
    user.balance += amount
    session.commit()
    session.close()

def block_unblock_user(user_id):
    session = SessionLocal()

    user = session.query(User).filter_by(user_id=user_id).first()

    if user.status == 0:
        user.status = 1
        status = "unblocked"
    else:
        user.status = 0
        status = "blocked"

    session.commit()
    session.close()
    return status

def deposit_and_withdraw(user_id, amount, type):
    session = SessionLocal()

    deposit = DepositAndWithdraw(user=user_id, amount=amount, type=type, date=datetime.now())
    session.add(deposit)
    session.commit()
    session.close()

def get_last_deposit_and_withdraw(user_id, type):
    session = SessionLocal()

    deposit = session.query(DepositAndWithdraw).filter_by(user=user_id, type=type).order_by(DepositAndWithdraw.id.desc()).first()

    session.close()
    return deposit

def get_users_list(chunks=45, page=1):
    session = SessionLocal()
    users = session.query(User).filter(User.name != None).order_by(User.id).limit(chunks).offset((page-1)*chunks).all()
    user_count = session.query(User).filter(User.name != None).count()
    # users = session.query(User).order_by(User.id).limit(chunks).offset((page-1)*chunks).all()
    # user_count = session.query(User).count()
    session.close()
    return users, user_count

def get_invite_count(user_id, registerd=False):

    session = SessionLocal()
    if registerd:
        invite_count = session.query(User).filter(User.invited_by == user_id, User.name != None).count()
    else:
        invite_count = session.query(User).filter(User.invited_by == user_id).count()

    session.close()
    return invite_count


def add_message(sender, type, message, reciver=None):
    session = SessionLocal()
    message = Message(sender=sender, type=type, reciver=reciver, message=message, date=datetime.now())
    session.add(message)
    session.commit()
    session.close()

def check_daily_broadcast_message(user_id):

    session = SessionLocal()
    message = session.query(Message).filter(Message.sender==user_id, Message.type=="channel", func.date(Message.date)==datetime.now().date()).first()
    session.close()
    if message:
        return True
    else:
        return False
    
def create_settings():
    session = SessionLocal()
    settings = Settings(id=1, bot_on_off=1, channel_photo_lock=1, channel_video_lock=1, channel_gif_lock=1, channel_sticker_lock=1, channel_audio_lock=1, channel_voice_lock=1)
    session.add(settings)
    session.commit()
    session.close()

def get_settings():
    session = SessionLocal()
    settings = session.query(Settings).first()
    session.close()
    return settings

def add_daily_challenge(user_id, dice, value):
    session = SessionLocal()
    daily_challenge = DailyChallenge(user=user_id, dice=dice, value=value, date=datetime.now())
    session.add(daily_challenge)
    session.commit()
    session.close()

def check_daily_challenge(user_id, dice):

    session = SessionLocal()
    daily_challenge = session.query(DailyChallenge).filter(DailyChallenge.user==user_id, DailyChallenge.dice==dice, func.date(DailyChallenge.date)==datetime.now().date()).first()
    session.close()
    if daily_challenge:
        return True
    else:
        return False
    

def add_duel(user, amount, emoji, status):

    session = SessionLocal()
    duel = Duel(user=user, amount=amount, emoji=emoji, status=status, date=datetime.now())
    session.add(duel)
    session.commit()
    session.close()

def get_last_duel(user, emoji):
    session = SessionLocal()
    duel = session.query(Duel).filter(Duel.user==user, Duel.emoji==emoji).order_by(Duel.id.desc()).first()
    session.close()
    return duel

def get_this_week_top_likes(limit=4,last_week=False):

    session = SessionLocal()

    if last_week:
        days_since_saturday = (datetime.now().weekday() + 2) % 7
        end_of_last_week = (datetime.now() - timedelta(days=days_since_saturday)).replace(hour=0, minute=0, second=0, microsecond=0)
        start_of_last_week = end_of_last_week - timedelta(days=7)

        likes_query = session.query(
            Like.liked_user,
            func.count(Like.id).label('like_count')
        ).filter(
            Like.date >= start_of_last_week,
            Like.date < end_of_last_week
        ).group_by(
            Like.liked_user
        ).order_by(
            desc('like_count')
        ).limit(limit).all()

    else:

        # Filters just for this week
        days_since_saturday = (datetime.now().weekday() + 2) % 7 # set saturday as start of week
        start_of_week = (datetime.now() - timedelta(days=days_since_saturday)).replace(hour=0, minute=0, second=0, microsecond=0)

        likes_query = session.query(
            Like.liked_user, 
            func.count(Like.id).label('like_count')
        ).filter(
            Like.date >= start_of_week
        ).group_by(
            Like.liked_user
        ).order_by(
            desc('like_count')
        ).limit(
            limit
        ).all()

    likes = [(like.liked_user, like.like_count) for like in likes_query]

    session.close()

    return likes

def get_like_count(user_id, last_week=False):

    session = SessionLocal()

    if last_week:
        days_since_saturday = (datetime.now().weekday() + 2) % 7
        end_of_last_week = (datetime.now() - timedelta(days=days_since_saturday)).replace(hour=0, minute=0, second=0, microsecond=0)
        start_of_last_week = end_of_last_week - timedelta(days=7)

        like_count = session.query(
            func.count(
                Like.id
            ).label(
                'like_count'
            )
        ).filter(
            Like.liked_user==user_id, 
            Like.date >= start_of_last_week, 
            Like.date < end_of_last_week
        ).scalar()
    
    else:
        # Filters just for this week
        days_since_saturday = (datetime.now().weekday() + 2) % 7 # set saturday as start of week
        start_of_week = (datetime.now() - timedelta(days=days_since_saturday)).replace(hour=0, minute=0, second=0, microsecond=0)

        like_count = session.query(func.count(Like.id).label('like_count')).filter(Like.liked_user==user_id, Like.date >= start_of_week).scalar()
    session.close()
    return like_count

def like_user(liker_user, liked_user):

    session = SessionLocal()
    like = Like(liker_user=liker_user, liked_user=liked_user, date=datetime.now())
    session.add(like)
    session.commit()
    session.close()

def get_user_daily_liked_count(user_id):
    session = SessionLocal()
    like_count = session.query(func.count(Like.id).label('like_count')).filter(Like.liked_user==user_id, Like.date >= datetime.now() - timedelta(days=1)).scalar()
    session.close()
    return like_count

def check_like_user(liker_user, liked_user):

    days_since_saturday = (datetime.now().weekday() + 2) % 7 # set saturday as start of week
    start_of_week = datetime.now() - timedelta(days=days_since_saturday)

    session = SessionLocal()
    like = session.query(Like).filter(Like.liker_user==liker_user, Like.liked_user==liked_user, Like.date >= start_of_week).first()
    session.close()
    if like:
        return True
    else:
        return False
    
def toggle_brodcast_locks(column_name):

    session = SessionLocal()
    settings = session.query(Settings).first()

    if settings:
        current_value = getattr(settings, column_name)
        new_value = 1 if current_value == 0 else 0

        setattr(settings, column_name, new_value)

        session.commit()
        session.close()

def updtate_settings(column_name, value):

    session = SessionLocal()
    settings = session.query(Settings).first()

    if settings:
        setattr(settings, column_name, value)

        session.commit()
        session.close()

def update_user_status(user_id, status):
    session = SessionLocal()
    user = session.query(User).filter_by(user_id=user_id).first()
    user.status = status
    session.commit()
    session.close()

def duel_list(week=False):

    session = SessionLocal()
    limit = 100

    if week:
    # Filters just for this week
        days_since_saturday = (datetime.now().weekday() + 2) % 7 # set saturday as start of week
        start_of_week = (datetime.now() - timedelta(days=days_since_saturday)).replace(hour=0, minute=0, second=0, microsecond=0)

        likes_query = session.query(
            Duel.user, 
            func.count(Duel.id).label('duel_count')
        ).filter(
            Duel.date >= start_of_week
        ).group_by(
            Duel.user
        ).order_by(
            desc('duel_count')
        ).limit(
            limit
        ).all()

    else:

        likes_query = session.query(
            Duel.user, 
            func.count(Duel.id).label('duel_count')
        ).group_by(
            Duel.user
        ).order_by(
            desc('duel_count')
        ).limit(
            limit
        ).all()

    duels = [(duel.user, duel.duel_count) for duel in likes_query]

    session.close()

    return duels

def duel_count(user_id, week=False, type="all"):

    days_since_saturday = (datetime.now().weekday() + 2) % 7 # set saturday as start of week
    start_of_week = (datetime.now() - timedelta(days=days_since_saturday)).replace(hour=0, minute=0, second=0, microsecond=0)

    session = SessionLocal()
    duel_query = session.query(
        func.count(Duel.id).label("duel_count")
    ).filter(
        Duel.user == user_id,
        Duel.status == 1 if type == "win" else Duel.status == 0 if type == "lose" else 1 == 1,
        Duel.date >= start_of_week if week else 1 == 1
    ).scalar()

    session.close()

    return duel_query

def get_last_channel_message(user_id):

    session = SessionLocal()

    last_message = session.query(Message).filter(Message.type=="channel", Message.sender==user_id).first()

    session.close()

    return last_message