from flask import Flask,render_template,request,flash,session,redirect,url_for,jsonify
from datetime import datetime,timedelta
import mysql.connector
import os
jxdb=mysql.connector.connect(host="localhost",user="root",password="",db="jxdb")


app=Flask(__name__)

app.secret_key="user"
app.config['UPLOAD_FOLDER'] = 'D:\\bike booster\\static\\img'


@app.route("/")
def hello():
  
  date=datetime.now()
  cur=jxdb.cursor()
  
  cur.execute("UPDATE `product` SET `Expiry`='invaild' WHERE Expiry_date=%s",(date.date(),))  
  jxdb.commit()


  cur.execute("SELECT product.id,product.name,product.img,product.price,user.Address FROM product INNER JOIN user on product.seller_name=user.name where Expiry='invaild' ORDER BY `product`.`id` DESC LIMIT 6")
  db1=cur.fetchall()

  cur.close()
  return render_template("home.html",data=db1,id=session.get('name'))


@app.route("/about")
def about():
   return render_template("about.html",id=session.get('name'))


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    cur=jxdb.cursor()
    cur.execute(" SELECT name  FROM product WHERE name LIKE %s LIMIT 10", (f"%{query}%",))
    suggestions=cur.fetchall()
    cur.close() 
    return jsonify(suggestions)

@app.route("/searchbar",methods=["POST"])
def ser():
    query=request.form.get("jk")
    print(query)
    cur=jxdb.cursor()
    cur.execute(" SELECT * FROM product WHERE name=%s", (query,))
    suggestions=cur.fetchall()
    print(suggestions)
    cur.close()
    return render_template("showproduct.html",show=suggestions)


@app.route("/login")
def login():
   return render_template("login.html")

@app.route("/sign-up")
def sign():
   return render_template("register.html")

@app.route("/logout")
def logout():
  session.clear()
  return redirect(url_for('hello'))



@app.route("/sign-up1",methods=["POST"])
def sign1():
  name=request.form.get("f1")
  email=request.form.get("f2")
  password=request.form.get("f3")
  cpassword=request.form.get("f4")
  phone=request.form.get("f5")
  address=request.form.get("f6")
  

   
  if name==None or email==None or password==None or cpassword==None or phone==None or address==None:
      return redirect(url_for('sign'))
  cur=jxdb.cursor()
  cur.execute("INSERT INTO `user`(`name`, `password`, `email`, `phone`, `Address`) VALUES (%s,%s,%s,%s,%s)",(name,password,email,phone,address))
  jxdb.commit()
  cur.close()
  flash("registion scusessfully")  
  return render_template("login.html")


@app.route("/login-user",methods=["POST"])
def login1():
      f1=request.form.get("h1")
      f2=request.form.get("h2")
      session["name"]=f1
      
      cur = jxdb.cursor()
        
        # Execute the query
      cur.execute("SELECT * FROM user WHERE name=%s AND password=%s", (f1, f2))
        
        # Fetch one result
      result = cur.fetchone()
        
      if result:  # If a matching record is found
            return redirect(url_for('hello'))
      else:
            return redirect(url_for('login'))
      

@app.route("/sell1")
def sell1():
    return render_template("sell.html")
          

@app.route("/sell")
def sell():
      d1=session.get('name')
      if d1==None:
          return redirect(url_for('login'))
      return redirect(url_for('sell1'))






 
@app.route("/product",methods=["POST"])
def product():
    f1=request.files['picture']
    f11=f1.filename
    f2=request.form.get("name")
    f3=request.form.get("price")
    f4=request.form.get("product")
    f5=session["name"]
    f6=request.form.get("jk")
    date1=datetime.now()+timedelta(days=4)
    print(date1)
    f7=request.form.get('jk1')
    print(f1.filename,f2,f3,f4,f5,f6)
    f1.save(os.path.join(app.config['UPLOAD_FOLDER'],f1.filename))
    cur=jxdb.cursor()
    cur.execute("INSERT INTO `product`(`name`,`img`,`price`, `info`, `seller_name`, `type`,`sub_type`,`Expiry_date`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(f2,f11,f3,f4,f5,f6,f7,date1))
    jxdb.commit()
    cur.close()
    return redirect(url_for('hello'))


## bike part
@app.route("/bike")
def bike():
    cur=jxdb.cursor()
    d1=session.get('name')
    if d1==None:
        cur.execute("SELECT product.id,product.name,product.img,product.price,user.Address FROM product INNER JOIN user ON product.seller_name = user.name  where product.Expiry='valid' AND product.type='BikePart'")
        db=cur.fetchall()
      
        cur.close()
        return render_template("bikepart.html",data=db)
    else:
        cur.execute("SELECT product.id,product.name,product.img,product.price,user.Address FROM product INNER JOIN user ON product.seller_name = user.name  where product.Expiry='valid' AND product.type='BikePart' AND product.seller_name!=%s  ORDER BY `product`.`id`",(d1,))
        db=cur.fetchall()
        cur.close()
        return render_template("bikepart.html",data=db,id=db)

@app.route("/Accessories")
def Accessories():
    cur=jxdb.cursor()
    cur.execute("SELECT * FROM `product` WHERE type='Accessories'")
    db=cur.fetchall()
    cur.close()
    return render_template("bikeaccessories.html",data1=db)

@app.route("/sellproduct")
def sellproduct():
    d1=session.get('name')
    print(d1)
    if d1==None:
      return redirect(url_for('login'))
    else:
      cur=jxdb.cursor()
      date=datetime.now()
      a=date.date()
      #if date.date()
      
      cur.execute("SELECT * FROM `product` WHERE seller_name=%s ORDER BY id DESC",(d1,))
      db=cur.fetchall()
      cur.close()
      return render_template("sellproduct.html",data=db)
#see product
@app.route('/show/<i1>',methods=['GET'])
def show(i1):
    cur=jxdb.cursor()
    cur.execute("SELECT * FROM `product` WHERE id=%s",(i1,))
    db=cur.fetchall()

    cur.execute(
        "SELECT user.phone FROM `product` INNER JOIN user on product.seller_name=user.name WHERE product.id=%s",
        (i1,)
    )
    db1 = cur.fetchone()
    phone=db1[0]
    mess="Hello,I am intersted your product" 
    cur.close()
    return render_template('showproduct.html',show=db,ph=phone,b=mess,id=session.get('name'))





if __name__=="__main__":
    app.run(debug=True)
