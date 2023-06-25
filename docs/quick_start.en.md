# Quick Start

This tutorial goes over how to get the application running locally for personal simple use. As long as it runs you will be able to get alerts whenever a new listing is found and the application leverages Docker to be able to run the services on any machine that supports Docker.

# Prerequistes
- Ensure to have Docker installed.
- Have an SMPT mail server set up to use (We will use gmail in this tutorial)

# How to install Docker
TODO

# How to get emails
This application will send out an email to the account's email whenever a new posting is found. In this tutorial we will be using Gmail however you are free to use another mailing service of your choice.

## Set up your email account

TODO

## Set up environment variables

Run the following commands in a terminal. Ensure to replace your `<username>` and `<password>` with your username and password.

### Linux/MacOS
```bash
export EMAIL_HOST_USER=<username>
export EMAIL_HOST_PASSWORD=<password>
export EMAIL_HOST="smtp.gmail.com"
export EMAIL_PORT=587
```

### Windows
TODO


# How to run

1. Run the command `docker compose build`. You will know this has ran successfully if you see an output similar to below

2. Run `docker compose up`. You should see something similar to below once everything is up and working.

3. Open your web browser and navigate to `http://localhost:3000/signup`. This is where the web app is hosted
- Note it is possible the app is not loaded yet and is still starting up. If you do not see any page yet just wait a bit and try again.

4. You should now see the following screen and be ready to start creating alerts!

# Creating your first alert

1. First make your account by providing an email you wish to get alerts on and a password that only you will know.

2. Now navigate to `http://localhost:3000/login` and login with the same email and password provided above. You should be brought to the main dashboard.

3. In the top right corner click on Create an Alert or simply navigate to `http://localhost:3000/create-alert`. This is where you will enter the details fo the vehicle you wish to be alerted on. In this tutorial we will be creating an alert for a Honda Civic 2007 but note this can be used for any vehicle.

4. For `Manufacturer` enter `Honda`, for `Model` enter `Civic`, and for `Year` enter `2007`. Then click on the `Create Alert` button. You should then be brought back to the dashboard and your new alert has been created!

5. Keep an eye on your email to see if you get an alert. By default this application checks for postings every minute. You should get an email similar to the one shown below which will link you to the Kenny U-Pull website.

6. Congrats! Your Kenny U Pull browsing is now automated so you can have that little edge over other people looking for parts :)!

7. Optional: Not required but I would love to hear what you think feel free to email me at [info.jeffreyboisvert@gmail.com](mailto:info.jeffreyboisvert@gmail.com)!

# Modifying/Deleting an alert

You cannot modify an alert the only way to modify it is to delete it and make a new one.
Each alert has a `Delete` button which will be used to delete the alert from the system.
