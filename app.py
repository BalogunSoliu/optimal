from email import message
from tabnanny import check
from unicodedata import category
from werkzeug.security import generate_password_hash
from flask import Flask, render_template, request, redirect, url_for, session,flash
import pandas as pd
import random

from postgre_database import *


global username
global password
global first_name
global last_name
global Email
global Job_Skill
global Other_telephone
global House_Address
global Date_of_Birth
global Experience
global Local_Government
global State
        
Email=''
### ---------------------------------------------------------- 
### ---------------------- Login Page ------------------------
app=Flask(__name__)
app.secret_key = 'mrlantop'
 
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404 
@app.errorhandler(500)
def internal_server(e):
    return render_template('500.html'), 500

@app.route('/', methods=['POST','GET'])
@app.route('/login', methods=['POST','GET'])
def login():

    global username
    global password
    global first_name
    global last_name
    global Email
    global Job_Skill
    global Other_telephone
    global House_Address
    global Date_of_Birth
    global Experience
    global Local_Government
    global State
    global link

    if session.get("username") != None:
        return redirect(url_for('benefit'))
    else:
        if request.method=="POST": 
            username=request.form['username']
            password=request.form["password"]

            if username.startswith('0'):
                username='+234' + username[1:]
            else:
                username = '+234' + username[-10:]
    
            check,first_name, last_name,Email,link,p_status=loginto(username,password)

            session['link']=link
            session['username']=username
            session['first_name']=first_name
            session['last_name']=last_name
        

            session['Email']=Email
            session['pstatus']=p_status
            #session['pstatus']=confirmpayment(username)
            
            
            if check=='correct_password':
                           
                return redirect(url_for('benefit'))
            else:
                return render_template('login.html', msg=check, username=username)

        return render_template("login.html")

@app.route('/faq')
def faq():
    return render_template("FAQ.html")

@app.route('/optimal')
def optimal():
    return redirect("http://optimalng.com")

global  totp

#===========================================================================
### ------------------ Registration Page -------------------
@app.route('/register',methods = ['GET','POST'])
def register():
    global data
    global chg
    global  referral_code
    global  parent_referral
    global  totp

    session['chg']=False
    #parent_referral=""
    
    
    if request.method =='GET':
        
        referral_code=request.args.get('referral')
        referral_link="http://community.optimalng.com/register?referral=" + str(referral_code)
        print('ref1',referral_link[-7:],referral_link)
        referral_code=get_parent_phone(referral_link)
        session['referral_code']=referral_code
        print('ref2',session['referral_code'])
        return render_template('register.html',rphone=session['referral_code'])
        


    if request.method=="POST":

        number=request.form["telephone"]
        cnumber = request.form['ctelephone']
        rnumber = request.form['rphone']
        password1 = request.form['password']
        password2 = request.form['comfirm']
        email = request.form['email']
        last_name = request.form['lastname']
        first_name = request.form['firstname']
        gender = request.form['Gender'][0]

    try:
        if number.startswith('0'):
            number='+234' + number[1:]
            cnumber='+234' + cnumber[1:]
            
        else:
            number = '+234' + number[-10:]
            cnumber = '+234' + cnumber[-10:]
        
        if rnumber.startswith('0'):
            rnumber='+234' + rnumber[1:]
        elif rnumber=='':
            rnumber=''
        else:
            rnumber = '+234' + rnumber[-10:]
        
        if len(first_name) < 2:
            flash('Firstname must be greater than two characters.', category='error')
        elif password1!=password2:
            flash('passwords don\'t match.', category='error')
        elif password1!=password2:
            flash('passwords don\'t match.', category='error')
        elif number!=cnumber:
            print(number,cnumber)
            flash('Telephone numbers don\'t match.', category='error')
        elif len(password1) < 7:
            flash('password must be greater than seven characters.', category='error')

        else:
            data={'First_Name':first_name,
                'Last_Name':last_name,
                'Phone_Number':number,
                'Email':email,
                'password':generate_password_hash(password1, method='sha256'),
                'Gender':gender,
                'Referral_Link':'http://community.optimalng.com/register?referral='+first_name+'_'+number[6:],
                'Payment_Status':'Basic',
                'PARENT_PHONE_NUMBER': rnumber
                }
            session['data']=data
            session['Email'] = data['Email']
            session['link']=data['Referral_Link']
            session['username']=data['Phone_Number']
            session['first_name']=data['First_Name']
            session['last_name']=data['Last_Name']
            session['link']=data['Referral_Link']
            session['password'] = data['password']
            session['gender'] = data['Gender']
            session['pstatus']=data['Payment_Status']
            session['PARENT_PHONE_NUMBER']=data['PARENT_PHONE_NUMBER']
            username=data['Phone_Number']
            check=checkusername(username)
            print(check)

            if not check:
                print('not exist',check)
                return redirect(url_for('captcha'))
                
            else:
                print('exist',check)
                flash('User already exist', category='error')
                
    except Exception as e:
        print(e)
        render_template('register.html', msg='Invalid Number')

      
    return render_template('register.html')

### ---------------------------------------------------------- 
### ---------------------- Captcha Function------------------------

@app.route('/captcha', methods=['POST','GET'])
def captcha():
    a = random.choice(range(10))
    b = random.choice(range(10))
    if request.method=='POST':
        q_ans1 = request.form['QA1'].lower()
        q_ans2 = request.form['QA2'].lower()
        question1 = request.form['question1']
        question2 = request.form['question2']

        data = session['data']
        answer = int(request.form['answer'])
        value1 = int(request.form['a'])
        value2 = int(request.form['b'])
        print(question1,q_ans1)

        if question1 == question2:
            flash('You can\'t choose the same questions', category='error')

        elif answer != sum([value2,value1]):
            flash('Incorrect, try again!', category='error')

        else:
            data={'First_Name':session['first_name'],
                'Last_Name':session['last_name'],
                'Phone_Number':session['username'],
                'Email':session['Email'],
                'password':session['password'],
                'Gender':session['gender'],
                'Referral_Link':session['link'],
                'Payment_Status':session['pstatus'],
                'PARENT_PHONE_NUMBER': session['PARENT_PHONE_NUMBER'],
                'Security_Q1':question1,
                'Security_Q2':question2,
                'Security_A1':q_ans1,
                'Security_A2':q_ans2,
                }
            try:#insert data
                
                insertdata(data)
                #print(data,'df.head')    
            except:
                render_template('error.html')

            return render_template('welcome.html',name=session['first_name'])
    

    return render_template('captcha.html',a=a,b=b)

### ---------------------------------------------------------- 
### ---------------------- Dashboard Function------------------------  
    
@app.route('/dashboard',methods = ['GET','POST'])
def dashboard():

    username = session['username']
    first_name = session['first_name']
    last_name = session['last_name']
    return render_template('dashboard.html',phone=username,first_name=first_name.capitalize(),
                                    last_name=last_name.capitalize())

### ---------------------------------------------------------- -----------
### ----------------------OTP Validation  Function ------------------------  
       
@app.route('/passwordreset',methods = ['GET','POST'])
def passwordreset():
    if request.method=="POST": 
        q1=request.form['q1'].lower()
        q2=request.form['q2'].lower()
        a1=request.form['a1'].lower()
        a2=request.form['a2'].lower()
        password=request.form["password"]
        rpassword = request.form['Cpassword']
        print(q1,a1)
        
        if (q1==a1 and q2==a2) and (password==rpassword):
            changepassworddb(session['username'],generate_password_hash(password, method='sha256'))
            return render_template('login.html', message='Password reset successfull.')

        else:
            return render_template('changepassword2.html',q1=session['q1'],q2=session['q2'],a1=session['a1'],a2=session['a2'],msg='Incorrect security answers. Please provide the right answers!')

### ---------------------------------------------------------- -----------
### ----------------------Password REQUEST/forgot passord Function ------------------------  
@app.route('/forgotp', methods=['POST','GET'])
def forgotp():

    if request.method=="POST": 
        username=request.form['username']

        if username.startswith('0'):
            username='+234' + username[1:]
        else:
            username = '+234' + username[-10:]

        q1,q2,a1,a2,check=checkuser(username)  
        
        if check =='exist':
             session['q1']  = q1
             session['q2']  = q2
             session['a1']  = a1
             session['a2']  = a2
             session['username']  = username
             return render_template('changepassword2.html',q1=q1,q2=q2,a1=a1,a2=a2)
        else:
            return render_template('forgotp.html', msg='user not found')

    return render_template('forgotp.html')

@app.route('/business',methods = ['GET','POST'])
def business():
    global username
    global password
    global first_name
    global last_name
    global Email
    global Job_Skill
    global Other_telephone
    global House_Address
    global Date_of_Birth
    global Experience
    global Local_Government
    global State

    first_name=session['first_name']
    username=session['username']
    last_name =session['last_name']

    Email = session['Email']
    
    return render_template('dashboard.html',phone=username,first_name=first_name.capitalize(),
                                    last_name=last_name.capitalize(),  p_status=session['pstatus'])

@app.route('/manage',methods = ['GET','POST'])
def manage():
    
    global username
    global password
    global first_name
    global last_name
    global Email
    global Job_Skill
    global Other_telephone
    global House_Address
    global Date_of_Birth
    global Experience
    global Local_Government
    global State

    a = random.choice(range(10))
    b = random.choice(range(10))

    first_name=session['first_name']
    username=session['username']
    last_name =session['last_name'] 

    Email = session['Email'] 

    
    return render_template('manageaccount.html', email=Email, phone_number=username,first_name=first_name.upper(),
                                    last_name=last_name.upper(),  p_status=session['pstatus'],a=a,b=b+1)

@app.route('/update',methods = ['GET','POST'])
def update():

    a = random.choice(range(10))
    b = random.choice(range(10))

    first_name=session['first_name']
    username=session['username']
    last_name =session['last_name'] 

    Email = session['Email']

    if request.method=="POST": 
        first_name=request.form['first_name']
        last_name=request.form["last_name"]
        Email=request.form['email']
        username = request.form['phone']
        captcha = int(request.form['answer'])
        a = int(request.form['a'])
        b = int(request.form['b'])
        print('aaaaaa',captcha)
        
        if captcha == sum([a,b]):
            updateprofile(username,first_name,last_name,Email)
            return render_template('manageaccount.html',email=Email, phone_number=username,first_name=first_name.upper(),
                                    last_name=last_name.upper(),  p_status=session['pstatus'],a=a,b=b+1, messag='your profile has been updated successfully')

        else:
            return render_template('manageaccount.html',email=Email, phone_number=username,first_name=first_name.upper(),
                                    last_name=last_name.upper(),  p_status=session['pstatus'],a=a,b=b+1,   message='Profile update error, Incorrect captcha. Please try again!')


@app.route('/updatepassword',methods = ['GET','POST'])
def updatepassword():
    if request.method=="POST": 
        username=request.form['phone']
        password=request.form["password"]
        rpassword = request.form['rpassword']
        captcha = int(request.form['answer'])
        a = int(request.form['a'])
        b = int(request.form['b'])
        print('aaaaaa',captcha)
        
        if captcha == sum([a,b]) and rpassword==password:
            changepassworddb(username,generate_password_hash(password, method='sha256'))
            return render_template('manageaccount.html', messag='you profile has been updated successfully')

        else:
             return render_template('manageaccount.html', message='Profile update error, please fill the required fields correctly and try again!')

@app.route('/logout')
def logout():


    session.clear()
    
    return redirect(url_for('login'))


@app.route('/benefit status')
def benefit():
    global username
    global password
    global first_name
    global last_name
    global Email
    global Job_Skill
    global Other_telephone
    global House_Address
    global Date_of_Birth
    global Experience
    global Local_Government
    global State

    first_name=session['first_name']
    username=session['username']
    last_name =session['last_name']

    Email = session['Email'] 

    df=getref(username)
    if session['pstatus']=='Baic':
        session['pstatus']='Basic'
     
    #df=df.set_index('Phone number')
    return render_template('benefit.html',phone=username,first_name=first_name.capitalize(),
                                    last_name=last_name.capitalize(),
                                    df=df, phone_number=username,A=len(df),p_status=session['pstatus'])

@app.route('/payment',methods = ['GET','POST'])
def payment():
    global username
    global password
    global first_name
    global last_name
    global Email
    global Job_Skill
    global Other_telephone
    global House_Address
    global Date_of_Birth
    global Experience
    global Local_Government
    global State

    first_name=session['first_name']
    username=session['username']
    last_name =session['last_name']

    Email = session['Email']
    
    return render_template('makepayment.html',phone=username,first_name=first_name.capitalize(),
                                    last_name=last_name.capitalize(), p_status=session['pstatus'])

@app.route('/shareable',methods = ['GET','POST'])
def shareable():
    global username
    global password
    global first_name
    global last_name
    global Email
    global Job_Skill
    global Other_telephone
    global House_Address
    global Date_of_Birth
    global Experience
    global Local_Government
    global State

    first_name=session['first_name']
    username=session['username']
    last_name =session['last_name']
    Email = session['Email']

    link=session['link']
    
    return render_template('shareable.html',referral=link,phone=username,first_name=first_name.capitalize(),
                                    last_name=last_name.capitalize(), p_status=session['pstatus'])

@app.route('/mypayment',methods = ['GET','POST'])
def mypayment():
    global first_name
    global last_name
    global Email
    global username

    first_name=session['first_name']
    username=session['username']
    last_name =session['last_name']

    
    try:
        paymentlink=getpaymentlink(first_name,last_name,username,Email)
            
        return redirect(paymentlink)
    except:
        return render_template('makepayment.html',phone=username,first_name=first_name.capitalize(),
                                    last_name=last_name.capitalize(), p_status=session['pstatus'])

    
@app.route('/dispute', methods = ['GET','POST'])
def dispute():

    
    username=session['username']
  
    if request.method=='POST':
        category = request.form['category']
        email = request.form['email']
        phone = request.form['phone']
        comment = request.form['comment']
        data = {
            'Phone_Number':'+234'+phone[-10:],
            'Email':email,
            'Category':category,
            'Comment':comment
        }
        disputedata(data)
        msg='We have received your message, we\'ll get back to you shortly!'
        print(msg)

        return render_template('dispute.html', phone=username,msg=msg)

    
    return render_template('dispute.html', phone=username)

@app.route('/admin', methods = ['GET','POST'])
def admin():
    
      session['Admin']=''
                   
      return render_template('adminlogin.html')

@app.route('/paymentfile', methods = ['GET','POST'])
def paymentfile():
    
    if request.method == 'POST':
        username=request.form['username']

        if username.startswith('0'):
            username='+234' + username[1:]
        else:
            username = '+234' + username[-10:] 
        try:
            pfile(username)
        except Exception as e:
            print(e)
        df = session['df']
        return render_template('admindb.html', tables=[df.to_html(classes='data')], titles='Registration Database')
    
    
    

@app.route('/admindb', methods = ['GET','POST'])
def admindb():
  
    try:
        if request.method=="POST": 
            username=request.form['username']
            password=request.form["password"]


        if username=='optimal' and password=='optimaladmin1234':
            session['Admin']='optimaladmin1234'
          
        if session['Admin']=='optimaladmin1234':
            df = getdatabaserecord()
            df=df.drop(['password','Security_Q1','Security_Q2','Security_A1','Security_A2'],axis=1)
            session['df'] = df
            return render_template('admindb.html', tables=[df.to_html(classes='data')], titles='Registration Database')
    
    except:
        return render_template('admindb.html', msg='not an admin')
    


if __name__=='__main__':
   
    app.run(debug=True)
