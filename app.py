# coding = 'utf-8'

import random
import config
from flask import Flask,render_template,flash,session,redirect,url_for,request,abort
from flask_script import Manager
from exts import db  
from models import Player
from flask import send_from_directory

app = Flask(__name__)   # 实例化一个程序

app.config.from_object(config)   # 导入配置项

db.init_app(app)
manager = Manager(app)

# 首页路由
@app.route('/', methods=['GET', 'POST'])   # methods=['GET', 'POST']
def index():
	if request.method == 'GET':
		return render_template('index.html')
	else:
		nickname = request.form.get('nick-name') or session.get('nickname')
		if nickname :
			player = Player.query.filter_by(nickname=nickname).first()   # 从数据库中查询玩家
			if player is None:
				player = Player(nickname=nickname,play_times=0,top_score=10)
				db.session.add(player)   # 数据库增加
				db.session.commit()
				print('增加一个新玩家：',nickname)
				session['nickname'] = nickname
				return redirect(url_for('guessthenumber'))
			else:
				print(nickname,':是一个旧玩家',)
				session['nickname'] = nickname   #会话对象。是一个全局对象？？下面的路由也可以使用？？
				#session.permanent = True
				return redirect(url_for('guessthenumber'))
		else:
			flash('请输入你的名字！')
			return render_template('index.html')


# 猜数字游戏路由
@app.route('/guessthenumber', methods=['GET', 'POST'])
def guessthenumber():
	player = Player.query.filter_by(nickname=session['nickname']).first()   # 数据库查询
	if request.method == 'GET':
		session['chances'] = 10
		session['set_number'] = random.randint(1,1000)
		session['number1'] = 0
		session['number2'] = 1000
		return render_template('guessthenumber.html')
	elif request.form.get('guess-number') == '':
		flash('请输入一个整数！')
		return render_template('guessthenumber.html')
	else:
		session['chances'] -= 1
		print('要猜的数字：',session['set_number'])
		guess_number = int(request.form.get('guess-number'))
		
		if guess_number > session['set_number']:
			session['number2'] = guess_number
			if session.get('chances') == 0:
				player.play_times += 1
				db.session.add(player)
				db.session.commit()
				flash('Game Over！要不再玩一次？')
				return redirect(url_for('index'))
			flash('数字太大了，在{}~{}之中再猜一个！'.format(session['number1'],session['number2']))
			return render_template('guessthenumber.html')
		
		if guess_number < session['set_number']:
			session['number1'] = guess_number
			if session.get('chances') == 0:
				player.play_times += 1
				db.session.add(player)
				db.session.commit()
				flash('Game Over！要不再玩一次？')
				return redirect(url_for('index'))
			flash('数字太小了，在{}~{}之中再猜一个！'.format(session['number1'],session['number2']))
			return render_template('guessthenumber.html')
		
		else:
			flash('恭喜你用了{}次机会就猜对了数字！'.format(10-session['chances']))
			player.play_times += 1
			if player.top_score == None:
				player.top_score = 10-session['chances']
			else:
				player.top_score = min(player.top_score,10-session['chances'])
			db.session.add(player)
			db.session.commit()
			return redirect(url_for('index'))

# 退出登录
@app.route('/logout')
def logout():
	del session['nickname']
	return redirect(url_for('index'))

# 玩家排名的路由
@app.route('/rank')
def rank():
	players = Player.query.order_by(Player.top_score).all()   # 按最高分顺序查询所有玩家
	return render_template('rank.html',players=players)

# 游戏规则页面
@app.route('/rule')
def rule():
	return render_template('rule.html')

# 上下文处理器
@app.context_processor   
def my_context_processor():
	nickname = session.get('nickname')
	if nickname:
			return {'nickname':nickname}
	return {}    # 被该修饰器修饰的函数必须返回一个字典，即使是空字典

# 错误页面
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
		
if __name__ == '__main__':
	manager.run()