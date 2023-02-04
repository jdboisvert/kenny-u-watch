package app

import (
	"bytes"
	"encoding/json"
	"log"
	"net/http"
	"time"

	kennyupull "github.com/jdboisvert/kenny-u-pull-go-sdk"
)

func CheckVehiclesListings() {
	log.Println("Checking for new vehicles to alert on...")
	vehiclesToSearchFor := GetAllVehicles()
	for _, vehicle := range vehiclesToSearchFor {
		go CheckForNewVehiclesPosted(vehicle)
	}
}

func CheckForNewVehiclesPosted(vehicle Vehicle) {
	log.Println("Checking for new vehicles posted for vehicle: ", vehicle)
	inventorySearch := kennyupull.InventorySearch{
		Year:  vehicle.Year,
		Make:  vehicle.Manufacturer,
		Model: vehicle.Model,
	}
	latestListing, err := kennyupull.GetLatestListing(inventorySearch)

	if err != nil {
		log.Println("Got an error when trying to get inventory listings: ", err)
	}
	if latestListing == nil {
		log.Println("No listings found for vehicle: ", vehicle)
		return
	}

	now := time.Now()
	currentDate := now.Format("2006-01-02") // Listing date format is YYYY-MM-DD

	hasYetToBeCheck := !vehicle.LastRowID.Valid && !vehicle.Location.Valid
	doesNotMatchRecordInDatabase := hasYetToBeCheck || (vehicle.LastRowID.String != latestListing.RowID || vehicle.Location.String != latestListing.Branch)

	if latestListing.DateListed == currentDate && doesNotMatchRecordInDatabase {
		// New listing found for today for the vehicle that we haven't seen before so send an alert
		log.Println("New listing found for vehicle: ", vehicle, " and the listing is: ", latestListing)
		go SendUpdateToSubscribers(latestListing, &vehicle)

		// Update the vehicle with the latest listing info
		vehicle.LastRowID.String = latestListing.RowID
		vehicle.Location.String = latestListing.Branch
		UpdateVehicle(&vehicle)
	}
}

func SendUpdateToSubscribers(latestListing *kennyupull.InventoryListing, vehicle *Vehicle) {
	allSubscribers := GetAllSubscriptions(vehicle)

	for _, subscriber := range allSubscribers {
		go SendUpdateToASubscriber(latestListing, &subscriber)
	}
}

func SendUpdateToASubscriber(latestListing *kennyupull.InventoryListing, subscriber *Subscription) {
	values := map[string]string{"year": latestListing.Year, "make": latestListing.Make, "model": latestListing.Model, "date_listed": latestListing.DateListed, "row_id": latestListing.RowID, "branch": latestListing.Branch, "listing_url": latestListing.ListingUrl, "client_id": subscriber.ClientID}
	json_data, err := json.Marshal(values)

	if err != nil {
		log.Fatal(err)
	}

	// TODO move to env var or config file and need retry logic for alerting via exponential backoff.
	resp, err := http.Post("http://localhost:8000/listing-consumer/v1/new-listing", "application/json",
		bytes.NewBuffer(json_data))

	if err != nil {
		log.Println("Got an error when trying to send an alert: ", err)
		return // TODO need retry logic for alerting via exponential backoff.
	}

	if resp.StatusCode != http.StatusNoContent {
		log.Println("Got a non-204 status code from the alert consumer when trying to send an alert: ", resp.StatusCode)
	}

	defer resp.Body.Close()
}

func SubscribeToVehicle(vehicleSubscription *VehicleSubscription) (*Subscription, error) {
	vehicle, err := GetOrCreateVehicle(vehicleSubscription.Manufacturer, vehicleSubscription.Model, vehicleSubscription.Year)

	if err != nil {
		log.Println("Got an error when trying to get or create vehicle: ", err)
		return nil, err
	}

	subscription, err := CreateSubscription(&vehicle, vehicleSubscription.ClientID)

	return subscription, err
}

func UnsubscribeFromVehicle(vehicleSubscription *VehicleSubscription) {
	vehicle, err := GetOrCreateVehicle(vehicleSubscription.Manufacturer, vehicleSubscription.Model, vehicleSubscription.Year)

	if err != nil {
		log.Println("Got an error when trying to get or create vehicle: ", err)
		return
	}

	DeleteSubscription(&vehicle, vehicleSubscription.ClientID)
}
