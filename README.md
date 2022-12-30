# Chemistry
Chemical Reaction Calculator

A django application to calculate elementary chemical reactions (a chemical reaction that has only a single transition state),
whose input is the desired reaction and the amount of final product and the output is the amount of reagents and total cost 
(based on registered stores on database). It is possible to add new compounds, new reactions and new avaiable stores using the API
as well.
The application was deployed on AWS EC2 instance, using Nginx and Gunicorn. You can try it out using EC2 IP adress: http://18.231.30.103. 
For now, the deploy is happening manually, but I am studying a bit more to understand how to create a domain with certbot to finish my deploy
automation.
