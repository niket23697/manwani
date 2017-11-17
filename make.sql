use manwani;
create table customer(
	username varchar(30) primary key,
	fname varchar(30),
	lname varchar(30),
	gender varchar(10),
	add1 varchar(30),
	add2 varchar(30),
	city varchar(2),
	email varchar(50),
	contact varchar(11),
	no_of_orders int default 0);

create table product(
	batch_no int primary key,
	name varchar(30),
	w_seller varchar(30),
	ret_price int,
	mfg_date date,
	best_before int,
	category varchar(30),
	curr_stock int,
	pur_rec_id int);

create table retail_record(
	ret_rec_id int primary key auto_increment,
	ret_date datetime,
	amt int,
	username varchar(30),
	status int);

create table feedback(
	fb_id int primary key auto_increment,
	content varchar(500),
	username varchar(30));

create table prod_sale(
	ret_rec_id int,
	batch_no int
	);
alter table prod_sale add primary key (ret_rec_id, sno);

create table pur_record(
	pur_rec_id int primary key auto_increment,
	pur_date date,
	amt int,
	w_seller_id int);

create table w_seller(
	w_seller_id int primary key,
	w_seller_name varchar(30),
	w_seller_address varchar(60));

constraint f1 feedback(username) references customer(username)