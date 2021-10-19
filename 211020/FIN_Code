from db_config import mysql,dic1,dic2,dic3
import pymysql
from hmac import compare_digest
from flask import Flask,jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from datetime import timedelta

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

jwt = JWTManager(app)
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    full_name = db.Column(db.Text, nullable=False)

    # NOTE: In a real application make sure to properly hash and salt passwords
    def check_password(self, password):
        return compare_digest(password, "123456")


# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable format.
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


# Register a callback function that loades a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(username=username).one_or_none()
    if not user or not user.check_password(password):
        return jsonify("Wrong username or password"), 401

    # Notice that we are passing in the actual sqlalchemy user object here
    access_token = create_access_token(identity=user, fresh=timedelta(minutes=60))
    return jsonify(access_token=access_token)


@app.route("/who_am_i", methods=["GET"])
@jwt_required()
def protected():
    # We can now access our sqlalchemy User object via `current_user`.
    return jsonify(
        id=current_user.id,
        full_name=current_user.full_name,
        username=current_user.username,
    )



#----------------------使用者CRUD-------------------------------------------------------------          
@app.route('/addAny', methods=['POST'])                                         #新增 (db:使用者、背包、學習紀錄)
@jwt_required()
def add_Any():
    try:
        _json = request.json
        db = _json['dataBase']
       # C1 = _json['C1']
      #  C2 = _json['C2']
        C1 = _json['C1']
        C2 = _json['C2']
        stuID = _json['stuID']
        
        dicChioe = {}
#        _password = _json['pwd']
        # validate the received values
        if db=="使用者" :
            dicChioe=dic1.copy()
        if db=="學習紀錄":
            dicChioe=dic2.copy()
        if db=="背包":
            dicChioe=dic3.copy()
            
        if db :
            #do not save password as a plain text
#            _hashed_password = generate_password_hash(_password)
            # save edits
            values = ','.join(['%s'] * len(dicChioe)) 
            keys = ','.join(dicChioe.keys()) 
            sql = "INSERT INTO {table}({keys}) VALUES({values})".format(table = db, keys = keys, values = values)
            data = (C1, C2,stuID)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
#            cursor,conn =con(mysql,sql,data)
            resp = jsonify('User added successfully!')
    #        resp.status_code = 200
            cursor.close() 
            conn.close()
            return resp
        

        else:
            return not_found()
    except Exception as e:
        print(e)



@app.route('/users', methods=['GET'])                                           #獲得所有使用者資訊
@jwt_required()
def users():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM 使用者")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()
      
@app.route('/users/<string:db>/<string:id>', methods=['GET'])                  #獲得單一使用者的訊息(db:使用者||背包 id:學號)
@jwt_required()
def user(db,id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute("SELECT * FROM {table} WHERE 學號=%s".format(table = db),id)
        row = cursor.fetchone()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()
        
        

@app.route('/update/<string:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    try:
        _json = request.json
        name = _json['name']
  #      studentID = _json['stuid']
        
        # validate the received values
        if name and request.method == 'PUT':
            #do not save password as a plain text
#            _hashed_password = generate_password_hash(_password)
            # save edits
            sql = "UPDATE 使用者 SET 姓名=%s WHERE 學號=%s"
            data = (name, id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()

#            cursor,conn =con(mysql,sql,data)
            resp = jsonify('User updated successfully!')
#            resp.status_code = 200
            cursor.close() 
            conn.close()
            return resp
            
        else:
            return not_found()
    except Exception as e:
        print(e)


  
@app.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM 使用者 WHERE ID=%s", (id,))
        conn.commit()
        resp = jsonify('User deleted successfully!')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()



@app.route('/addForOne', methods=['PUT'])
@jwt_required()
def add_one():
   try:
        _json = request.json
        db = _json['dataBase']
       # C1 = _json['C1']
        change = _json['change']
        where = _json['where']
        #ChangC = _json['ChangC']
        #V1 = _json['V1']
        
        #change=(C1+"='"+V1+"'")
       # where=(ChangC+"='"+stuID+"'")

#        _password = _json['pwd']
        # validate the received values
        
        if db :
            #do not save password as a plain text
#            _hashed_password = generate_password_hash(_password)
            # save edits

            sql = "update {table} set {change} where {where}".format(table = db,where=where,change=change)
            
            conn = mysql.connect()           
            cursor = conn.cursor()            
            cursor.execute(sql)
            conn.commit()
            
#            cursor,conn =con(mysql,sql,data)
            resp = jsonify('User added successfully!')
    #        resp.status_code = 200
            cursor.close() 
            conn.close()
            return resp
        
        

        else:
            return not_found()
   except Exception as e:
        print(e)



@app.route('/user/<string:db>/<string:id>/<string:thing>/<string:change>', methods=['GET'])                   #獲得的提示ID、道具ID(db:教學紀錄||背包 id:學號)
@jwt_required()
def get_things(db,id,thing,change):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        data=(id,change)
        sql="SELECT * FROM {table} WHERE 學號=%s and {thing}=%s".format(table = db,thing=thing)
        
        cursor.execute(sql,data)
        row = cursor.fetchone()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

@app.route('/CheckUserLoIn', methods=['POST'])
@jwt_required()
def checkUserLoIn():
    try:
        _json = request.json
        name = _json['name']
        pwd = _json['pwd']
#        _password = _json['pwd']
        # validate the received values
        
            #do not save password as a plain text
#            _hashed_password = generate_password_hash(_password)
            # save edits
       
        sql = "SELECT * FROM 使用者 "       
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        rows = cursor.fetchall()
    #    resp = jsonify(rows)
    #        resp.status_code = 200

        cursor.close() 
        conn.close()
        for row in rows:
            if row[1] == name :
                if row[4] == pwd:
                    return "已註冊"
                else :
                    return "密碼錯誤"
        return "此帳號尚未註冊"

    except Exception as e:
        print(e)

        
#----------------------道具CRUD-------------------------------------------------------------    
'''        
@app.route('/Equipment', methods=['POST'])
@jwt_required()
def add_Equipment():
    try:
        _json = request.json
        name = _json['name']
        studentID = _json['stuid']
#        _password = _json['pwd']
        # validate the received values
        if name and studentID and request.method == 'POST'  :
            #do not save password as a plain text
#            _hashed_password = generate_password_hash(_password)
            # save edits
            sql = "INSERT INTO 使用者(姓名, 學號) VALUES(%s, %s)"
            data = (name, studentID)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
#            cursor,conn =con(mysql,sql,data)
            resp = jsonify('User added successfully!')
    #        resp.status_code = 200
            cursor.close() 
            conn.close()
            return resp
        

        else:
            return not_found()
    except Exception as e:
        print(e)



@app.route('/Equipments', methods=['GET'])
@jwt_required()
def Equipments():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM 使用者")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()
      
@app.route('/Equipments/<int:id>', methods=['GET'])
@jwt_required()
def Equipment(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM 使用者 WHERE ID=%s", id)
        row = cursor.fetchone()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()
        
        

@app.route('/update/<int:id>', methods=['PUT'])
@jwt_required()
def update_Equipment(id):
    try:
        _json = request.json
        name = _json['name']
        studentID = _json['stuid']
        
        # validate the received values
        if name and studentID and request.method == 'PUT':
            #do not save password as a plain text
#            _hashed_password = generate_password_hash(_password)
            # save edits
            sql = "UPDATE 使用者 SET 姓名=%s, 學號=%s WHERE ID=%s"
            data = (name,studentID, id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()

#            cursor,conn =con(mysql,sql,data)
            resp = jsonify('User updated successfully!')
#            resp.status_code = 200
            cursor.close() 
            conn.close()
            return resp
            
        else:
            return not_found()
    except Exception as e:
        print(e)


  
@app.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_Equipment(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM 使用者 WHERE ID=%s", (id,))
        conn.commit()
        resp = jsonify('User deleted successfully!')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()
'''
#-----------------------------------------------------------------------------------            
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp
        
if __name__ == "__main__":
    db.create_all()
    db.session.add(User(full_name="LLT", username="abc"))
    db.session.add(User(full_name="Ann Takamaki", username="panther"))
    db.session.add(User(full_name="Jester Lavore", username="little_sapphire"))
    db.session.commit()

    app.run(debug=True)
