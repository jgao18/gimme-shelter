from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'InShelter'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route("/")
def main():
    return render_template('index.html')

@app.route('/showOrgRegPage')
def showOrgRegPage():
    return render_template('org-signup.html')

@app.route('/showUserNavPage')
def showUserNavPage():
    return render_template('user-home.html')
    
@app.route('/showOrgNavPage')
def showOrgNavPage():
    return render_template('org-home.html')
    
@app.route('/showUserProfilePage')
def showUserProfilePage():
    return render_template('user-profile.html')
    
@app.route('/showOrgProfilePage')
def showOrgProfilePage():
    return render_template('org-profile.html')
    

@app.route('/signUp',methods=['POST','GET'])
def signUp():
    
    # read the posted values from the UI
    _firstName = request.form['inputFirstName']
    _lastName = request.form['inputLastName']
    _username = request.form['inputUsername']
    _password = request.form['inputPassword']
 
    # validate the received values
    if _firstName and _lastName and _username and _password:
        json.dumps({'message':'User created successfully !'})
        
        conn = mysql.connect()
        cursor = conn.cursor()
        _hashed_password = generate_password_hash(_password)
        cursor.callproc('sp_createResident',(_firstName,_lastName,_username,_hashed_password))

        data = cursor.fetchall()
 
        if len(data) is 0:
            conn.commit()
            return json.dumps({'message':'User created successfully !', 'username':_username, 'firstName':_firstName, 'lastName':_lastName,})
        else:
            return json.dumps({'error':str(data[0])})
    else:
        return json.dumps({'message':'missing fields'})

if __name__ == "__main__":
    app.run()
