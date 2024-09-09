from flask import Blueprint,render_template,request,redirect,session
import datetime
import mysql.connector
import uuid
con=mysql.connector.connect(host="localhost",user="root",password="",database="shopmanagement",consume_results=True)
cur=con.cursor()
customer=Blueprint('customer',__name__)
products = []
global total_count

@customer.route('/Cus_signup',methods=['POST','GET'])
def Cus_signup():
    if request.method=='POST':
        cusid = uuid.uuid1()
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmpassword = request.form.get("confirmpassword")
        if password != confirmpassword:
            msg = "password is incorrect"
            return render_template('cus_signup.html', msg=msg)
        sql = f"insert into cus_signup(cusid,username,email,password,confirmpassword)values('{cusid}','{username}','{email}','{password}','{confirmpassword}')"
        cur.execute(sql)
        con.commit()
        return redirect('/home')
    return render_template('cus_signup.html')

@customer.route('/Cus_signin',methods=['POST','GET'])
def Cus_signin():
    if request.method=="POST":
        email=request.form.get("emailid")
        password=request.form.get("password")
        sql=f"select * from cus_signup where email='{email}' and password='{password}'"
        cur.execute(sql)
        res=cur.fetchall()
        if res!=[]:
            pass
    return render_template('cus_signin.html')

@customer.route('/Customer',methods=['POST','GET'])
def Add_customer():
    if request.method == "POST":
        name = request.form.get("name")
        place = request.form.get("place")
        phonenumber = request.form.get("phonenumber")

        sql = f"insert into customers(customername,place,phonenumber)values('{name}','{place}','{phonenumber}')"
        cur.execute(sql)
        con.commit()
    return render_template('Add_cus.html')

@customer.route('/Customerdetails')
def Cus_details():
    sql = "select * from customers"
    cur.execute(sql)
    data = cur.fetchall()
    return render_template('Cus_details.html', data=data)


@customer.route('/home', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        Cus_no = request.form.get("customernumber")
        sql=f"select * from customers where phonenumber='{Cus_no}'"
        cur.execute(sql)
        numbers=cur.fetchall()
        if numbers!=[]:
            session["customer_number"]=Cus_no
            session["billno"]=uuid.uuid1()
            return redirect("/product")
        else:
            return redirect('/Cus_signup')


    return render_template('home.html')

@customer.route('/Delete/<id>')
def delete(id):
    sql=f"delete from customers where id='{id}'"
    cur.execute(sql)
    con.commit()
    return redirect('/Customerdetails')

@customer.route('/Edit/<id>',methods=['POST','GET'])
def edit(id):
    sql=f"select * from customers where id='{id}'"
    cur.execute(sql)
    Data=cur.fetchall()
    if request.method=="POST":
        customername=request.form.get("customername")
        place=request.form.get("place")
        phonenumber=request.form.get("phonenumber")
        sql=f"update customers set customername='{customername}',place='{place}',phonenumber='{phonenumber}' where id='{id}'"
        cur.execute(sql)
        con.commit()
        return redirect('/Customerdetails')
    return render_template('update_customer.html',Data=Data)


@customer.route('/product',methods=['POST','GET'])
def product_buy():
    global name
    sum=()
    bill_no = session.get("billno", None)
    customer_no = session.get("customer_number", None)
    date = datetime.date.today()
    sql = f"select * from daily_purchased_products where bill_no='{bill_no}' and date='{date}' and customer_no={customer_no}"
    cur.execute(sql)
    result = cur.fetchall()
    print(result, "//")
    if request.method=="POST":
        date = datetime.date.today()
        print(date)
        mnth=date.strftime("%B")
        print(customer_no)
        product_name=request.form.get("productname")
        qty=request.form.get("quantity")
        sql=f"select * from stocks where name='{product_name}'"
        cur.execute(sql)
        name=cur.fetchall()
        # print(name)
        # print(bill_no,date,customer_no,product_name,qty,int(name[0][3])*int(qty))
        sql=f"select * from daily_purchased_products where bill_no='{bill_no}'and date='{date}'and product_name='{product_name}'"
        cur.execute(sql)
        res_price=cur.fetchall()
        print(res_price,"//")

        # sum=0
        # for i in range(len(res_price)):
        #     sum+=res_price[i][6]
        # print(sum)
        # price=(int(qty)+res_price[0][5])*int(name[0][3])
        # print(res_price,"//")
        sum = 0
        if res_price!=[]:

            # for i in range(len(res_price)):
            #     sum += res_price[i][6]
            # print(sum)
            price = (int(qty) + res_price[0][5]) * int(name[0][3])
            # print(res_price, "//")
            sql = f"update daily_purchased_products set product_qty=product_qty+'{qty}',total_price='{price}' where product_name='{product_name}' and bill_no='{bill_no}' and customer_no='{customer_no}'and date='{date}'"
            cur.execute(sql)
            con.commit()
            sql=f"update stocks set quantity=quantity-'{qty}' where name='{product_name}'"
            cur.execute(sql)
            con.commit()
        else:
            sql = f"update stocks set quantity=quantity-'{qty}' where name='{product_name}'"
            cur.execute(sql)
            con.commit()
            sql = f"insert into daily_purchased_products(bill_no,date,customer_no,product_name,product_qty,total_price)values('{bill_no}','{date}','{customer_no}','{product_name}','{qty}','{int(name[0][3]) * int(qty)}')"
            cur.execute(sql)
            con.commit()
        sql=f"insert into customer_products(customer_no,month,date,product_name)values('{customer_no}','{mnth}','{date}','{product_name}')"
        cur.execute(sql)
        con.commit()
        sql=f"select product_name from customer_products where month='{mnth}' and date='{date}'"
        cur.execute(sql)
        buyed_details=cur.fetchall()
        print(buyed_details,"//")
        sql=f"select product_name from customer_products where product_name='{product_name}' and date='{date}'"
        cur.execute(sql)
        count=cur.fetchall()
        total_count=(len(count))




        return  redirect("/product")

    return render_template('purchased_products.html',result=result,sum=sum)


@customer.route("/")
def homepage():
    date = datetime.date.today()
    sql = "select name,quantity from stocks where quantity<5"
    cur.execute(sql)
    details = cur.fetchall()
    print(details, "//")
    sql = f"select date from customer_products where date='{date}'"
    cur.execute(sql)
    count = cur.fetchall()
    total_count = (len(count))

    return render_template('homepage.html', details=details,total_count=total_count)
