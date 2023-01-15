# Kenny U-Watch
An application to make it possible to watch Kenny U-Pull's [vehicle inventory](https://kennyupull.com/auto-parts/our-inventory/) easily via alerts you can create, update, and delete at anytime. Get an email whenever a car you are watching is posted to the inventory page. This is an re-imagining of Kenny U-Pull's "[Alert me](https://kennyupull.com/alert-me/)" product.


## About this repository
This repository contains the backend code for the Kenny U-Watch application and is formatted to be a monorepo however each application is independent.


## User Watch Management
This application allows users to create, update, and delete alerts. An alert is a vehicle make, model, and year that the user wants to be alerted about. The user can create a watch by providing the make, model, and year of the vehicle they want to watch. The user can also update and delete watches they have created. The user can also view all the watches they have created.

This repository contains the backend code that interacts with a frontend and is meant to be user facing. It also contains the admin portal functionality that allows admins to view all the watches created by all users. Please read the [README](https://github.com/jdboisvert/kenny-u-watch/tree/main/user_watch_management#readme) section for more information about the application and how to get it running.

## Alert Producer
This application is responsible for producing alerts to the user. It is meant to be run as a cron job. It will check the inventory page for new vehicles and send an email an alert to all subscribers about the given vehicle (in this case to the User Watch Management system). Please read the [README](https://github.com/jdboisvert/kenny-u-watch/tree/main/alert-producer#readme) section for more information about the application and how to get it running.
