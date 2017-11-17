from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
from django.db import connection, IntegrityError, transaction
from datetime import datetime, date
import re

def home(request):
	return render(request, 'home.html')

def register(request):
	return render(request, 'register.html')

def register_user(request):
#	collect the form input
	fname=request.POST['fname']
	lname=request.POST['lname']
	gender=request.POST['gender']
	email=request.POST['email']
	add1=request.POST['add1']
	add2=request.POST['add2']
	city=request.POST['city']
	contact=request.POST['contact']
	username=request.POST['username']
	pwd=request.POST['pwd']
	pwd2=request.POST['pwd2']

	email_ok = re.search(r'[\w.-]+@[\w-]+\.[\w.-]+', email)
	contact_ok = 1
	if len(contact)!=11:
		contact_ok=0
	for char in contact:
		if(ord(char)<48 or ord(char)>57):
			contact_ok=0
			break
	cursor = connection.cursor()
	cursor.execute("select * from customer where username='"+username+"';")
	res=cursor.fetchone()
	connection.close()

	if not contact_ok:
		messages.error(request, 'Invalid contact number.')
		return render(request, 'register.html')
	elif not email_ok:
		messages.error(request, 'Invalid e-mail address.')
		return render(request, 'register.html')
	elif res is not None:
		messages.error(request, 'This username is taken.')
		return render(request, 'register.html')
	elif pwd != pwd2:
		messages.error(request, 'Passwords do not match.')
		return render(request, 'register.html')
	else:
		cursor = connection.cursor()
		try:
			print	"YOYOYOYOYO"
			cursor.execute("insert into customer(username, fname, lname, gender, add1, add2, city, email, contact) values('"+username+"','"+fname+"','"+lname+"','"+gender+"','"+add1+"','"+add2+"','"+city+"','"+email+"','"+contact+"');")
			connection.commit()
			user=User.objects.create_user(username, None, pwd)
			messages.success(request, 'Registration successful.')
			return render(request, 'home.html')
		except Exception as e:
			print e
			connection.rollback()
		connection.close()
		return HttpResponseRedirect(reverse('home'))

def login(request):
	if request.POST:
		username = request.POST['username']
		pwd = request.POST['pwd']

		cursor = connection.cursor()
		cursor.execute("select * from auth_user where username='"+username+"';")
		data=cursor.fetchone()
		connection.close()
		if data is not None:
			username=data[4]
			user=auth.authenticate(username=username, password=pwd)
			if user is not None:
				auth.login(request,user)
				return HttpResponseRedirect(reverse('home'))
			else:
				messages.error(request, 'Incorrect username and/or password.')
				return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
		messages.error(request, 'This username does not exist.')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	return render(request, "home.html")

def logout(request):
	# cursor=connection.cursor()
	# cursor.execute("select ret_rec_id from retail_record where username='"+request.user.username+"' and status=1;")
	# olist=list(cursor.fetchall())
	# for i in range(len(olist)):
	# 	x=olist[i][0]
	# 	cursor.execute("delete from retail_record where ret_rec_id="+str(x)+";")
	# 	connection.commit()

	auth.logout(request)
	messages.success(request, 'Successfully logged out.')
	return HttpResponseRedirect(reverse('home'))

def feedback(request):
	content=request.POST['fb']
	username=request.user.username
	cursor = connection.cursor()
	cursor.execute("insert into feedback(content,username) values('"+content+"','"+username+"');")
	connection.commit()
	messages.success(request, 'Feedback submitted.')
	return	HttpResponseRedirect(reverse('home'))
	connection.close()
	return	HttpResponseRedirect(reverse('home'))

def edit(request):
	cursor=connection.cursor()
	cursor.execute("select * from customer where username='"+request.user.username+"';")
	res = cursor.fetchall()
	print "YOYOYOYOYOYOYOYO",len(res)
	profile=list(list(res)[0])
	return render(request, 'edit.html', {'profile': profile})

def profile(request):
	if not request.user.is_superuser:
		cursor=connection.cursor()
		cursor.execute("select * from customer where username='"+request.user.username+"';")
		res = cursor.fetchall()
		profile=list(list(res)[0])
		return render(request, 'profile.html', {'profile': profile})
	else:
		return render(request, 'profile.html')

def contact(request):
	return render(request, 'contact.html')

def edit_profile(request):
#	collect the form input
	fname=request.POST['fname']
	lname=request.POST['lname']
	gender=request.POST['gender']
	email=request.POST['email']
	add1=request.POST['add1']
	add2=request.POST['add2']
	city=request.POST['city']
	contact=request.POST['contact']
	username=request.POST['username']

	email_ok = re.search(r'[\w.-]+@[\w-]+\.[\w.-]+', email)
	contact_ok = 1
	if len(contact)!=11:
		contact_ok=0
	for char in contact:
		if(ord(char)<48 or ord(char)>57):
			contact_ok=0
			break
	cursor = connection.cursor()
	cursor.execute("select * from customer where username='"+username+"';")
	res=cursor.fetchone()
	connection.close()

	if not contact_ok:
		messages.error(request, 'Invalid contact number.')
		return render(request, 'edit.html')
	elif not email_ok:
		messages.error(request, 'Invalid e-mail address.')
		return render(request, 'edit.html')
	else:
		cursor = connection.cursor()
		cursor.execute("update customer set fname='"+fname+"',lname='"+lname+"',gender='"+gender+"',email='"+email+"',add1='"+add1+"',add2='"+add2+"',city='"+city+"',contact='"+contact+"' where username='"+request.user.username+"';")
		connection.commit()
		connection.close()
		messages.success(request, 'Changes saved.')
		return HttpResponseRedirect(reverse('profile'))

def shop(request):
	cursor=connection.cursor()
	cursor.execute("select distinct category from product order by category;")
	categories=list(cursor.fetchall())
	# connection.close()
	# print len(categories),"YOYOYO", categories
	inv=[]
	for cat in categories:
		categ=cat[0]
		# print categ
		# cursor=connection.cursor()
		get_items="select * from product where category='"+categ+"' order by name;"
		cursor.execute(get_items)
		items=list(cursor.fetchall())
		for i in xrange(len(items)):
			items[i]=list(items[i])
			# print items[i]
		temp=[]
		temp.append(categ)
		temp.append(items)
		inv.append(temp)
	connection.close()
	#print inv[0][0]
	return render(request, "shop.html", {"inventory":inv})

def edit_inv(request):
	batchno=request.GET.get('batchno')
	print batchno, "YOYO"
	cursor=connection.cursor()
	cursor.execute("select * from product where batch_no='"+batchno+"';")
	res=list(cursor.fetchone())
	print res, "RES"
	connection.close()
	return render(request, 'edit_item.html', {'item':res})

def edit_item(request):
	batchno=request.POST['batchno']
	name=request.POST['name']
	wseller=request.POST['wseller']
	price=request.POST['price']
	category=request.POST['category']
	cursor=connection.cursor()
	cursor.execute("update product set name='"+name+"',w_seller='"+wseller+"',ret_price='"+price+"',category='"+category+"' where batch_no='"+batchno+"';")
	connection.commit()
	connection.close()
	return render(request, "shop.html")


def delete_item(request):
	batchno=request.GET.get('batchno')
	cursor=connection.cursor()
	cursor.execute("delete from product where batch_no='"+batchno+"';")
	connection.commit()
	connection.close()
	return HttpResponseRedirect(reverse('shop'))
	# return render(request, "shop.html")

def add_item_page(request):
	return render(request, 'add_item.html')

def add_item(request):
	if request.POST:
		batch_no=request.POST['batchno']
		name=request.POST['name']
		w_seller=request.POST['w_seller']
		ret_price=request.POST['ret_price']
		mfg_date=str(request.POST['mfg_date'])
		best_before=str(request.POST['best_before'])
		category=request.POST['category']
		curr_stock=request.POST['curr_stock']
		#for i in xrange(int(curr_stock)):
		cursor=connection.cursor()
			# cursor.execute("insert into product(batch_no,name,w_seller,ret_price,mfg_date,best_before,category,curr_stock) values('"+batch_no+"','"+name+"','"+w_seller+"','"+ret_price+"','"+mfg_date+"','"+best_before+"','"+category+"','"+curr_stock"'');")
		cursor.execute("insert into product(batch_no,name,w_seller,ret_price,mfg_date,best_before,category,curr_stock) values('%s','%s','%s','%s','%s','%s','%s','%s');"%(batch_no,name,w_seller,ret_price,mfg_date,best_before,category,curr_stock))
		connection.commit()
		connection.close()
	return HttpResponseRedirect(reverse('shop'))

# def cart(request):
# 	return render(request, 'mycart.html')

def mycart(request):
	cursor=connection.cursor()
	cursor.execute("select * from retail_record where username='"+request.user.username+"' and status=1;")
	x=cursor.fetchone()
	if x is not None:
		cursor.execute("select * from retail_record where username='"+request.user.username+"' and status=1;")
		ret_rec_id=list(cursor.fetchall())[0][0]
		cursor.execute("select * from retail_record where ret_rec_id="+str(ret_rec_id)+";")
		order_info=list(list(cursor.fetchall())[0])
		q="select product.batch_no, product.name, product.category, ret_price, prod_sale.quantity from product, prod_sale where product.batch_no=prod_sale.batch_no and prod_sale.ret_rec_id="+str(ret_rec_id)+";"
		cursor.execute(q)
		itemslist=list(cursor.fetchall())
		return render(request, 'mycart.html', {'order':order_info, 'items':itemslist})
	else:
		messages.error(request, 'No items in the cart.')
		return render(request, 'mycart.html')

def history(request):
		return render(request, 'history.html')

def add_to_cart(request):
	cursor=connection.cursor()
	batch_no=request.GET.get('batch_no')
	quantity=request.GET.get('quantity')
	print "B:", batch_no
	cursor.execute("select ret_price from product where batch_no="+str(batch_no)+";")
	res=list(list(cursor.fetchall())[0])[0]
	print "RES:",res
	cursor.execute("select * from retail_record where username='"+request.user.username+"' and status=1;")
	data = cursor.fetchone()
	print "DATA:", data
	if data is None:
		cursor.execute("insert into retail_record (ret_date,amt,username,status) values	(NOW(), 0,'"+request.user.username+"',1);")
		connection.commit()
	else:
		cursor.execute("select * from retail_record where username='"+request.user.username+"' and status=1;")
		ret_rec_id=list(cursor.fetchall())[0][0]
		q="select * from prod_sale where ret_rec_id="+str(ret_rec_id)+" and batch_no="+str(batch_no)+";"
		print q
		cursor.execute(q)
		res2=cursor.fetchall()
		if res2 is not None:
			cursor.execute("update prod_sale set quantity=quantity+1 where ret_rec_id="+str(ret_rec_id)+" and batch_no="+str(batch_no)+";")
			cursor.execute("update retail_record set amt=amt+"+str(res)+" where ret_rec_id="+str(ret_rec_id)+";")
		else:
			cursor.execute("insert into prod_sale values ("+str(ret_rec_id)+","+str(batch_no)+","+str(quantity)+");")
			cursor.execute("update retail_record set amt = amt+"+str(res)+" where ret_rec_id="+str(ret_rec_id)+";")
		connection.commit()
	return HttpResponseRedirect(reverse('shop'))


def makeadmin(request):
	return render(request, 'makeadmin.html')

def make_admin(request):
#	collect the form input
	fname=request.POST['fname']
	lname=request.POST['lname']
	gender=request.POST['gender']
	email=request.POST['email']
	add1=request.POST['add1']
	add2=request.POST['add2']
	city=request.POST['city']
	contact=request.POST['contact']
	username=request.POST['username']
	pwd=request.POST['pwd']
	pwd2=request.POST['pwd2']

	email_ok = re.search(r'[\w.-]+@[\w-]+\.[\w.-]+', email)
	contact_ok = 1
	if len(contact)!=11:
		contact_ok=0
	for char in contact:
		if(ord(char)<48 or ord(char)>57):
			contact_ok=0
			break
	cursor = connection.cursor()
	cursor.execute("select * from customer where username='"+username+"';")
	res=cursor.fetchone()
	connection.close()

	if not contact_ok:
		messages.error(request, 'Invalid contact number.')
		return render(request, 'register.html')
	elif not email_ok:
		messages.error(request, 'Invalid e-mail address.')
		return render(request, 'register.html')
	elif res is not None:
		messages.error(request, 'This username is taken.')
		return render(request, 'register.html')
	elif pwd != pwd2:
		messages.error(request, 'Passwords do not match.')
		return render(request, 'register.html')
	else:
		cursor = connection.cursor()
		try:
			print	"YOYOYOYOYO"
			cursor.execute("insert into customer(username, fname, lname, gender, add1, add2, city, email, contact) values('"+username+"','"+fname+"','"+lname+"','"+gender+"','"+add1+"','"+add2+"','"+city+"','"+email+"','"+contact+"');")
			user=User.objects.create_user(username, None, pwd)
			user.is_superuser=True
			user.save()
			connection.commit()
			messages.success(request, 'Admin created.')
			return render(request, 'home.html')
		except Exception as e:
			print e
			connection.rollback()
		connection.close()
		return HttpResponseRedirect(reverse('home'))

def orders(request):
	cursor=connection.cursor()
	cursor.execute("select * from retail_record;")
	data = list(list(cursor.fetchall()))
	return render(request, 'allorders.html', {'order_data': data})
# def payment(request):
