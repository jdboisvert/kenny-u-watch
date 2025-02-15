<p align="center">
  <img src="https://github.com/jdboisvert/kenny-u-watch/blob/main/docs/images/logo.png?raw=true" height="250">
</p>

An application to make it possible to watch Kenny U-Pull's [vehicle inventory](https://kennyupull.com/auto-parts/our-inventory/) easily via alerts you can create, and delete at anytime.

Get an email whenever a car you are watching is posted to the inventory page. This is an re-imagining of Kenny U-Pull's "[Alert me](https://kennyupull.com/alert-me/)" product.

Note this is an unofficial product and is not affiliated with Kenny U-Pull.

# Main Features
- Create, and delete alerts for vehicles you want to watch on Kenny U-Pull's inventory page.
- Get an email whenever a vehicle you are watching is posted to the inventory page.
- Admin portal to view all the alerts created by all users.
- Handle multiple users with their own username and password.
- Fully bilingual (English and French) support.

# Want to try it out?

Follow the [Quick Start](https://github.com/jdboisvert/kenny-u-watch/tree/main/docs/quick_start.en.md) tutorial to get everything up and running on your machine!

## Sneak peek
![Demo of app](./docs/videos/dashboard_demo.gif)

## How to use the APIs
You can import the Postman collection from the root of this project and use it to test the application.

# About this repository
This repository contains the code for the Kenny U-Watch application and is formatted to be a monorepo however each application is independent in their own sub directories. Everything can be found here to run the full application.

### User Watch Management (user_watch_management)
This application allows users to create, update, and delete alerts. An alert is a vehicle make, model, and year that the user wants to be alerted about. The user can create a watch by providing the make, model, and year of the vehicle they want to watch. The user can also update and delete watches they have created. The user can also view all the watches they have created.

This repository contains the backend code that interacts with a frontend and is meant to be user facing. It also contains the admin portal functionality that allows admins to view all the watches created by all users. Please read the [README](https://github.com/jdboisvert/kenny-u-watch/tree/main/user_watch_management#readme) section for more information about the application and how to get it running.

### Alert Producer (alert-producer)
This application is responsible for producing alerts to the user. It is meant to be run as a cron job. It will check the inventory page for new vehicles and send an email an alert to all subscribers about the given vehicle (in this case to the User Watch Management system). Please read the [README](https://github.com/jdboisvert/kenny-u-watch/tree/main/alert-producer#readme) section for more information about the application and how to get it running.

### Kenny U-Watch Web App (kenny-u-watch-web-app)
This application is responsible for handling the UI to interact with the alerts and authentication with the API servers. This can be accessed in your browser.
