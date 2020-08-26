# Modelling the Spread of COVID-19 using an SEIR Model

# Instructions to deploy this project on an EC2 instance

1. Launch a new instance

2. Select a ubuntu 18.04 VM and a t2 microinstance

3. Configure a security group that allows you to SSH into the instance and set up port 80 to enable HTTP requests

4. Launch the instance and SSH into the instance

5. Install nodejs 10.x from Nodesource
   ```
   curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
   sudo apt-get install -y nodejs
   ```
6. Install python's package manager, pip

   `sudo apt-get install -y python3-pip`
  
7. Install the nodejs production process manager
   ```
   sudo npm install -g pm2
   sudo pm2 startup systemd
   ```
8. Install nginx
   `sudo apt-get install -y nginx`
   
9. Clone this repository
   `sudo git clone https://github.com/CheranMahalingam/COVID-19_Projections_SEIR_Model.git`
   
10. Install the flask backend dependencies
    ```
    cd COVID-19_Projections_SEIR_Model/api
    sudo pip3 install --user -r requirements.txt
    ```
11. Manually install scrapy
    `sudo pip3 uninstall scrapy && sudo pip3 install scrapy`

12. Start the production process manager
    `sudo pm2 start application.py --interpreter=python3`
   
13. Install the react frontend dependencies and run the frontend build
   ```
    cd ../covid-projections
    sudo npm install
    sudo npm run build
   ```
14. Create a custom Nginx configuration
    `sudo rm /etc/nginx/sites-available/default`
    `sudo nano /etc/nginx/sites-available/default`
    Copy the following into the text editor
    ```
    server {
      listen 80;
      server_name _;
      
      location / {
        root /home/ubuntu/COVID-19_Projections_SEIR_Model/covid-projections/build;
        try_files $uri $uri/ /index.html;
      }
      
      location http://localhost:5000 {
        proxy_pass http://localhost:5000;
      }
    }
    ```
15. Restart Nginx
    `sudo systemctl restart nginx`
    
16. Copy the IPv4 or DNS address into the browser to run the fullstack application

# Instructions to run locally

1. Open the terminal and cd into the covid-projections directory

   `cd *****/COVID-19_Projections_SEIR_Model/covid-projections`

2. Install dependencies using npm

   `npm install`

3. Install dependencies using pip

   ```
   cd ../api
   pip3 install -r requirements.txt
   ```

4. To run the flask backend use,

   `flask run`

5. Open a new terminal and cd into the covid-projections directory

   `cd *****/COVID-19_Projections_SEIR_Model/covid-projections`

6. To run the web application use,

   `npm start`

7. The program will open on port 3000 and is available at http://localhost:3000

# SEIR Model

The model splits the population into four groups. Susceptible (people who are not immune
to infection), Exposed (people who have been infected but are yet to become infectious),
Infected (people who can spread the disease), Recovered (people who are immune).
The population of each group can be approximated using the following differential
equations:

<p align="center">
  <img src="images/SEIR_differential_equations.png">
</p>
