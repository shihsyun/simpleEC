<pre>
use DRF to provide EC function, include register, order.

User Story as below

1. User can register a customer.
2. Customer need verify their account before use.
3. User login/logout
4. Customer can change password.
5. Customer can apply to become a seller.
6. Seller can create/modify/delete Product.
7. Customer can create/modify/delete Product.

example as below
1.  POST http://127.0.0.1:8000/register/ 
    Input
	  {
		  "email":"test1@test.com",
		  "password":"Foo001"
	  }

2.  POST http://127.0.0.1:8000/verify_gencode/
    Input
    {
		  "email":"test1@test.com"
	  }
    Output
    "VMTlWOmo_ljZJjYhhmqFtTMExYU-97ZhXLj8l570"
    Get http://127.0.0.1:8000/verifycode/?token="VMTlWOmo_ljZJjYhhmqFtTMExYU-97ZhXLj8l570"
    Output HTTP_204_NO_CONTENT

3.  POST http://127.0.0.1:8000/login/
    Input
    {
		  "username":"test1@test.com",
		  "password":"Foo001"
	  }
    Output
    {
      "token": "7fa5cfbb41654244bbd9ee7e56390f967be1e856"
    }
    POST http://127.0.0.1:8000/logout/
    Input
    {
		  "username":"test1@test.com"
	  }
    Output HTTP_204_NO_CONTENT
4.  PUT http://127.0.0.1:8000/changepassword/
    Input
    {
		  "username":"test1@test.com",
		  "oldpassword":"Foo001",
		  "newpassword":"fOO001"		
	  }
    Output
    {
      "token": "446371d3950bd40c9531f72127032f518b105bfe"
    }
5.  PUT http://127.0.0.1:8000/apply/
    Input
    {
		  "email":"test5@test.com",
		  "password":"Foo001"
	  }
    Output HTTP_204_NO_CONTENT
6.  POST http://127.0.0.1:8000/products/
    Input
    {
		  "title":"test Echo",
		  "sku":"Foo007",
		  "price":123.45,
		  "description":"test123",
		  "available": true,
    	"stock": 30
	  }    
    PUT http://127.0.0.1:8000/product/1/
    Input
    {
		  "title":"test Echo",
		  "sku":"Foo007",
		  "price":123.45,
		  "description":"test123",
		  "available": true,
    	"stock": 50
	  }    
    DELETE http://127.0.0.1:8000/product/1/
    Output HTTP_204_NO_CONTENT
7.  POST http://127.0.0.1:8000/orders/
    Input
    {
		  "total":12345,
		  "items":[1, 3]
	  }
    PUT http://127.0.0.1:8000/order/1/
    Input
    {
		  "total":123.45,
		  "items":[3]
	  }
    DELETE http://127.0.0.1:8000/order/1/
    Output HTTP_204_NO_CONTENT
</pre>
