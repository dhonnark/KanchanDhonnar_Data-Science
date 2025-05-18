create database employee;
use employee;

select EMP_ID, FIRST_NAME, LAST_NAME, GENDER, DEPT FROM excel_employee_data;

select EMP_ID, FIRST_NAME, LAST_NAME, GENDER, DEPT,EMP_RATING 
FROM  excel_employee_data
WHERE EMP_RATING<2 ;

SELECT concat(FIRST_NAME,' ',last_name)as NAME 
           FROM excel_employee_data where DEPT ="finance"
           
select MANAGER_ID AS EMP_ID, COUNT(EMP_ID) AS NUMB_OF_REPORTERS 
from emp_record_table 
where MANAGER_ID is not null
group by MANAGER_ID

select* from emp_record_table
where dept="healthcare"
union
select* from emp_record_table
where dept="finance"



select * from excel_employee_data
select*, dense_rank() over(order by exp desc) from excel_employee_data

select t1.*,t2.min_salary from
(select role, max(salary) from excel_employee_data group by role) as t1
inner join
(select role, min(salary) as min_salary from excel_employee_data group by role) as t2
on t1.role=t2.role



create view vw_emp
as
select * from excel_employee_data
where salary>6000

select * from vw_emp

select * from(select * from excel_employee_data where exp>10) as t

delimiter //
create procedure sp1_exp()
begin
select * from excel_employee_data
where exp>3;
end //
delimiter ;

call sp1_exp

Select*, case
         When exp<2 then 'JUNIOR DATA SCIENTIST'
         When exp between 2 and 5  then 'ASSOCIATE DATA SCIENTIST'
         When exp between 5 and 10 then 'SENIOR DATA SCIENTIST'
         When exp between 10 and 12 then 'LEAD DATA SCIENTIST'
         When exp between 12 and 16 then 'manager'
         else 'Precident'
         End as POSITION
From excel_employee_data

alter table excel_employee_data
modify column first_name char(40)

create index inx_name on excel_employee_data(first_name)

select * from excel_employee_data
where first_name='eric';


select*,((0.05*salary)*emp_rating) as BONUS from excel_employee_data;

select continent,country, avg(salary) from excel_employee_data group by continent,country;





