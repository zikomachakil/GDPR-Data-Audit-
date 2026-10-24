SELECT
--Names masking----
	LEFT(first_name , 1) + '*****' + RIGHT(first_name , 0) AS First_Name,
	LEFT(last_name , 0) + '******' + RIGHT(last_name , 0) AS last_name,


--INFOS IDING
	LEFT(email , 0) + '*****' + SUBSTRING(email , CHARINDEX('@' , email) , LEN(email)) AS Secure_Email,
	LEFT(gender ,0) + 'XXXX' + RIGHT(gender , 0) AS Gender,
	LEFT(ip_address , 0) + '*******' + RIGHT(ip_address ,0) AS Ip_ADD,
	
	account_created_at,
	is_active,
	consent_given,
	consent_version
FROM Data7