from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

config = {
  "apiKey": "AIzaSyBgQD6aYXng_d47Sj56kTV-yF9h6ExG2p4",
  "authDomain": "clils-project.firebaseapp.com",
  "projectId": "clils-project",
  "storageBucket": "clils-project.appspot.com",
  "messagingSenderId": "147852976889",
  "appId": "1:147852976889:web:d1a3fe7e7f8b69edbd3828",
  "measurementId": "G-YRBZZPR6QJ",
  "databaseURL":"https://clils-project-default-rtdb.firebaseio.com/"
};
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


@app.route('/', methods=['GET', 'POST'])
def signin():
    error=""
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email,password)
            print(login_session['user'])
            return redirect (url_for('add_tweet'))
        except:
            error="Authentication failed"
    return render_template("signin.html") 
    



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error=""
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        try:
            login_session['email']=email
            login_session['password']=sign_in_with_email_and_password
            login_session['user'] = auth.create_user_with_email_and_password(email,password)
            user = {"name": request.form['fullname'],"username":request.form['username'],"bio":request.form['bio']}
            UID = login_session['user']['localId']
            db.child("Users").child(UID).set(user)
            return redirect (url_for('add_tweet'))
        except:
            error="Authentication failed"
    return render_template("signup.html")



@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method=="POST":
        try:
            UID = login_session['user']['localId']
            tweets={"title":request.form['title'], "tweet":request.form['tweet'],"uid":UID}
            db.child("Tweets").push(tweet)
            return redirect(url_for('all_tweets'))
        except:
            return render_template("add_tweet.html")
    return render_template("add_tweet.html")

@app.route('/all_tweets')
def all_tweets():
    tweets=db.child("Tweets").get().val()
    return render_template("tweets.html",tweets=tweets)



if __name__ == '__main__':
    app.run(debug=True)