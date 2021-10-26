from flaskext.mysql import MySQL
import flask
#-------------------------------------------------
dic1={'姓名 ':None,
      '學號 ':None,
      '密碼 ':None,
     }
dic2={'提示ID ':None,
      '關卡名稱 ':None,
      '學號 ':None,
     }
dic3={'道具ID ':None,
      '數量 ':None,
      '學號 ':None,
     }
#-------------------------------------------------
mysql = MySQL() 

app = flask.Flask(__name__)
# MySQL 配置
app.config['MYSQL_DATABASE_USER'] = 'root' 
app.config['MYSQL_DATABASE_PASSWORD'] = '123456' 
app.config['MYSQL_DATABASE_DB'] = 'fin' 
app.config['MYSQL_DATABASE_HOST' ] = 'localhost' 
mysql.init_app(app)

