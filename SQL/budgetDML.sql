--sof: initDML.sql
--Author: Michael Rayson
--desc: Provides sample data for the database for testing

--deletes all data from account table and transaction table
delete from transaction_t;
delete from account_t;
delete from category_t;

--inserts accounts into the account table
insert into account_t(account_name, account_balance) values ('ScotiaChecking', 0);
insert into account_t(account_name, account_balance) values ('PCFinancial', 0);

--inserts categories into the category table
insert into category_t(category_name) values('Unsorted');
insert into category_t(category_name) values('Monthly Expense: Rent');
insert into category_t(category_name) values('Monthly Expense: Hydro');
insert into category_t(category_name) values('Monthly Expense: Internet');
insert into category_t(category_name) values('Everyday Expense: Groceries');
insert into category_t(category_name) values('Everyday Expense: Gas');
insert into category_t(category_name) values('Everyday Expense: Eating Out');
insert into category_t(category_name) values('Misc Expense: Clothes');
insert into category_t(category_name) values('Misc Expense: Entertainment');
insert into category_t(category_name) values('Misc Expense: Bills');
insert into category_t(category_name) values('Misc Expense: Repair/Home');
insert into category_t(category_name) values('Misc Expense: School');
insert into category_t(category_name) values('Transfer: Savings');
insert into category_t(category_name) values('Transfer: Misc');
insert into category_t(category_name) values('Income: Work');
insert into category_t(category_name) values('Income: Misc');

-- insert into transaction_t(account_name, trans_amount, trans_date, trans_payee, trans_desc, category_name)
-- 	values ('ScotiaChecking', 2140.83, '2019-11-01','None','INITIALISATION','INIT')

-- insert into transaction_t(account_name, trans_amount, trans_date, trans_payee, trans_desc, category_name)
-- 	values ('PCFinancial', -21.81, '2019-11-01','None','INITIALISATION','INIT')
--eof: initDML.sql