<<<<<<< HEAD
from flask import Flask,render_template,request,redirect,session
from ai import analyze_resume
from db import Base, engine, SessionLocal
import db
import model
import PyPDF2
import docx
import json

app = Flask(__name__)
app.secret_key = "shivam123"

Base.metadata.create_all(bind=engine)

#home
@app.route('/')
def home():
    if "user" in session:
         return redirect("/dashbord")
    return redirect("/login")

#singup

@app.route("/singup", mrthods=["GET","POST"])
def singup():
     db=SessionLocal()

     if request.method == "POST":
          email = request.form.get("email")
          password= request.form.get("password")

          existing_user = db.query(model.user).filter_by(email=email).first()
          if existing_user:
            return "User already exists"
          
          user = model.user(email=email, password=password)
          db.add(user)
          db.commit()

          return redirect("/login")
     return render_template("/singup.html")

#login

@app.route("/login",methods=["GET","POST"])
def login():
    db = SessionLocal()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user=db.query(model.user).filter_by(email=email,password=password).first()

        if user:
            session["user"]=user.email
            return redirect("/dashbord")
        else:
            return "invalid credentials"
        
    return render_template("/login.html")

#dashbord

@app.route("/dashbord",methods=["GET","POST"])
def dashboed():
    if "user" not in session:
        return redirect("/login")
    
    result = None

    if request.method == "POST ":
        user_gole = request.form.get("role")
        resume_text = request.form.get("resume")

        file = request.files.get("file")
   
        if file and file.name != "":
            if file.filename.endswith(".pdf"):
                try:
                    pdf_reader= PyPDF2.PdfReader(file)
                    text = ""
                    for page in pdf_reader.pages:
                     text += page.extract_text() or ""
                     resume_text = text
                except Exception as e:
                 result = f"Error processing PDF: {str(e)}"

        elif file.filename.endswith(".docx"):
                try:
                    doc=docx.document(file)
                    text=""
                    for para in doc.paragraphs:
                        text += para.text + "\n"
                    resume_text = text
                except Exception as e:
                    result = f"Error processing DOCX: {str(e)}"
                    

        if resume_text and user_gole: 
            try:
               result = analyze_resume(resume_text , user_gole)

               #save to db
               db = SessionLocal()
               user = db.query(model.user).filter_by(email=session["user"]).first()

               report = model.Report(
                   user_id = user.id,
                   resume_text = resume_text,
                   result = json.dumps(result)
                   
               )
               db.add(report)
               db.commit()

            except Exception as e:
                result = {"error": f"AI error : {str(e)}"}

                return render_template(
                    "dashbord.html",
                    usser=session["user"],
                    result=result
                )
            
@app.route("/history")
def history():
    if "user" not in session:
        return redirect("/login")
    
    db= SessionLocal()
    user = db.query(model.user).filter_by(email=session["user"]).first()

    reports = db.query(model.Report).filter_by(user_id=user.id).all()



    #convert json string> dict
    pasred_reports = []
    for r in reports:
        try:
            pasred_result = json.loads(r.result)
        except:
            pasred_result = []

            pasred_reports.append({
                "resume_text":r.resume_text,
                "result":pasred_result
            })


        return render_template("history.html",reports=pasred_reports)
        

#logout
@app.route("/logout")
def Logout():
    session.pop("user",None)
    return redirect("/login")
     

        
if __name__ == '__main__':
=======
from flask import Flask,render_template,request,redirect,session
from ai import analyze_resume
from db import Base, engine, SessionLocal
import db
import model
import PyPDF2
import docx
import json

app = Flask(__name__)
app.secret_key = "shivam123"

Base.metadata.create_all(bind=engine)

#home
@app.route('/')
def home():
    if "user" in session:
         return redirect("/dashbord")
    return redirect("/login")

#singup

@app.route("/singup", mrthods=["GET","POST"])
def singup():
     db=SessionLocal()

     if request.method == "POST":
          email = request.form.get("email")
          password= request.form.get("password")

          existing_user = db.query(model.user).filter_by(email=email).first()
          if existing_user:
            return "User already exists"
          
          user = model.user(email=email, password=password)
          db.add(user)
          db.commit()

          return redirect("/login")
     return render_template("/singup.html")

#login

@app.route("/login",methods=["GET","POST"])
def login():
    db = SessionLocal()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user=db.query(model.user).filter_by(email=email,password=password).first()

        if user:
            session["user"]=user.email
            return redirect("/dashbord")
        else:
            return "invalid credentials"
        
    return render_template("/login.html")

#dashbord

@app.route("/dashbord",methods=["GET","POST"])
def dashboed():
    if "user" not in session:
        return redirect("/login")
    
    result = None

    if request.method == "POST ":
        user_gole = request.form.get("role")
        resume_text = request.form.get("resume")

        file = request.files.get("file")
   
        if file and file.name != "":
            if file.filename.endswith(".pdf"):
                try:
                    pdf_reader= PyPDF2.PdfReader(file)
                    text = ""
                    for page in pdf_reader.pages:
                     text += page.extract_text() or ""
                     resume_text = text
                except Exception as e:
                 result = f"Error processing PDF: {str(e)}"

        elif file.filename.endswith(".docx"):
                try:
                    doc=docx.document(file)
                    text=""
                    for para in doc.paragraphs:
                        text += para.text + "\n"
                    resume_text = text
                except Exception as e:
                    result = f"Error processing DOCX: {str(e)}"
                    

        if resume_text and user_gole: 
            try:
               result = analyze_resume(resume_text , user_gole)

               #save to db
               db = SessionLocal()
               user = db.query(model.user).filter_by(email=session["user"]).first()

               report = model.Report(
                   user_id = user.id,
                   resume_text = resume_text,
                   result = json.dumps(result)
                   
               )
               db.add(report)
               db.commit()

            except Exception as e:
                result = {"error": f"AI error : {str(e)}"}

                return render_template(
                    "dashbord.html",
                    usser=session["user"],
                    result=result
                )
            
@app.route("/history")
def history():
    if "user" not in session:
        return redirect("/login")
    
    db= SessionLocal()
    user = db.query(model.user).filter_by(email=session["user"]).first()

    reports = db.query(model.Report).filter_by(user_id=user.id).all()



    #convert json string> dict
    pasred_reports = []
    for r in reports:
        try:
            pasred_result = json.loads(r.result)
        except:
            pasred_result = []

            pasred_reports.append({
                "resume_text":r.resume_text,
                "result":pasred_result
            })


        return render_template("history.html",reports=pasred_reports)
        

#logout
@app.route("/logout")
def Logout():
    session.pop("user",None)
    return redirect("/login")
     

        
if __name__ == '__main__':
>>>>>>> be4b09ac4c3691a4af7015eaf7271467c8118e10
     app.run(debug=True)