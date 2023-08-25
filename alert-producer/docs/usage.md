# Usage
This server supports both subscribing and unsubscribing to alerts.

To subscribe, send a POST request to the `/v1/subscribe-vehicle` endpoint with the following body as an example:

    {
        "manufacturer": "Lexus",
        "model": "IS-250",
        "year": "2010",
        "client_id": "1234"
    }

To unsubscribe, send a POST request to the `/v1/unsubscribe-from-vehicle` endpoint with the following body as an example:

    {
        "manufacturer": "Lexus",
        "model": "IS-250",
        "year": "2010",
        "client_id": "1234"
    }

In the root of this project you can find a postman collection to import and use for local testing.

This project also runs a cron job which will check the inventory page for new vehicles and send all subscribers an update about the new listing.
