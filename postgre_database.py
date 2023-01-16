from sqlalchemy import *
import pandas as pd
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
import pyotp
import sqlite3
import pandas as pd
from paystackapi.paystack import Paystack
import http.client
from datetime import datetime
from datetime import timedelta

def pfile(username):
    engine=create_engine('postgresql://tditwfmicyyirg:3d3e2a88480e8cf780186d9c8abe79c80232a5f7c46f8c6bc7629a04ba83204e@ec2-44-194-6-121.compute-1.amazonaws.com:5432/da2hbfp8pegd88')
    
    dbConnection    = engine.connect();

    df=pd.read_sql("select * from registration",dbConnection)
    df=df.set_index('Phone_Number')

    df2=df.loc[username]

    df2.Payment_Status='Paid'

    df.loc[username]=[df2.First_Name,df2.Last_Name,df2.Email,df2.Gender,df2.Referral_Link,df2.Payment_Status, df2.password,df2.PARENT_PHONE_NUMBER,df2.Security_Q1,df2.Security_Q2,df2.Security_A1,df2.Security_A2]

    df.to_sql('registration', dbConnection, if_exists='replace')


    dbConnection.close()
    

def insertdata(data):
    #Connect to the server (Postgres Database on Heroku)
    engine=create_engine('postgresql://tditwfmicyyirg:3d3e2a88480e8cf780186d9c8abe79c80232a5f7c46f8c6bc7629a04ba83204e@ec2-44-194-6-121.compute-1.amazonaws.com:5432/da2hbfp8pegd88')
    dbConnection    = engine.connect();

    df=pd.read_sql("select * from registration",dbConnection)
    df=df.set_index('Phone_Number')

    df.loc[data['Phone_Number']]=[data['First_Name'],
                                     data['Last_Name'],
                                     data['Email'],
                                     data['Gender'],
                                     data['Referral_Link'],
                                     data['Payment_Status'],
                                     data['password'],
                                      data['PARENT_PHONE_NUMBER'],
                                      data['Security_Q1'],
                                      data['Security_Q2'],
                                      data['Security_A1'],
                                      data['Security_A2']]
    
    print(df)
    df.to_sql('registration', dbConnection, if_exists='replace')
    

    dbConnection.close()
 

def loginto(username,password):

    #Connect to the server (Postgres Database on Heroku)
    engine=create_engine('postgresql://tditwfmicyyirg:3d3e2a88480e8cf780186d9c8abe79c80232a5f7c46f8c6bc7629a04ba83204e@ec2-44-194-6-121.compute-1.amazonaws.com:5432/da2hbfp8pegd88')

    dbConnection    = engine.connect();
    df=pd.read_sql("select * from registration",dbConnection)


    #df[df['Phone_Number'].str.startswith('+')]=df['Phone_Number'].str[1:]
    
    df=df.set_index('Phone_Number')
    print(list(df.index))
    try :

        if username in list(df.index):
            df2=df.loc[username]

            if not check_password_hash(df2.password,password):#df2.password!=password:
                check="wrong password"
                print(df2.password,password)
                first_name,last_name,Email,link,p_status=1,2,3,4,5
            
            else:
                check='correct_password'
                first_name=df2.First_Name
                last_name=df2.Last_Name
                Email=df2.Email
                link=df2.Referral_Link 
                p_status = df2.Payment_Status
                
        else:
            check='user not found'
            first_name,last_name,Email,link,p_status=1,2,3,4,5
            

        
                           
        
    except Exception as e:
        print(e)
        check='user not found'
        first_name,last_name,Email,link,p_status=1,2,3,4,5

    return check, first_name, last_name,Email,link,p_status


   
    
    
def checkusername(username):
    #Connect to the server (Postgres Database on Heroku)
    engine=create_engine('postgresql://tditwfmicyyirg:3d3e2a88480e8cf780186d9c8abe79c80232a5f7c46f8c6bc7629a04ba83204e@ec2-44-194-6-121.compute-1.amazonaws.com:5432/da2hbfp8pegd88')
    
    dbConnection    = engine.connect();

    df=pd.read_sql("select * from registration",dbConnection)
    df=df.set_index('Phone_Number')
    usernames=list(df.index)

    if username in usernames:
        return True
    else:
        return False


def get_parent_phone(referral_link):


    #Connect to the server (Postgres Database on Heroku)
    #Connect to the server (Postgres Database on Heroku)
    engine=create_engine('postgresql://tditwfmicyyirg:3d3e2a88480e8cf780186d9c8abe79c80232a5f7c46f8c6bc7629a04ba83204e@ec2-44-194-6-121.compute-1.amazonaws.com:5432/da2hbfp8pegd88')
        
    dbConnection    = engine.connect();
    #referral_link='https://optimalcommunity.herokuapp.com/register?referral=Balogun_68400456'
    df=pd.read_sql("select * from registration ",dbConnection) 
    df = df[df.Referral_Link==referral_link]
    #print('phone',list(df.Phone_Number)[0])
    try:
        if list(df.Phone_Number)[0][-7:] == referral_link[-7:]:
            return list(df.Phone_Number)[0]
        else:
            print('hhhh')
            return ''
    except Exception as e:
        print(e)
        return ''

        
    

def addcareer2(username,skill,otel,state,lga,address,dob,experience,Email):
       #Connect to the server (Postgres Database on Heroku)
       engine=create_engine('postgresql://tditwfmicyyirg:3d3e2a88480e8cf780186d9c8abe79c80232a5f7c46f8c6bc7629a04ba83204e@ec2-44-194-6-121.compute-1.amazonaws.com:5432/da2hbfp8pegd88')
                            
       dbConnection    = engine.connect();
    
       df=pd.read_sql("select * from career_job",dbConnection)

       df=df.set_index('telephone')
       df.loc[username]=[skill,otel,Email,state,lga,address,dob,experience]

       df.to_sql('career_job', dbConnection, if_exists='replace')
       dbConnection.close()


def checkuser(username):
    
    #Connect to the server (Postgres Database on Heroku)
    engine=create_engine('postgresql://tditwfmicyyirg:3d3e2a88480e8cf780186d9c8abe79c80232a5f7c46f8c6bc7629a04ba83204e@ec2-44-194-6-121.compute-1.amazonaws.com:5432/da2hbfp8pegd88')
    
    dbConnection    = engine.connect();

    df=pd.read_sql("select * from registration",dbConnection)
    df=df.set_index('Phone_Number')
    try:
        if username in list(df.index):

            df2=df.loc[username]
            q1=df2.Security_Q1
            q2 = df2.Security_Q2
            a1 = df2.Security_A1
            a2 = df2.Security_A2
            check = 'exist'
        else:
            check = 'user not found'
            q1,q2,a1,a2,check=1,2,3,4,check

        return q1,q2,a1,a2,check
    except Exception as e:
        check = 'user not found'
        print(e)
        q1,q2,a1,a2,check=1,2,3,4,check

        return q1,q2,a1,a2,check

    



def changepassworddb(username,newpassword):
    
    #Connect to the server (Postgres Database on Heroku)
    engine=create_engine('postgresql://tditwfmicyyirg:3d3e2a88480e8cf780186d9c8abe79c80232a5f7c46f8c6bc7629a04ba83204e@ec2-44-194-6-121.compute-1.amazonaws.com:5432/da2hbfp8pegd88')
    
    dbConnection    = engine.connect();

    df=pd.read_sql("select * from registration",dbConnection)
    df=df.set_index('Phone_Number')

    df2=df.loc[username]

    df2.password=newpassword

    df.loc[username]=[df2.First_Name,df2.Last_Name,df2.Email,df2.Gender,df2.Referral_Link,df2.Payment_Status, df2.password,df2.PARENT_PHONE_NUMBER,df2.Security_Q1,df2.Security_Q2,df2.Security_A1,df2.Security_A2]

    df.to_sql('registration', dbConnection, if_exists='replace')


    dbConnection.close()

    
def updateprofile(username,First_Name,Last_Name,Email):

    #Connect to the server (Postgres Database on Heroku)
    engine=create_engine('postgresql://tditwfmicyyirg:3d3e2a88480e8cf780186d9c8abe79c80232a5f7c46f8c6bc7629a04ba83204e@ec2-44-194-6-121.compute-1.amazonaws.com:5432/da2hbfp8pegd88')
    
    dbConnection = engine.connect();

    df=pd.read_sql("select * from registration",dbConnection)
    df=df.set_index('Phone_Number')

    df2=df.loc[username]

    df.loc[username]=[First_Name,Last_Name,Email,df2.Gender,df2.Referral_Link,df2.Payment_Status,df2.password,df2.PARENT_PHONE_NUMBER,df2.Security_Q1,df2.Security_Q2,df2.Security_A1,df2.Security_A2]

    df.to_sql('registration', dbConnection, if_exists='replace')

    dbConnection.close()

def getref(username):

    engine=create_engine('postgresql://tditwfmicyyirg:3d3e2a88480e8cf780186d9c8abe79c80232a5f7c46f8c6bc7629a04ba83204e@ec2-44-194-6-121.compute-1.amazonaws.com:5432/da2hbfp8pegd88')
        
    dbConnection    = engine.connect();

    df=pd.read_sql(f'''SELECT * FROM registration WHERE "PARENT_PHONE_NUMBER" = '{username}' ''',dbConnection)
    print(df)
    return df



   


#=============================================================================
#==================GENERATION OF OTP FOR USER TO CREATE ACCOUNT================

def getpaymentlink(firstname,lastname,phonenumber,email):
    
    paystack_secret_key = "sk_live_100961388d035de59e0e955b516e6d4a0f18adfa"
    paystack = Paystack(secret_key=paystack_secret_key)

    response = paystack.customer.create(first_name=firstname,
                               last_name=lastname,
                               email=email, phone=phonenumber)

    customer_id=response['data']['customer_code']


    response=paystack.invoice.create( customer=customer_id,
                amount=60000,
                note='Optimal Community payment',
                due_date=str(datetime.now() + timedelta(days=90)))
    
    paymentlink="https://paystack.com/pay/" +  response['data']['request_code']
    
    return paymentlink


def gettree(username):

    
    #Connect to the server (Postgres Database on Heroku)
    engine=create_engine('postgresql://tditwfmicyyirg:3d3e2a88480e8cf780186d9c8abe79c80232a5f7c46f8c6bc7629a04ba83204e@ec2-44-194-6-121.compute-1.amazonaws.com:5432/da2hbfp8pegd88')
    
                         
    dbConnection    = engine.connect();

    df=pd.read_sql("select * from registration",dbConnection)

    print(df)

    print(username)
    parent_phone_df=df[df['PARENT_PHONE_NUMBER']==username]

    check = not(parent_phone_df.empty)

    phone_number=[]
    referral=[]
    payment_status=[]
    
    while check:
        
        phone_number.append(list(parent_phone_df['Phone_Number'])[0])

        payment_status.append(list(parent_phone_df['Payment_Status'])[0])
        
        referral.append(username)

        print(parent_phone_df)
        username=list(parent_phone_df['Phone_Number'])[0]
         
        parent_phone_df=df[df['PARENT_PHONE_NUMBER']==username]

        
        if parent_phone_df.empty:
            break
        check = not(parent_phone_df.empty)

    df2=pd.DataFrame(data={'Phone number':phone_number,
                           'Referral': referral,
                            'Payment Status': payment_status})


    return df2

def getdatabaserecord():

    engine=create_engine('postgresql://tditwfmicyyirg:3d3e2a88480e8cf780186d9c8abe79c80232a5f7c46f8c6bc7629a04ba83204e@ec2-44-194-6-121.compute-1.amazonaws.com:5432/da2hbfp8pegd88')
    dbConnection    = engine.connect();

    df=pd.read_sql("select * from registration",dbConnection)
    df=df.set_index('Phone_Number')

    return df
def disputedata(data):
    #Connect to the server (Postgres Database on Heroku)
    engine=create_engine('postgresql://tditwfmicyyirg:3d3e2a88480e8cf780186d9c8abe79c80232a5f7c46f8c6bc7629a04ba83204e@ec2-44-194-6-121.compute-1.amazonaws.com:5432/da2hbfp8pegd88')
    dbConnection    = engine.connect();

    df=pd.read_sql("select * from dispute",dbConnection)
    df=df.set_index('Phone_Number')

    df.loc[data['Phone_Number']]=[data['Email'],
                                        data['Comment'],
                                        data['Category']]
        
    df.to_sql('dispute', dbConnection, if_exists='append')
    print(df)
    

    dbConnection.close()
    
