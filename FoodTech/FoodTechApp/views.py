from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
import pymysql
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
from datetime import date
from Blockchain import *
from Block import *
import pyqrcode
import png
from pyqrcode import QRCode

global uname, address, phone
global deliver_address, deliver_time

blockchain = Blockchain()
if os.path.exists('blockchain_contract.txt'):
    with open('blockchain_contract.txt', 'rb') as fileinput:
        blockchain = pickle.load(fileinput)
    fileinput.close()

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def AddFood(request):
    if request.method == 'GET':
       return render(request, 'AddFood.html', {})    

def BrowseProducts(request):
    if request.method == 'GET':
        output = '<tr><td><font size="" color="black">Food&nbsp;Name</font></td><td><select name="t1">'
        for i in range(len(blockchain.chain)):
            if i > 0:
                b = blockchain.chain[i]
                data = b.transactions[0]
                data = base64.b64decode(data)
                decrypt = blockchain.decrypt(data)
                decrypt = decrypt.decode("utf-8")
                arr = decrypt.split("#")
                if arr[0] == 'addproduct':
                    output+='<option value='+arr[1]+'>'+arr[1]+'</option>'
        output+="</select></td></tr>"
        context= {'data1':output}
        return render(request, 'BrowseProducts.html', context)

def Login(request):
    if request.method == 'GET':
       return render(request, 'Login.html', {})

def Admin(request):
    if request.method == 'GET':
       return render(request, 'Admin.html', {})
    
    
def ViewOrders(request):
    if request.method == 'GET':
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Food Name</font></th>'
        output+='<th><font size=3 color=black>Customer Name</font></th>'
        output+='<th><font size=3 color=black>Contact No</font></th>'
        output+='<th><font size=3 color=black>Email ID</font></th>'
        output+='<th><font size=3 color=black>Address</font></th>'
        output+='<th><font size=3 color=black>Ordered Date</font></th></tr>'
        for i in range(len(blockchain.chain)):
            if i > 0:
                b = blockchain.chain[i]
                data = b.transactions[0]
                data = base64.b64decode(data)
                decrypt = blockchain.decrypt(data)
                decrypt = decrypt.decode("utf-8")
                arr = decrypt.split("#")
                if arr[0] == 'bookorder':
                    details = arr[3].split(",")
                    pid = arr[1]
                    user = arr[2]
                    book_date = arr[4]
                    output+='<tr><td><font size=3 color=black>'+pid+'</font></td>'
                    output+='<td><font size=3 color=black>'+user+'</font></td>'
                    output+='<td><font size=3 color=black>'+details[0]+'</font></td>'
                    output+='<td><font size=3 color=black>'+details[1]+'</font></td>'
                    output+='<td><font size=3 color=black>'+details[2]+'</font></td>'
                    output+='<td><font size=3 color=black>'+str(book_date)+'</font></td></tr>'
        output+="</table><br/><br/><br/><br/><br/><br/>"
        context= {'data':output}
        return render(request, 'ViewOrders.html', context)     

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})

def AddFood(request):
    if request.method == 'GET':
       return render(request, 'AddFood.html', {})

def BookOrder(request):
    if request.method == 'GET':
        global deliver_address, deliver_time, phone
        pid = request.GET['crop']
        user = ''
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip('\n')
        file.close()
        details = ''
        for i in range(len(blockchain.chain)):
            if i > 0:
                b = blockchain.chain[i]
                data = b.transactions[0]
                data = base64.b64decode(data)
                decrypt = blockchain.decrypt(data)
                decrypt = decrypt.decode("utf-8")
                arr = decrypt.split("#")
                if arr[0] == "signup":
                    if arr[1] == user:
                        details = arr[3]+","+arr[4]+","+arr[5]
                        break
        today = date.today()            
        data = "bookorder#"+pid+"#"+user+"#"+details+"#"+str(today)+deliver_address+"#"+deliver_time+"#"+phone
        enc = blockchain.encrypt(str(data))
        enc = str(base64.b64encode(enc),'utf-8')
        blockchain.add_new_transaction(enc)
        hash = blockchain.mine()
        b = blockchain.chain[len(blockchain.chain)-1]
        blockchain.save_object(blockchain,'blockchain_contract.txt')
        print("Previous Hash : "+str(b.previous_hash)+" Block No : "+str(b.index)+" Current Hash : "+str(b.hash))
        bc = "Previous Hash : "+str(b.previous_hash)+"<br/>Block No : "+str(b.index)+"<br/>Current Hash : "+str(b.hash)
        output = 'Your Order details Updated<br/>'+bc
        context= {'data':output}
        return render(request, 'UserScreen.html', context)      

def SearchProductAction(request):
    if request.method == 'POST':
        ptype = request.POST.get('t1', False)
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Food Name</font></th>'
        output+='<th><font size=3 color=black>Batch No</font></th>'
        output+='<th><font size=3 color=black>Farm Origin Data</font></th>'
        output+='<th><font size=3 color=black>Expiry Date</font></th>'
        output+='<th><font size=3 color=black>Storage Conditions</font></th>'
        output+='<th><font size=3 color=black>Shipping Details</font></th>'
        output+='<th><font size=3 color=black>Price</font></th>'
        output+='<th><font size=3 color=black>Food Image</font></th>'
        output+='<th><font size=3 color=black>QR Code</font></th>'
        output+='<th><font size=3 color=black>Book Food</font></th></tr>'
        for i in range(len(blockchain.chain)):
            if i > 0:
                b = blockchain.chain[i]
                data = b.transactions[0]
                data = base64.b64decode(data)
                decrypt = blockchain.decrypt(data)
                decrypt = decrypt.decode("utf-8")
                arr = decrypt.split("#")
                if arr[0] == 'addproduct':
                    if arr[1] == ptype:
                        output+='<tr><td><font size=3 color=black>'+arr[1]+'</font></td>'
                        output+='<td><font size=3 color=black>'+arr[2]+'</font></td>'
                        output+='<td><font size=3 color=black>'+str(arr[3])+'</font></td>'
                        output+='<td><font size=3 color=black>'+str(arr[4])+'</font></td>'
                        output+='<td><font size=3 color=black>'+arr[5]+'</font></td>'
                        output+='<td><font size=3 color=black>'+arr[6]+'</font></td>'
                        output+='<td><font size=3 color=black>'+arr[7]+'</font></td>'
                        output+='<td><img src=/static/products/'+arr[8]+' width=200 height=200></img></td>'
                        output+='<td><img src=/static/products/qr_'+arr[2]+'.png width=200 height=200></img></td>'
                        output+='<td><a href=\'BookOrder?crop='+arr[1]+'\'><font size=3 color=black>Click Here</font></a></td></tr>'
        output+="</table><br/><br/><br/><br/><br/><br/>"
        context= {'data':output}
        return render(request, 'SearchProducts.html', context)              
        
    
def Deliver(request):
    if request.method == 'POST':
        global deliver_address, deliver_time
        deliver_address = request.POST.get('t1', False)
        deliver_time = request.POST.get('t2', False)
        context= {'data':'Please login to continue'}
        return render(request, 'Login.html', context)

def AddFoodAction(request):
    if request.method == 'POST':
        fname = request.POST.get('t1', False)
        batch = request.POST.get('t2', False)
        farm = request.POST.get('t3', False)
        expiry = request.POST.get('t4', False)
        storage = request.POST.get('t5', False)
        shipping = request.POST.get('t6', False)
        price = request.POST.get('t7', False)
        image = request.FILES['t8']
        imagename = request.FILES['t8'].name
        data = "addproduct#"+fname+"#"+batch+"#"+farm+"#"+expiry+"#"+storage+"#"+shipping+"#"+price+"#"+imagename+"#qr_"+batch+".png"
        qr = fname+","+batch+","+farm+","+expiry+","+storage+","+shipping+","+price
        enc = blockchain.encrypt(str(data))
        enc = str(base64.b64encode(enc),'utf-8')
        blockchain.add_new_transaction(enc)
        hash = blockchain.mine()
        b = blockchain.chain[len(blockchain.chain)-1]
        print("Encrypted Data : "+str(b.transactions[0])+" Previous Hash : "+str(b.previous_hash)+" Block No : "+str(b.index)+" Current Hash : "+str(b.hash))
        bc = "Encrypted Data : "+str(b.transactions[0])+" Previous Hash : "+str(b.previous_hash)+"<br/>Block No : "+str(b.index)+"<br/>Current Hash : "+str(b.hash)
        blockchain.save_object(blockchain,'blockchain_contract.txt')
        fs = FileSystemStorage()
        filename = fs.save('FoodTechApp/static/products/'+imagename, image)
        qr_url = pyqrcode.create(qr)
        qr_url.png('FoodTechApp/static/products/qr_'+batch+".png", scale = 6)
        context= {'data':'Food details added.<br/>'+bc}
        return render(request, 'AddFood.html', context)
        
   
def Signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        contact = request.POST.get('contact', False)
        email = request.POST.get('email', False)
        address = request.POST.get('address', False)        
        record = 'none'
        for i in range(len(blockchain.chain)):
            if i > 0:
                b = blockchain.chain[i]
                data = b.transactions[0]
                data = base64.b64decode(data)
                decrypt = blockchain.decrypt(data)
                decrypt = decrypt.decode("utf-8")
                arr = decrypt.split("#")
                if arr[0] == "signup":
                    if arr[1] == username:
                        record = "exists"
                        break
        if record == 'none':
            data = "signup#"+username+"#"+password+"#"+contact+"#"+email+"#"+address
            enc = blockchain.encrypt(str(data))
            enc = str(base64.b64encode(enc),'utf-8')
            blockchain.add_new_transaction(enc)
            hash = blockchain.mine()
            b = blockchain.chain[len(blockchain.chain)-1]
            print("Encrypted Data : "+str(b.transactions[0])+" Previous Hash : "+str(b.previous_hash)+" Block No : "+str(b.index)+" Current Hash : "+str(b.hash))
            bc = "Encrypted Data : "+str(b.transactions[0])+" Previous Hash : "+str(b.previous_hash)+"<br/>Block No : "+str(b.index)+"<br/>Current Hash : "+str(b.hash)
            blockchain.save_object(blockchain,'blockchain_contract.txt')
            context= {'data':'Signup process completd and record saved in Blockchain with below hashcodes.<br/>'+bc}
            return render(request, 'Register.html', context)
        else:
            context= {'data':username+'Username already exists'}
            return render(request, 'Register.html', context)    


def AdminLogin(request):
    global uname, address, phone
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        if username == 'admin' and password == 'admin':
            context= {'data':"Welcome "+username}
            return render(request, 'AdminScreen.html', context)        
        else:
            context= {'data':'Invalid login details'}
            return render(request, 'Admin.html', context)   
            
        
def UserLogin(request):
    global uname, address, phone
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)        
        status = 'none'
        for i in range(len(blockchain.chain)):
            if i > 0:
                b = blockchain.chain[i]
                data = b.transactions[0]
                data = base64.b64decode(data)
                decrypt = blockchain.decrypt(data)
                decrypt = decrypt.decode("utf-8")
                arr = decrypt.split("#")
                if arr[0] == "signup":
                    if arr[1] == username and arr[2] == password:
                        status = 'success'
                        uname = username
                        address = arr[5]
                        phone = arr[3]
                        break
        if status == 'success':
            file = open('session.txt','w')
            file.write(username)
            file.close()
            context= {'data':"Welcome "+username}
            return render(request, 'UserScreen.html', context)        
        else:
            context= {'data':'Invalid login details'}
            return render(request, 'Login.html', context)            


        
        



        
            
