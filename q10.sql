SELECT CONSTRAINT_NAME	#we want this feiled
FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS	#from the raleation table_constraints
WHERE TABLE_NAME='film';	#the name of the table 