from flask import Blueprint, render_template,request,redirect
import mysql.connector
import uuid
con=mysql.connector.connect(host="localhost",user="root",password="",database="shopmanagement")
cur=con.cursor()
shop = Blueprint('shop', __name__)



@shop.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=="POST":
        shopid=uuid.uuid1()
        username=request.form.get("username")
        email=request.form.get("email")
        password=request.form.get("password")
        confirmpassword=request.form.get("confirmpassword")
        if password!=confirmpassword:
            msg="password is incorrect"
            return render_template('signup.html',msg=msg)
        sql=f"insert into shop_signup(shopid,username,email,password,confirmpassword)values('{shopid}','{username}','{email}','{password}','{confirmpassword}')"
        cur.execute(sql)
        con.commit()
        return redirect("login")

    return render_template('signup.html')

@shop.route('/login',methods=['POST','GET'])
def login():
    if request.method=="POST":
        email=request.form.get("emailid")
        password=request.form.get("password")
        sql=f"select * from shop_signup where email='{email}' and password='{password}'"
        cur.execute(sql)
        res=cur.fetchall()
        if res!=[]:
            return redirect('/stocks')
    return render_template('login.html')

@shop.route('/stocks',methods=['POST','GET'])
def Add_stocks():
    if request.method=="POST":
        name=request.form.get("name")
        quantity=request.form.get("quantity")
        price=request.form.get("price")
        sql=f"insert into stocks(name,quantity,price)values('{name}','{quantity}','{price}')"
        cur.execute(sql)
        con.commit()
    return render_template('Add_stock.html')

@shop.route('/stockdetails')
def stock_details():
    sql="select * from stocks"
    cur.execute(sql)
    data=cur.fetchall()
    return render_template('stock_details.html',data=data)

@shop.route('/delete/<id>')
def delete(id):

    sql=f"delete from stocks where id='{id}'"
    cur.execute(sql)
    con.commit()
    return redirect('/stockdetails')

@shop.route('/edit/<id>',methods=['POST','GET'])
def edit(id):
    sql=f"select * from stocks where id='{id}'"
    cur.execute(sql)
    Data=cur.fetchall()
    print(Data)
    if request.method=="POST":
        name=request.form.get("name")
        quantity=request.form.get("quantity")
        price=request.form.get("price")
        sql=f"update stocks set name='{name}',quantity='{quantity}',price='{price}' where id='{id}'"
        cur.execute(sql)
        con.commit()
        return redirect('/stockdetails')
    return render_template('update_stocks.html',Data=Data)



@shop.route("/productdetails")
def product_details():
    sql="select * from customer_products"
    cur.execute(sql)
    products=cur.fetchall()

    return render_template("product_details.html",products=products)