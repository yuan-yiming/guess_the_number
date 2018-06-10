# encoding:utf8

from exts import db

class Player(db.Model):
	__tablename__ = 'players'
	id = db.Column(db.Integer,primary_key=True)
	nickname = db.Column(db.String(11),nullable=False,unique=True)   # 玩家昵称
	play_times = db.Column(db.Integer,nullable=False)   # 游戏次数
	top_score = db.Column(db.Integer)   # 最高分