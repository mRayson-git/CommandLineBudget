--sof: budgetDDL.sql
--Author: Michael Rayson
--Desc: Contains the DDL commands to create the tables needed for the budget database

--For testing reasons, delete in final version
drop table if exists transaction_t;
drop table if exists account_t;
drop table if exists category_t;

--Table for Accounts(Chequing, Savings, etc...)
CREATE TABLE account_t(
	account_name		varchar(60),
	account_balance		decimal(38,2),
	CONSTRAINT pk_account_name PRIMARY KEY(account_name)
);

--Table for Categories
CREATE TABLE category_t (
	category_id			int				auto_increment,
	category_name 		varchar(60)		not null,
	category_budget		decimal(38,2) 	default 0.00,
	category_time		date			default curdate(),
	CONSTRAINT pk_category_id PRIMARY KEY (category_id)
);

--Table for transactions(auto_increment trans_id starting from 1)
create table transaction_t (
	trans_id		int				auto_increment,
    account_name    varchar(60)		not null,
  	trans_amount  	decimal(38,2) 	not null,
  	trans_date    	date          	not null,
  	trans_payee   	varchar(60)   	default null,
	trans_desc		varchar(60)		default null,
	category_name 	varchar(60)		default 'None',
	memo			text			default '',
	CONSTRAINT pk_trans_id PRIMARY KEY (trans_id),
	CONSTRAINT fk_account_name FOREIGN KEY (account_name) REFERENCES account_t (account_name)
);

--Creating indexes
create index date on transaction_t (trans_date);

--eof:budgetDDl.sql