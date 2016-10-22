from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route("/")
def main():
    print "HIIIIIIIIIIIII"
    return render_template('homepage.html')

#@app.route('/showSignUp')
#def showSignUp():
  #  print "watffae"
   # return render_template('homepage.html')

@app.route('/signUp',methods=['POST','GET'])
def signUp():

    print "HELLLOOO?!?!?!?"
    print "ETRTREFDSDSFASDF"
	
    # read the posted values from the UI
    _name = request.form['inputName']
    print "QQQQQQQQQQQQQQQQQQQQQQq"
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
	
    print "ABCDEF"
	
    print _name
    print _email
    print _password
	
    print "ABC"
 
    # validate the received values
    if _name and _email and _password:
        json.dumps({'message':'User created successfully !'})
        
        conn = mysql.connect()
        cursor = conn.cursor()
        _hashed_password = generate_password_hash(_password)
        print "hi"
        cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
        print "hello"

        data = cursor.fetchall()
 
        if len(data) is 0:
            conn.commit()
            return json.dumps({'message':'User created successfully !'})
        else:
            return json.dumps({'error':str(data[0])})
    else:
        print "no"
        print "123"
        return json.dumps({'html':'<span>Enter the required fields</span>'})

if __name__ == "__main__":
    app.run()
