-- CS4400: Introduction to Database Systems
-- Bank Management Project - Phase 3 (v2)
-- Generating Stored Procedures & Functions for the Use Cases
-- April 4th, 2022

-- implement these functions and stored procedures on the project database
use bank_management;

-- [1] create_corporation()
-- This stored procedure creates a new corporation
drop procedure if exists create_corporation;
delimiter //
create procedure create_corporation (in ip_corpID varchar(100),
    in ip_shortName varchar(100), in ip_longName varchar(100),
    in ip_resAssets integer)
cre_corp: begin
	if exists (select * from corporation where ip_corpID = corpId) then select 1; leave cre_corp; end if;
    if exists (select * from corporation where shortName = ip_shortName) then select 2; leave cre_corp; end if;
    if exists (select * from corporation where longName = ip_longName) then select 3; leave cre_corp; end if;
	insert into corporation (corpId, shortName, longName, resAssets) values (ip_corpID, ip_shortName, ip_longName, ip_resAssets);
end //
delimiter ;

-- [2] create_bank()
-- This stored procedure creates a new bank that is owned by an existing corporation
-- The corporation must also be managed by a valid employee [being a manager doesn't leave enough time for other jobs]
drop procedure if exists create_bank;
delimiter //
create procedure create_bank (in ip_bankID varchar(100), in ip_bankName varchar(100),
	in ip_street varchar(100), in ip_city varchar(100), in ip_state char(2),
    in ip_zip char(5), in ip_resAssets integer, in ip_corpID varchar(100),
    in ip_manager varchar(100), in ip_bank_employee varchar(100))
cre_bank: begin
	if (ip_manager in (select perID from workfor union select manager from bank)) then select 1; leave cre_bank; end if;
    if exists (select * from bank where bankID = ip_bankID) then select 2; leave cre_bank; end if;
    if exists (select * from bank where street = ip_street and city = ip_city and state = ip_state and zip = ip_zip) then select 3; leave cre_bank; end if;
	insert into bank values
    (ip_bankID,ip_bankName,ip_street,ip_city,ip_state,ip_zip,ip_resAssets,ip_corpID,ip_manager);
    
    insert into workfor values
    (ip_bankID,ip_bank_employee);
end //
delimiter ;

-- [3] start_employee_role()
-- If the person exists as an admin or employee then don't change the database state [not allowed to be admin along with any other person-based role]
-- If the person doesn't exist then this stored procedure creates a new employee
-- If the person exists as a customer then the employee data is added to create the joint customer-employee role
drop procedure if exists start_employee_role;
delimiter //
create procedure start_employee_role (in ip_perID varchar(100), in ip_taxID char(11),
	in ip_firstName varchar(100), in ip_lastName varchar(100), in ip_birthdate date,
    in ip_street varchar(100), in ip_city varchar(100), in ip_state char(2),
    in ip_zip char(5), in ip_dtJoined date, in ip_salary integer,
    in ip_payments integer, in ip_earned integer, in emp_password  varchar(100))
sp_main: begin
	-- Implement your code here
    if ip_perID in (select perID from employee) then select 1; leave sp_main; end if;
    if ip_perID in (select perID from system_admin) then select 2; leave sp_main; end if;
	if ip_taxID in (select taxID from bank_user) then select 3; leave sp_main; end if;
    if ip_perID not in (select perID from person) then
    insert into person values(ip_perID, emp_password);
    insert into bank_user values(ip_perID, ip_taxID, ip_birthdate, ip_firstName,
		ip_lastName, ip_dtJoined, ip_street, ip_city, ip_state, ip_zip); end if;
    insert into employee values (ip_perID, ip_salary, ip_payments, ip_earned);
end //
delimiter ;

-- [4] start_customer_role()
-- If the person exists as an admin or customer then don't change the database state [not allowed to be admin along with any other person-based role]
-- If the person doesn't exist then this stored procedure creates a new customer
-- If the person exists as an employee then the customer data is added to create the joint customer-employee role
drop procedure if exists start_customer_role;
delimiter //
create procedure start_customer_role (in ip_perID varchar(100), in ip_taxID char(11),
	in ip_firstName varchar(100), in ip_lastName varchar(100), in ip_birthdate date,
    in ip_street varchar(100), in ip_city varchar(100), in ip_state char(2),
    in ip_zip char(5), in ip_dtJoined date, in cust_password varchar(100))
sp_main: begin
	-- Implement your code here
    if exists (select perID from system_admin where perID = ip_perID) then select 1; leave sp_main; end if;
    if exists (select perID from customer where perID = ip_perID) then select 2; leave sp_main; end if;
	if exists (select taxID from bank_user where taxID = ip_taxID) then select 3; leave sp_main; end if;
    if not ip_perID in (select perID from person) then
		insert into person values(ip_perID, cust_password); 
	end if;
	if not ip_perID in (select perID from bank_user) then
		insert into bank_user values(ip_perID, ip_taxID, ip_birthdate, ip_firstName, ip_lastName,
		ip_dtJoined, ip_street, ip_city, ip_state, ip_zip);
	end if;
    insert into customer values(ip_perID);
		
end //
delimiter ;

-- [5] stop_employee_role()
-- If the person doesn't exist as an employee then don't change the database state
-- If the employee manages a bank or is the last employee at a bank then don't change the database state [each bank must have a manager and at least one employee]
-- If the person exists in the joint customer-employee role then the employee data must be removed, but the customer information must be maintained
-- If the person exists only as an employee then all related person data must be removed
drop procedure if exists stop_employee_role;
delimiter //
create procedure stop_employee_role (in ip_perID varchar(100))
sp_main: begin
	-- Implement your code here
    if ip_perID not in (select perID from employee) then select 1; leave sp_main; end if;
    if ip_perID in (select manager from bank) then select 2; leave sp_main; end if;
    if ip_perID in (select perID from workFor where bankID in
    (select bankID from workFor group by bankID having count(perID) = 1))
    then select 3; leave sp_main;
    end if;
    
    if ip_perID in 
    (select perID from employee where perID not in
    (select perID from customer) and perID is not NULL) then 
    set FOREIGN_KEY_CHECKS = 0;
    delete from person where perID = ip_perID;
    delete from bank_user where perID = ip_perID;
    delete from employee where perID = ip_perID;
    delete from workFor where perID = ip_perID;
    set FOREIGN_KEY_CHECKS = 1;
    end if;
    
    if ip_perID in 
    (select perID from employee where perID in
    (select perID from customer) and perID is not NULL) then
    set FOREIGN_KEY_CHECKS = 0;
    delete from employee where perID = ip_perID;
    delete from workFor where perID = ip_perID;
    set FOREIGN_KEY_CHECKS = 1;
    end if;
end //
delimiter ;

-- [6] stop_customer_role()
-- If the person doesn't exist as an customer then don't change the database state
-- If the customer is the only holder of an account then don't change the database state [each account must have at least one holder]
-- If the person exists in the joint customer-employee role then the customer data must be removed, but the employee information must be maintained
-- If the person exists only as a customer then all related person data must be removed
drop procedure if exists stop_customer_role;
delimiter //
create procedure stop_customer_role (in ip_perID varchar(100))
sp_main: begin
	-- Implement your code here
    if not exists (select perID from customer where perID = ip_perID) then select 1; leave sp_main; end if;
    if exists (select accountID from access where accountID in 
		(select accountID from access where perID = ip_perID)
		group by accountID having count(*) = 1)
    then select 2; leave sp_main; end if;
	delete from access where perID = ip_perID;
    delete from customer_contacts where perID = ip_perID;
    delete from customer where perID = ip_perID;
    if exists (select perID from employee where perID = ip_perID) then leave sp_main; end if;
    delete from bank_user where perID = ip_perID;
    delete from person where perID = ip_perID;
    
end //
delimiter ;

-- [7] hire_worker()
-- If the person is not an employee then don't change the database state
-- If the worker is a manager then then don't change the database state [being a manager doesn't leave enough time for other jobs]
-- Otherwise, the person will now work at the assigned bank in addition to any other previous work assignments
-- Also, adjust the employee's salary appropriately
drop procedure if exists hire_worker;
delimiter //
create procedure hire_worker (in ip_perID varchar(100), in ip_bankID varchar(100),
	in ip_salary integer)
sp_main: begin
	-- Implement your code here
    if ip_perID not in (select perID from employee) then select 1; leave sp_main; end if;
    if ip_perID in (select manager from bank) then select 2; leave sp_main; end if;
	if (ip_bankID, ip_perID) in (select * from workFor) then select 3; leave sp_main; end if;
    
    insert into workFor values (ip_bankID, ip_perID);
    update employee set salary = ip_salary where perID = ip_perID;
end //
delimiter ;

-- [8] replace_manager()
-- If the new person is not an employee then don't change the database state
-- If the new person is a manager or worker at any bank then don't change the database state [being a manager doesn't leave enough time for other jobs]
-- Otherwise, replace the previous manager at that bank with the new person
-- The previous manager's association as manager of that bank must be removed
-- Adjust the employee's salary appropriately
drop procedure if exists replace_manager;
delimiter //
create procedure replace_manager (in ip_perID varchar(100), in ip_bankID varchar(100),
	in ip_salary integer)
sp_main: begin
	-- Implement your code here
    if ip_perID not in (select perID from employee) then select 1; leave sp_main; end if;
    if ip_perID in (select manager from bank) then select 2; leave sp_main; end if;
    if ip_perID in (select perID from workFor) then select 3; leave sp_main; end if;
    
    update bank set manager = ip_perID where bankID = ip_bankID;
    update employee set salary = ip_salary where perID = ip_perID;
end //
delimiter ;

-- [9] add_account_access()
-- If the account does not exist, create a new account. If the account exists, add the customer to the account
-- When creating a new account:
    -- If the person opening the account is not an admin then don't change the database state
    -- If the intended customer (i.e. ip_customer) is not a customer then don't change the database state
    -- Otherwise, create a new account owned by the designated customer
    -- The account type will be determined by the enumerated ip_account_type variable
    -- ip_account_type in {checking, savings, market}
-- When adding a customer to an account:
    -- If the person granting access is not an admin or someone with access to the account then don't change the database state
    -- If the intended customer (i.e. ip_customer) is not a customer then don't change the database state
    -- Otherwise, add the new customer to the existing account
drop procedure if exists add_account_access;
delimiter //
create procedure add_account_access (in ip_requester varchar(100), in ip_customer varchar(100),
	in ip_account_type varchar(10), in ip_bankID varchar(100),
    in ip_accountID varchar(100), in ip_balance integer, in ip_interest_rate integer,
    in ip_dtDeposit date, in ip_minBalance integer, in ip_numWithdrawals integer,
    in ip_maxWithdrawals integer, in ip_dtShareStart date)
add_account_access_main: begin
	if (ip_requester not in (select perID from customer union select perId from system_admin)) then leave add_account_access_main; end if;
    if ((ip_bankID,ip_accountID) in (select bankID, accountID from bank_account)) then
		if exists (select * from access where bankID = ip_bankID and accountID = ip_accountID and perID = ip_customer) then select 1; leave add_account_access_main; end if;
		insert into access values(ip_customer,ip_bankID,ip_accountID,ip_dtShareStart,null);
        leave add_account_access_main;
	end if;
    if (ip_requester not in (select perID from system_admin)) then leave add_account_access_main; end if;
		if (ip_account_type = 'checking') then
			insert into bank_account values(ip_bankID,ip_accountID,ip_balance);
			insert into access values(ip_customer,ip_bankID,ip_accountID,ip_dtShareStart,null);
			insert into checking values(ip_bankID,ip_accountID,null,null,null,null);
		elseif (ip_account_type = 'savings') then
			insert into bank_account values(ip_bankID,ip_accountID,ip_balance);
			insert into access values(ip_customer,ip_bankID,ip_accountID,ip_dtShareStart,null);
			insert into interest_bearing values(ip_bankID,ip_accountID, ip_interest_rate, ip_dtDeposit);
			insert into savings values(ip_bankID,ip_accountID,ip_minBalance);
		else
			insert into bank_account values(ip_bankID,ip_accountID,ip_balance);
			insert into access values(ip_customer,ip_bankID,ip_accountID,ip_dtShareStart,null);
			insert into interest_bearing values(ip_bankID,ip_accountID, ip_interest_rate, ip_dtDeposit);
			insert into market values(ip_bankID,ip_accountID,ip_maxWithdrawals,ip_numWithdrawals);
		end if;
end //
delimiter ;


-- [10] remove_account_access()
-- Remove a customer's account access. If they are the last customer with access to the account, close the account
-- When just revoking access:
    -- If the person revoking access is not an admin or someone with access to the account then don't change the database state
    -- Otherwise, remove the designated sharer from the existing account
-- When closing the account:
    -- If the customer to be removed from the account is NOT the last remaining owner/sharer then don't close the account
    -- If the person closing the account is not an admin or someone with access to the account then don't change the database state
    -- Otherwise, the account must be closed
drop procedure if exists remove_account_access;
delimiter //
create procedure remove_account_access (in ip_requester varchar(100), in ip_sharer varchar(100),
	in ip_bankID varchar(100), in ip_accountID varchar(100))
remove_account_access_main:begin
	if ((ip_requester not in (select perID from system_admin)) and (ip_requester not in (select perID from customer))) then leave remove_account_access_main; end if;
    if ((ip_bankID,ip_accountID) in (select A.bankID, A.accountID from (select * from access where perID != ip_sharer) as A)) then
		delete from access where ip_sharer = perID and ip_bankID = bankID and ip_accountID = accountID;
    else 
		delete from access where ip_sharer = perID and ip_bankID = bankID and ip_accountID = accountID;
		if (ip_bankID,ip_accountID) in (select bankID, accountID from interest_bearing) then
			if (ip_bankID,ip_accountID) in (select bankID, accountID from market)  then
				delete from market where ip_bankID = bankID and ip_accountID = accountID;
			else 
				update checking set dtOverdraft= null,amount = null,protectionBank = null, protectionAccount = null where ip_bankID = protectionBank and ip_accountID = protectionAccount;
				delete from savings where ip_bankID = bankID and ip_accountID = accountID;
			end if;
            delete from interest_bearing_fees where ip_bankID = bankID and ip_accountID = accountID;
			delete from interest_bearing where ip_bankID = bankID and ip_accountID = accountID;
		else 
			delete from checking where ip_bankID = bankID and ip_accountID = accountID;
		end if;
		delete from bank_account where ip_bankID = bankID and ip_accountID = accountID;
    end if;
end //
delimiter ;



-- [11] create_fee()
drop procedure if exists create_fee;
delimiter //
create procedure create_fee (in ip_bankID varchar(100), in ip_accountID varchar(100),
	in ip_fee_type varchar(100))
create_fee_main: begin
	if exists (select * from interest_bearing_fees where (bankID, accountID, fee) = (ip_bankID, ip_accountID, ip_fee_type))
    then select 1; leave create_fee_main; end if;
	if not exists (select * from bank_account where (bankID, accountID) = (ip_bankID, ip_accountID))
    then select 2; leave create_fee_main; end if;
    if not exists (select * from interest_bearing where (bankID, accountID) = (ip_bankID, ip_accountID))
    then select 3; leave create_fee_main; end if;
	Insert into interest_bearing_fees (bankID, accountID, fee) values (ip_bankID, ip_accountID, ip_fee_type);
end //
delimiter ;

-- [12] start_overdraft()
drop procedure if exists start_overdraft;
delimiter //
create procedure start_overdraft (in ip_requester varchar(100),
	in ip_checking_bankID varchar(100), in ip_checking_accountID varchar(100),
    in ip_savings_bankID varchar(100), in ip_savings_accountID varchar(100))
start_overdraft_main: begin
    if ((ip_requester not in (select perID from system_admin)) and (ip_requester not in (select perID from customer))) then leave start_overdraft_main; end if;
    if not exists (select * from checking where bankID = ip_checking_bankID AND accountID = ip_checking_accountID) then select 1; leave start_overdraft_main; end if;
    if not exists (select * from savings where bankID = ip_savings_bankID AND accountID = ip_savings_accountID) then select 2; leave start_overdraft_main; end if;
	if ip_savings_bankID in (select protectionBank from checking) and 
		ip_savings_accountID in (select protectionAccount from checking) then select 3; leave start_overdraft_main; end if;
    if exists (select protectionBank, protectionAccount from checking where bankID = ip_checking_bankID and accountID = ip_checking_accountID
    and protectionBank is not null and protectionAccount is not null) then select 4; leave start_overdraft_main; end if;
    update checking set protectionBank = ip_savings_bankID, protectionAccount = ip_savings_accountID where bankID = ip_checking_bankID AND accountID = ip_checking_accountID;
end //
delimiter ;

-- [13] stop_overdraft()
drop procedure if exists stop_overdraft;
delimiter //
create procedure stop_overdraft (in ip_requester varchar(100),
	in ip_checking_bankID varchar(100), in ip_checking_accountID varchar(100))
stop_overdraft_main: begin
    if ((ip_requester not in (select perID from system_admin)) and (ip_requester not in (select perID from customer))) then leave stop_overdraft_main; end if;
	if not exists (select * from checking where bankID = ip_checking_bankID AND accountID = ip_checking_accountID) then select 1; leave stop_overdraft_main; end if;
    if not exists (select * from checking where bankID = ip_checking_bankID AND accountID = ip_checking_accountID
    and protectionBank is not null and protectionAccount is not null) then select 2; leave stop_overdraft_main; end if;
	update checking set protectionBank = null, protectionAccount = null where ip_checking_bankID = bankID and ip_checking_accountID = accountID;
end //
delimiter ;


-- [14] account_deposit()
-- If the person making the deposit does not have access to the account then don't change the database state
-- Otherwise, the account balance and related info must be modified appropriately
drop procedure if exists account_deposit;
delimiter //
create procedure account_deposit (in ip_requester varchar(100), in ip_deposit_amount integer,
	in ip_bankID varchar(100), in ip_accountID varchar(100), in ip_dtAction date)
acc_dep: begin
	-- Implement your code here	
    if (select ip_accountID in (select accountID from access where perID = ip_requester and bankID = ip_bankID) = 0) then leave acc_dep; end if;
    
	update access
	set dtAction = ip_dtAction
	where perID = ip_requester and bankID = ip_bankID and accountID = ip_accountID;
    
    update bank_account
	set balance = balance + ip_deposit_amount
	where accountID = ip_accountID and ip_bankID = bankID;
    
    update interest_bearing
	set dtDeposit = ip_dtAction
	where accountID = ip_accountID and ip_bankID = bankID;
end //
delimiter ;

-- [15] account_withdrawal()
-- If the person making the withdrawal does not have access to the account then don't change the database state
-- If the withdrawal amount is more than the account balance for a savings or market account then don't change the database state [the account balance must be positive]
-- If the withdrawal amount is more than the account balance + the overdraft balance (i.e., from the designated savings account) for a checking account then don't change the database state [the account balance must be positive]
-- Otherwise, the account balance and related info must be modified appropriately (amount deducted from the primary account first, and second from the overdraft account as needed)
drop procedure if exists account_withdrawal;
delimiter //
create procedure account_withdrawal (in ip_requester varchar(100), in ip_withdrawal_amount integer,
	in ip_bankID varchar(100), in ip_accountID varchar(100), in ip_dtAction date)
acc_with: begin
-- if no access, leave
if (select ip_accountID in (select accountID from access where perID = ip_requester and bankID = ip_bankID) = 0) then leave acc_with; end if;
-- if checking
if (exists (select * from checking where bankID = ip_bankID and accountID = ip_accountID)) then
	-- if no enough money, leave
	if (select balance from bank_account where bankID = ip_bankID and accountID = ip_accountID) < (ip_withdrawal_amount - ifnull((select balance from bank_account where accountID = (select protectionAccount from checking where bankID = ip_bankID and accountID = ip_accountID) and (select protectionBank from checking where bankID = ip_bankID and accountID = ip_accountID) = bankID), 0)) then select 1; leave acc_with; end if;
    -- else
    update access
	set dtAction = ip_dtAction
	where perID = ip_requester and bankID = ip_bankID and accountID = ip_accountID;
    
-- 	update market
-- 	set numWithdrawals = numWithdrawals + 1
-- 	where accountID = ip_accountID and ip_bankID = bankID;
    
    -- if enough money in account, normal update
    if (select balance from bank_account where bankID = ip_bankID and accountID = ip_accountID) > ip_withdrawal_amount then
		update bank_account
		set balance = balance - ip_withdrawal_amount
		where accountID = ip_accountID and ip_bankID = bankID;
        leave acc_with;
	end if;
    -- else, use protection
    update checking
	set amount = (ip_withdrawal_amount - (select balance from bank_account where accountID = ip_accountID and ip_bankID = bankID))
	where accountID = ip_accountID and ip_bankID = bankID;
    
	update bank_account
	set balance = balance - (ip_withdrawal_amount - (select balance from (select balance from bank_account where accountID = ip_accountID and ip_bankID = bankID) as t))
	where accountID = (select protectionAccount from checking where bankID = ip_bankID and accountID = ip_accountID) and (select protectionBank from checking where bankID = ip_bankID and accountID = ip_accountID) = bankID;

	update bank_account
	set balance = 0
	where accountID = ip_accountID and ip_bankID = bankID;
    
    update checking
    set dtOverdraft = ip_dtAction
    where accountID = ip_accountID and ip_bankID = bankID;
    
	update access
	set dtAction = ip_dtAction
	where accountID = (select protectionAccount from checking where bankID = ip_bankID and accountID = ip_accountID) and (select protectionBank from checking where bankID = ip_bankID and accountID = ip_accountID) = bankID;
end if;
	
-- if interest_bearing
if (exists (select * from interest_bearing where bankID = ip_bankID and accountID = ip_accountID)) then
	## if no enough money, leave
	if (select balance from bank_account where bankID = ip_bankID and accountID = ip_accountID) < ip_withdrawal_amount then select 1; leave acc_with; end if;
	update access
	set dtAction = ip_dtAction
	where perID = ip_requester and bankID = ip_bankID and accountID = ip_accountID;

	update bank_account
	set balance = balance - ip_withdrawal_amount
	where accountID = ip_accountID and ip_bankID = bankID;

	update market
	set numWithdrawals = numWithdrawals + 1
	where accountID = ip_accountID and ip_bankID = bankID;
end if;	
end //
delimiter ;

-- [16] account_transfer()
-- If the person making the transfer does not have access to both accounts then don't change the database state
-- If the withdrawal amount is more than the account balance for a savings or market account then don't change the database state [the account balance must be positive]
-- If the withdrawal amount is more than the account balance + the overdraft balance (i.e., from the designated savings account) for a checking account then don't change the database state [the account balance must be positive]
-- Otherwise, the account balance and related info must be modified appropriately (amount deducted from the withdrawal account first, and second from the overdraft account as needed, and then added to the deposit account)
drop procedure if exists account_transfer;
delimiter //
create procedure account_transfer (in ip_requester varchar(100), in ip_transfer_amount integer,
	in ip_from_bankID varchar(100), in ip_from_accountID varchar(100),
    in ip_to_bankID varchar(100), in ip_to_accountID varchar(100), in ip_dtAction date)
acc_trans: begin
	-- Implement your code here
-- if no access, leave

if (select ip_from_accountID in (select accountID from access where perID = ip_requester and bankID = ip_from_bankID) = 0) then select 2; leave acc_trans; end if;
-- if checking
if (exists (select * from checking where bankID = ip_from_bankID and accountID = ip_from_accountID)) then
	-- if no enough money, leave
	if (select balance from bank_account where bankID = ip_from_bankID and accountID = ip_from_accountID) < (ip_transfer_amount - ifnull((select balance from bank_account where accountID = (select protectionAccount from checking where bankID = ip_from_bankID and accountID = ip_from_accountID) and (select protectionBank from checking where bankID = ip_from_bankID and accountID = ip_from_accountID) = bankID), 0)) then select 1; leave acc_trans; end if;
    -- else
    update access
	set dtAction = ip_dtAction
	where perID = ip_requester and bankID = ip_from_bankID and accountID = ip_from_accountID;

	update bank_account
	set balance = ifnull(balance, 0) + ip_transfer_amount
	where accountID = ip_to_accountID and ip_to_bankID = bankID;
    
    -- if enough money in account, normal update
    if (select balance from bank_account where bankID = ip_from_bankID and accountID = ip_from_accountID) > ip_transfer_amount then
		update bank_account
		set balance = balance - ip_transfer_amount
		where accountID = ip_from_accountID and ip_from_bankID = bankID;
        leave acc_trans;
	end if;
    -- else, use protection
    update checking
	set amount = (ip_transfer_amount - (select balance from bank_account where accountID = ip_from_accountID and ip_from_bankID = bankID))
	where accountID = ip_from_accountID and ip_from_bankID = bankID;
    
	update bank_account
	set balance = balance - (ip_transfer_amount - (select balance from (select balance from bank_account where accountID = ip_from_accountID and ip_from_bankID = bankID) as t))
	where accountID = (select protectionAccount from checking where bankID = ip_from_bankID and accountID = ip_from_accountID) and (select protectionBank from checking where bankID = ip_from_bankID and accountID = ip_from_accountID) = bankID;

	update bank_account
	set balance = 0
	where accountID = ip_from_accountID and ip_from_bankID = bankID;
    
    update checking
    set dtOverdraft = ip_dtAction
    where accountID = ip_from_accountID and ip_from_bankID = bankID;
    
	update access
	set dtAction = ip_dtAction
	where accountID = (select protectionAccount from checking where bankID = ip_from_bankID and accountID = ip_from_accountID) and (select protectionBank from checking where bankID = ip_from_bankID and accountID = ip_from_accountID) = bankID;
end if;
	
-- if interest_bearing
if (exists (select * from interest_bearing where bankID = ip_from_bankID and accountID = ip_from_accountID)) then
	## if no enough money, leave
	if (select balance from bank_account where bankID = ip_from_bankID and accountID = ip_from_accountID) < ip_withdrawal_amount then select 1; leave acc_trans; end if;
	
    update access
	set dtAction = ip_dtAction
	where perID = ip_requester and bankID = ip_from_bankID and accountID = ip_from_accountID;

	update bank_account
	set balance = balance - ip_transfer_amount
	where accountID = ip_from_accountID and ip_from_bankID = bankID;

	update market
	set numWithdrawals = numWithdrawals + 1
	where accountID = ip_from_accountID and ip_from_bankID = bankID;
    
	update bank_account
	set balance = ifnull(balance, 0) + ip_transfer_amount
	where accountID = ip_to_accountID and ip_to_bankID = bankID;
end if;	
end //
delimiter ;

-- [17] pay_employees()
-- Increase each employee's pay earned so far by the monthly salary
-- Deduct the employee's pay from the banks reserved assets
-- If an employee works at more than one bank, then deduct the (evenly divided) monthly pay from each of the affected bank's reserved assets
-- Truncate any fractional results to an integer before further calculations
drop procedure if exists pay_employees;
delimiter //
create procedure pay_employees ()
begin
    -- Implement your code here
    update employee
	set earned = 0
	where salary is not null and earned is null;

	update employee
	set payments = 0
	where payments is null;
    
    
    update employee set
    earned = earned + salary
    where salary is not null;
    
    update employee set
    payments = payments + 1;
    
    update bank set
    resAssets = 0
    where resAssets is null and bank.bankID in 
    (select bankID from workFor where perID in
    (select perID from employee where salary is not null));
    
    -- checkpoint: pay earned updated successfully
    
    #update bank set
	#resAssets = resAssets - (select salary from employee where perID = bank.manager and salary is not null);
    
    -- checkpoint: assets reduced due to managers' salary updated successfully
    
    create or replace view workers_and_num_banks as
	select wf.perID as perID, count(wf.bankID) as total_banks
	from workFor as wf
	where wf.perID in (select perID from employee where salary is not null)
	group by wf.perID;
    
    create or replace view payment_per_bank as
	select wanb.perID as perID, floor(e.salary / wanb.total_banks) as payment_per_bank
	from workers_and_num_banks as wanb,
    employee as e
	where wanb.perID = e.perID
	group by wanb.perID;
    
    update bank set
    resAssets = resAssets - (select sum(ppb.payment_per_bank)
	from workFor as wf, payment_per_bank as ppb
	where wf.perID = ppb.perID and bank.bankID = wf.bankID
	group by wf.bankID);
    
    drop view if exists workers_and_num_banks;
    drop view if exists payment_per_bank;
end //
delimiter ;

-- [18] penalize_accounts()
-- For each savings account that is below the minimum balance, deduct the smaller of $100 or 10% of the current balance from the account
-- For each market account that has exceeded the maximum number of withdrawals, deduct the smaller of $500 per excess withdrawal or 20% of the current balance from the account
-- Add all deducted amounts to the reserved assets of the bank that owns the account
-- Truncate any fractional results to an integer before further calculations
drop procedure if exists penalize_accounts;
delimiter //
create procedure penalize_accounts ()
begin
	-- Implement your code here
		create or replace view penalizeSaving as
        select *, least(truncate(0.1 * balance, 0), 100) as "penalty" from bank natural join
        bank_account natural join interest_bearing natural join savings
		where bank_account.balance < savings.minBalance;
        
        update penalizeSaving set balance = balance - penalty;

		update penalizeSaving set resAssets = resAssets + (select penalty from
		(select bankID, sum(penalty)as penalty from penalizeSaving group by bankID) as temp 
		where temp.bankID = penalizeSaving.bankID);
        
        drop view if exists penalizeSaving;
        
		create or replace view penalizeMarket as
        select *, least(truncate(0.2 * balance, 0), 500 * (numWithdrawals - maxWithdrawals)) as "penalty"
        from bank natural join bank_account natural join interest_bearing natural join market
		where numWithdrawals > maxWithdrawals;
        
        update penalizeMarket set balance = balance - penalty;
        
        update penalizeMarket set resAssets = resAssets + (select penalty from (select bankID, sum(penalty) from penalizeMarket
		group by bankID) as temp where temp.bankID = penalizeMarket.bankID);
  
  		drop view if exists penalizeMarket;
end //
delimiter ;



-- [19] accrue_interest()
-- For each interest-bearing account that is "in good standing", increase the balance based on the designated interest rate
-- A savings account is "in good standing" if the current balance is equal to or above the designated minimum balance
-- A market account is "in good standing" if the current number of withdrawals is less than or equal to the maximum number of allowed withdrawals
-- Subtract all paid amounts from the reserved assets of the bank that owns the account                                                                       
-- Truncate any fractional results to an integer before further calculations
drop procedure if exists accrue_interest;
delimiter //
create procedure accrue_interest ()
begin
	-- Implement your code here
		drop view if exists accrueInterestSaving;
            
		create or replace view accrueInterestSaving as
        select *, truncate(interest_rate * 0.01 * balance, 0) as "interest" from bank natural join
        bank_account natural join interest_bearing natural join savings
		where bank_account.balance >= savings.minBalance and interest_rate is not null;
        
		update accrueInterestSaving set resAssets = resAssets - (select interest from
		(select bankID, sum(interest)as interest from accrueInterestSaving group by bankID) as temp 
		where temp.bankID = accrueInterestSaving.bankID);
        
        update accrueInterestSaving set balance = balance + interest;
        
		drop view if exists accrueInterestMarket;
                
		create or replace view accrueInterestMarket as
        select *, truncate(interest_rate * 0.01 * balance, 0) as "interest" from bank natural join
        bank_account natural join interest_bearing natural join market
		where (numWithdrawals <= maxWithdrawals or numWithdrawals is null) and interest_rate is not null;
        
        
		update accrueInterestMarket set resAssets = ifnull(resAssets,0) - (select interest from
		(select bankID, sum(interest)as interest from accrueInterestMarket group by bankID) as temp 
		where temp.bankID = accrueInterestMarket.bankID);
        
        update accrueInterestMarket set balance = balance + interest;
        
end //
delimiter ;


-- [20] display_account_stats()
-- Display the simple and derived attributes for each account, along with the owning bank
-- create or replace view display_account_stats as
create or replace view display_account_stats as
select bankName as 'name_of_bank', bank_account.accountID as 'account_identifier', bank_account.balance as 'account_assets', count(*) as 'number_of_owners'
    from bank, bank_account, access
    where bank.bankID = bank_account.bankID and bank_account.accountID = access.accountID and bank_account.bankID = access.bankID
    group by access.accountID, access.bankID;

-- [21] display_bank_stats()
-- Display the simple and derived attributes for each bank, along with the owning corporation
-- create or replace view display_bank_stats as
    -- Uncomment above line and implement your code here
create or replace view display_bank_stats_helper as
select bankID, count(distinct accountID) as number_of_accounts, sum(balance) as total_balance
from bank_account
group by bankID;   
    
create or replace view display_bank_stats as
select bank.bankID as bank_identifier, shortName as name_of_corporation, bankName as name_of_bank, street, city, state, zip, number_of_accounts, bank.resAssets as bank_assets, ifnull(bank.resAssets, 0) + ifnull(total_balance, 0) as total_assets
from bank 
join corporation on bank.corpID = corporation.corpID
left outer join display_bank_stats_helper on display_bank_stats_helper.bankID = bank.bankID;

-- [22] display_corporation_stats()
-- Display the simple and derived attributes for each corporation
-- create or replace view display_corporation_stats as
create or replace view display_corporation_stats as
select corporation.corpId as 'corporation_identifier', corporation.shortName as 'short_Name', corporation.longName as 'formal_Name',  
count(distinct bank.bankID)  as 'number_of_banks', 
corporation.resAssets as 'Corporation_assets',  corporation.resAssets+ifnull(sum(ifnull(total_assets,0)),0) as 'total_assets'
from (corporation left outer join bank on corporation.corpID=bank.corpID
-- left outer join bank_account on bank.bankID=bank_account.bankID
left outer join display_bank_stats on corporation.shortName=display_bank_stats.name_of_corporation and display_bank_stats.bank_identifier = bank.bankID)
group by corporation.corpID;

-- [23] display_customer_stats()
-- Display the simple and derived attributes for each customer
-- create or replace view display_customer_stats as
    -- Uncomment above line and implement your code here

create or replace view display_customer_stats as
select bank_user.perID as "person_identifier", taxID as "tax_identifier",
concat(firstName, ' ', lastName) as "customer_name", birthdate as "date_of_birth", dtjoined as "joined_system",
street, city, state, zip, count(access.accountID) as "number_of_accounts", ifnull(sum(balance), 0) as "customer_assets"
from customer join bank_user on customer.perID = bank_user.perID
left outer join access on customer.perID = access.perID
left outer join bank_account on access.bankID = bank_account.bankID and access.accountID = bank_account.accountID 
group by customer.perID;

-- [24] display_employee_stats()
-- Display the simple and derived attributes for each employee
create or replace view display_employee_stats as
    -- Uncomment above line and implement your code here
select 
e.perID as person_identification_number,
bu.taxID as tax_identification_number,
concat(bu.firstName,' ', bu.lastName) as employee_name,
bu.birthdate as date_of_birth,
bu.dtJoined as joined_system,
bu.street as street,
bu.city as city,
bu.state as state,
bu.zip as zip,
IF(e.perID in (select perID from workFor), count(wf.bankID), NULL) as number_of_banks,
(total_resAssets + total_balance) as bank_assets
from ((employee as e, bank_user as bu) left outer join (workFor as wf) on e.perID = wf.perID)
left outer join
((select workFor.perID, sum(bank.resAssets) as total_resAssets
from workFor, bank
where workFor.bankID = bank.bankID 
group by workFor.perID) as tr, 
(select workFor.perID, sum(bank_account.balance) as total_balance
from workFor, bank_account
where workFor.bankID = bank_account.bankID
group by workFor.perID) as tb) on e.perID = tr.perID and tr.perID = tb.perID
where e.perID = bu.perID
group by e.perID;