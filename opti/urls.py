from django.conf.urls import url,include
from django.contrib import admin
from . import views

urlpatterns = [
	url(r'^home/$', views.home, name="home"),
	url(r'^register/$', views.register, name="register"),
	url(r'^register_user/$', views.register_user, name="register_user"),
	url(r'^login/$', views.login,name="login"),
	url(r'^feedback/$', views.feedback, name="feedback"),
	url(r'^profile/$', views.profile, name="profile"),
	url(r'^contact/$', views.contact, name="contact"),
	url(r'^logout/$', views.logout, name="logout"),
	url(r'^edit/$', views.edit, name="edit"),
	url(r'^edit_profile/$', views.edit_profile, name="edit_profile"),
	url(r'^shop/$', views.shop, name="shop"),
	url(r'^edit_inv/$', views.edit_inv, name="edit_inv"),
	url(r'^edit_item/$', views.edit_item, name="edit_item"),
	url(r'^delete_item/$', views.delete_item, name="delete_item"),
	url(r'^add_item_page/$', views.add_item_page, name="add_item_page"),
	url(r'^add_item/$', views.add_item, name="add_item"),
	url(r'^history/$', views.history, name="history"),
	url(r'^makeadmin/$', views.makeadmin, name="makeadmin"),
	url(r'^make_admin/$', views.make_admin, name="make_admin"),
	url(r'^mycart/$', views.mycart, name="mycart"),
	url(r'^add_to_cart/$', views.add_to_cart, name="add_to_cart"),
	url(r'^orders/$', views.orders, name="orders")
	]