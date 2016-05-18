from flask import Flask, render_template, json, request, session, redirect
from functools import wraps
from flask.ext.session import Session
from werkzeug import generate_password_hash, check_password_hash
import backend_functions
import AD

app = Flask(__name__)

SESSION_TYPE = 'filesystem'
PERMANENT_SESSION_LIFETIME = 180
app.config.from_object(__name__)
Session(app)

switch_info = ['xx.xx.xx.xx name_sw','xx.xx.xx.xx name_sw2','xx.xx.xx.xx name_sw3']

def isAuthed(func):
 @wraps(func)
 def decorated_function(*args, **kwargs):
   print "ENTREI NESTA MERDA"
   try:
      if "auth" not in session or session["auth"] != True:
        raise Exception("NOT AUTHORIZED")
      else:
        return func(*args, **kwargs)
   except:
        #OOPS
        redirect_to_index = redirect('/')
        response = app.make_response(redirect_to_index )
        return response

 return decorated_function

##### LOGIN #######
@app.route("/login", methods=["POST"])
def login():

    #if backend_functions.login(request.form["username"], request.form["password"],request.form["ip"]):
    a = AD.ApiLDAP()
    if a.authenticate("uk\\"+ request.form["username"], request.form["password"]):

        #### Login #####
        session["auth"] = True
        session["username"] = request.form["username"]
        session["password"] = request.form["password"]
        session["ip"] = request.form["ip"]
        session["ip_name"] = backend_functions.getNameSW(session["ip"],switch_info)
        print "ENTREI CRL"
        return redirect("/Menu", code=302)
    else:
        return render_template("invalid_login.html",ERROR_MSG="Authentication Failed")

##### LOGOUT#######
@app.route("/logOut", methods=["POST"])
@isAuthed
def logOut():
        session["auth"] = False
        #### LogOut #####
        print "LOGOUT CARALHO"
        return render_template('/')

##### MAIN PAGE #####
@app.route('/')
def main():

    tmpRet= backend_functions.list_switches(switch_info)
    return render_template('login.html',switch_info=tmpRet)


@app.route('/Menu')
@isAuthed
def Menu():
    return render_template('index.html')

####### CONFIGURE PORT ##########
@app.route('/NewSwitchport')
@isAuthed
def Switchport():
    print "VAMOS SWITCHPORT CRL!"
    ### GENERATE FILE FOR INTERFACES
    interface_file = backend_functions.generate_interface_file(session["ip"])
    print "ALO-->"+interface_file
    #### LIST ALL THE INTERFACES OF SW
    tmpRet = backend_functions.list_interfaces(interface_file)
    return render_template('switchport.html' , ip=session["ip_name"] , interface_list=tmpRet)

@app.route('/SwitchportResult', methods=['POST'])
@isAuthed
def Switchport_Submit():
    try:
        print "FODASSS"
        print "ISSO --> " + session["ip"] + "\n" + session["username"] +"\n" + request.form["inputInt"] +"\n" + request.form["inputDes"] + "\n" +  request.form["inputVlanID"]
        result = []
        ## OUTPUT
        #result = "VAMOS CRL " + request.form["inputInt"] +"\n " + request.form["inputDes"] + "\n " +  request.form["inputVlanID"]
        result = backend_functions.new_config_switchport(session["ip"],request.form["inputInt"],request.form["inputDes"],request.form["inputVlanID"])
        return render_template('switchportresult.html' , output=result )
    except:
         #OPS
         return render_template('switchportresult.html' , output="Push not works as expected!" )

####### DISABLED PORT ##########

@app.route('/DisableSwitchport')
@isAuthed
def DisableSwitchport():
    print "VAMOS SWITCHPORT DISABLED CRL!"
    ### GENERATE FILE FOR INTERFACES
    interface_file = backend_functions.generate_interface_file(session["ip"])
    print "ALO-->"+interface_file
    #### LIST ALL THE INTERFACES OF SW
    tmpRet = backend_functions.list_interfaces(interface_file)
    return render_template('switchportdisable.html' ,ip=session["ip_name"],interface_list=tmpRet)

@app.route('/SwitchportDisableResult', methods=['POST'])
@isAuthed
def Switchport_Disable_Submit():
    try:
        print "CARALHO!"
        print "ISSO --> " + session["ip"] + "\n" + session["username"] +"\n" + request.form["inputInt"] +"\n"
        result = []
        ## OUTPUT
        #result = "VAMOS CRL " + request.form["inputInt"] +"\n " + request.form["inputDes"] + "\n " +  request.form["inputVlanID"]
        result = backend_functions.disable_switchport(session["ip"],request.form["inputInt"])
        return render_template('switchportdisableresult.html' , output=result )
    except:
         #OPS
         return render_template('switchportdisableresult.html' , output="Push not works as expected!" )

####### SHOW PORT #######
@app.route('/ShowSwitchport')
@isAuthed
def ShowSwitchport():
    print "VAMOS SWITCHPORT SHOW CRL!"
    ### GENERATE FILE FOR INTERFACES
    interface_file = backend_functions.generate_interface_file(session["ip"])
    print "ALO-->"+interface_file
    #### LIST ALL THE INTERFACES OF SW
    tmpRet = backend_functions.list_interfaces(interface_file)
    return render_template('SwitchportShow.html' , ip=session["ip_name"], interface_list=tmpRet)

@app.route('/SwitchportShowResult', methods=['POST'])
@isAuthed
def Switchport_Show_Submit():
    #try:
        print "CARALHO!"
        print "ISSO --> " + session["ip"] + "\n" + session["username"] +"\n" + request.form["inputInt"] +"\n"
        result = []
        ## OUTPUT
        #result = "VAMOS CRL " + request.form["inputInt"] +"\n " + request.form["inputDes"] + "\n " +  request.form["inputVlanID"]
        result = backend_functions.checkconfig_switchport(session["ip"],request.form["inputInt"])
        return render_template('SwitchportShowResult.html' , output=result )
    #except:
         #OPS
         #return render_template('SwitchportShowResult.html' , output="Push not works as expected!" )



if __name__ == "__main__":
    app.run(debug=True)
