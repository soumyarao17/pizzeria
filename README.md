
Demo Screenshots attatched -
----------------------------
1. ![img.png](img.png)
2. ![img_2.png](img_2.png)
3. ![img_4.png](img_4.png)
4. ![img_3.png](img_3.png)
5. ![img_5.png](img_5.png)
6. ![img_6.png](img_6.png)



Code flow AND TESTS -
----------------------
1. app/views.py -> Viewset for create and get order status
2. app/tasks.py -> Background tasks to schedule order status changes based on time. Also to print/log it.
3. app/models.py -> Pizza and Order models with validations
4. app/tests/test_create_status.py -> Test to check creation of order along with validations for invalid ones
5. app/tests/test_create_status.py -> Test change of order status after creation


Execution Setup -
-----------------


1. Download and extract the zip file.

2. Download and install MySQL or install via Terminal - brew install mysql

3. Start MySQL server: brew services start mysql

4. (Optional) Set MySQL Password, MySQL Root Password

5. Install Docker and start docker daemon

6. Host MySQL server on Docker container and expose it to the port 3306. Use commands - <br />
(Ensure you are in the project home directory)<br />
Build - docker build -f docker/db/Dockerfile -t pizzeria_db .<br />
Run - docker run --network=host -it --expose 3306 -p 3306:3306 pizzeria_db<br />

7. MySQL server is now hosted which automatically created database "pizeria_db"
(If you have setup MySQL Root Password, update the Dockerfile accordingly)

8. Build and run docker for pizzeria app apis and tasks:<br />
Build - docker build -f docker/apis/Dockerfile -t pizzeria_apis_tasks .       <br />
Run - docker run --network=host -it --expose 8000 -p 8000:8000 pizzeria_apis_tasks     <br />

9. Open Docker Desktop and run a terminal in pizzeria_apis_tasks container
								<br /> OR <br />
	docker images | grep pizzeria_apis_tasks # Copy id     <br />
	docker run -i -t <id> /bin/bash      <br />

10. Run migrations and run the server: <br />
	python manage.py makemigrations   <br />
	python manage.py migrate   <br />
	python manage.py runserver 8000   <br />

11. Similary open another terminal to run process_tasks (background tasks): <br />
	python manage.py process_tasks <br />

12. Testing:
Open another terminal in pizzeria_apis_tasks container <br />
    - Api request to Create order: <br />
    curl -X POST 127.0.0.1:8000/create_order/ -d '{"pizzas": [{"name": "Pizza 1", "base": "thin-crust", "cheese": "mozzarella", "toppings": ["pepperoni", "mushrooms", "bell-peppers", "olives", "onions"]}, {"name": "Pizza 2", "base": "normal", "cheese": "cheddar", "toppings": ["pepperoni", "tomatoes", "bell-peppers", "olives", "sausage"]}]}'
    <br />
     Curl O/P: {
                 "order_id": 1
           } <br />
     Postman Output Screenshot -> ![img.png](img.png) <br /> <br />
   

   - Api request to Fetch order details: <br />
   curl -L -X GET 127.0.0.1:8000/get_order_status/1 <br />
   Curl O/P: {
			    "order_id": 1,
			    "order_status": "Delivered"
		  } <br />
   Postman Output Screenshot -> ![img_2.png](img_2.png) <br /> <br />

   - Api request to create invalid order: <br />
   curl -X POST 127.0.0.1:8000/create_order/ -d '{"pizzas": [{"name": "Pizza 1", "base": "thin-crust", "cheese": "mozzarella", "toppings": ["pepperoni", "mushrooms", "bell-peppers", "olives", "onions"]}, {"name": "Pizza 2", "base": "normal", "cheese": "cheddar", "toppings": ["pepperoni", "tomatoes", "bell-peppers", "olives"]}]}'
      <br />
   Curl O/P: {			
                "error": "You must select 5 toppings."
          } <br />
   Postman Output Screenshot -> ![img_4.png](img_4.png) <br /> <br />

   - Log screenshot of the background tasks <br />
	 Format : Orderid Status Time <br />
	 	- Displays how status change after 0, 1, 3 and 5 minutes <br />
	 Output Screenshot -> ![img_3.png](img_3.png) <br />

