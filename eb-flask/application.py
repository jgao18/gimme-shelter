from flask import Flask, render_template, request, json, redirect, session
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
import googlemaps.client
import copy
from datetime import datetime, date

app = Flask(__name__)

mysql = MySQL()
app.secret_key = 'secretkey'
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'InShelter'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route("/")
def main():
    if session.get('user'):
        userInfo = {"id": session['id'], "username": session['user'], "firstName": session['fname'], "lastName": session['lname']}
        return render_template('user-home.html', userInfo = userInfo)
    else:
        return render_template('index.html')

@app.route('/showOrgRegPage')
def showOrgRegPage():
    return render_template('org-signup.html')

@app.route('/showUserNavPage')
def showUserNavPage():
    if session.get('user'):
        userInfo = {"id": session['id'], "username": session['user'], "firstName": session['fname'], "lastName": session['lname']}
        return render_template('user-home.html', userInfo = userInfo)
    else:
        return render_template('index.html')
    
@app.route('/showOrgNavPage')
def showOrgNavPage():
    return render_template('org-home.html')
    
@app.route('/showUserProfilePage')
def showUserProfilePage():
    if session.get('user'):
        userInfo = {"id": session['id'], "username": session['user'], "firstName": session['fname'], "lastName": session['lname']}
        return render_template('user-profile.html', userInfo = userInfo)
    else:
        return render_template('index.html')
    
@app.route('/showOrgProfilePage')
def showOrgProfilePage():
    return render_template('org-profile.html')

@app.route('/showErrorPage')
def showErrorPage():
    return render_template('error.html')
    
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
            return json.dumps({'message':str(data[0])})
    else:
        return json.dumps({'message':'missing fields'})

@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['loginUsername']
        _password = request.form['loginPassword']

        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateUserLogin',(_username,))
        data = cursor.fetchall()

        if len(data) > 0:
            print str(data[0][2])
            if check_password_hash(str(data[0][2]),_password):
                session['id'] = data[0][0]
                session['user'] = data[0][1]
                session['fname'] = data[0][3]
                session['lname'] = data[0][4]
                session['location'] = data[0][4]
                session['ssn'] = data[0][5]
                session['dob'] = data[0][6]
                session['sex'] = data[0][7]
                session['phone'] = data[0][8]
                session['email'] = data[0][9]
                session['lang'] = data[0][10]
                session['sleepout'] = data[0][11]
                session['vethl'] = data[0][12]
                session['eserve'] = data[0][13]
                session['harm'] = data[0][14]
                session['legal'] = data[0][15]
                session['exploit'] = data[0][16]
                session['money'] = data[0][17]
                session['meaning'] = data[0][18]
                session['selfcare'] = data[0][19]
                session['social'] = data[0][20]
                session['physical'] = data[0][21]
                session['substance'] = data[0][21]
                session['mental'] = data[0][22]
                session['medication'] = data[0][23]
                session['abuse'] = data[0][24]

                return json.dumps({'message':'success'})
            else:
                return json.dumps({'message':'error'})
        else:
            return json.dumps({'message':'error'})
 
    except Exception as e:
        return json.dumps({'message':'error'})  
    finally:
        cursor.close()
        con.close()

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

@app.route('/saveUserProfile',methods=['POST','GET'])
def saveUserProfile():
    _firstName = request.form['uFirstName'] or None
    _lastName = request.form['uLastName'] or None
    _language = request.form['uLanguage'] or None
    _email = request.form['uEmail'] or None
    _birthday = request.form['uBdayM'] + request.form['uBdayD'] + request.form['uBdayY'] or None
    _gender = request.form['uGender'][0] or None
    _ssn = request.form['uSSN1'] + request.form['uSSN2'] + request.form['uSSN3'] or None
    _phone = request.form['uPhone1'] + request.form['uPhone2'] + request.form['uPhone3'] or None
    _location = request.form['uLocation'] or None
    _sleepout = int(request.form['sleepout'])
    _vethl = int(request.form['vethl'])
    _eserve = int(request.form['eserve'])
    _harm = int(request.form['harm'])
    _legal = int(request.form['legal'])
    _exploit = int(request.form['exploit'])
    _money = int(request.form['money'])
    _meaning = int(request.form['meaning'])
    _selfcare = int(request.form['selfcare'])
    _social = int(request.form['social'])
    _physical = int(request.form['physical'])
    _substance = int(request.form['substance'])
    _mental = int(request.form['mental'])
    _medication = int(request.form['medication'])
    _abuse = int(request.form['abuse'])
	
	# validate the received values
    if True:
        if _birthday != None: 
            _birthday = int(_birthday)
        if _ssn != None: 
            _ssn = int(_ssn)
        if _phone != None: 
            _phone = int(_phone)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_saveProfile',(session['user'], _firstName,_lastName,_language,_email,_birthday,_gender,_ssn,_phone,_location,_sleepout,_vethl,_eserve,_harm,_legal,_exploit,_money,_meaning,_selfcare,_social,_physical,_substance,_mental,_medication,_abuse))

        data = cursor.fetchall()
 
        if len(data) is 0:
            conn.commit()
            return json.dumps({'message':'User modified successfully!'})
        else:
            return json.dumps({'message':str(data[0])})
    else:
        return json.dumps({'message':'errors'})
    
# MATCH CODE
def getPersonLocation(personId):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT Location FROM Resident WHERE Id='" + str(personId) + "';")
    return cursor.fetchone()[0]

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def getElegibleShelters(personId):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT DoB, Sex, Sleep_outside, Veteran_homeless, Emergency_service, Harm, Legal, Exploitation, Money, Meaningful, Self_care, Social, Physical, Substance, Mental, Medication, Abuse FROM Resident where Id = '" + str(personId) + "';")
    personStats = cursor.fetchone()

    dob = personStats[0]
    sex = personStats[1]

    personStats = personStats[2:]

    if dob != None and calculate_age(dob) >= 60:
        personStats = personStats + (1,)
    else:
        personStats = personStats + (0,)

    cursor = conn.cursor()
    cursor.execute("SELECT Id, Takes_men, Takes_women, beds_avail, Sleep_outside, Veteran_homeless, Emergency_service, Harm, Legal, Exploitation, Money, Meaningful, Self_care, Social, Physical, Substance, Mental, Medication, Abuse, Elderly FROM Shelter")
    shelterStats = cursor.fetchall()

    elegible = []
    for shelterStat in shelterStats:
        isElegible = True
        if sex == 'M':
            if shelterStat[1] != 1:
                isElegible = False
        elif sex == 'F':
            if shelterStat[2] != 1:
                isElegible = False

        if shelterStat[3] <= 0:
            isElegible = False

        for i in range(4, len(personStats)):
            if shelterStat[i] != 2 and shelterStat[i] != None and personStats[i] != None: # 2 is don't care condition
                isElegible = isElegible and shelterStat[i] == personStats[i]
        if isElegible:
            elegible.append(shelterStat)

    return [x[0] for x in elegible]

def getShelterInfo(shelterIds):
    conn = mysql.connect()
    cursor = conn.cursor()
    shelterLocs = []

    for i in range(0, len(shelterIds)):

        cursor.execute("SELECT name, addr, beds_avail, closes_by FROM Shelter WHERE Id=" + str(shelterIds[i]) + ";")
        shelterLocs.append(cursor.fetchone())
    return shelterLocs

def convertGmapsData(result, numberOfAddresses):
    rowsArray = result['rows']
    distanceValues = [0 for x in range(numberOfAddresses)]
    distanceText = copy.deepcopy(distanceValues)
    for i in range(0, numberOfAddresses, 1):
        distanceValues[i] = rowsArray[0]['elements'][i]['distance']['value']
        distanceText[i] = rowsArray[0]['elements'][i]['distance']['text']
    return [distanceValues, distanceText]

@app.route('/match',methods=['POST','GET'])
def match():

    personId = session['id'];
    personLocation = getPersonLocation(personId)
    shelters = getElegibleShelters(personId)
    shelterInfo = getShelterInfo(shelters)

    gmaps = googlemaps.Client(key='AIzaSyCfb_q7APSzGK1WSk64s_i-vc6UA-XEFEY')
    y = [str(x[1]) for x in shelterInfo]

    result = gmaps.distance_matrix(personLocation, y)
    if (result['status'] != 'OK'):
        print("Query failed: returned status" + result['status'])
        exit()
    
    rowsDict = result['rows'][0]
    convertedData = convertGmapsData(result, len(shelters))
    
    new = []
    for i in range(0, len(shelters)):
        new.append((convertedData[0][i], shelters[i], convertedData[1][i]) + shelterInfo[i])
    
    new = sorted(new, key=lambda x: x[0])
    #new = [x[1:] for x in new]
    print new

    userInfo = {"id": session['id'], "username": session['user'], "firstName": session['fname'], "lastName": session['lname']}
    return render_template('user-shelters.html', userInfo = userInfo, shelterInfo = new)
    
    # get other relevant data about shelters and package for flask displsy (unknown)

if __name__ == "__main__":

    #con = mysql.connect()
    #cursor = con.cursor()
    #cursor.execute("select * from Resident")
    #print cursor.fetchall()

    app.run()

