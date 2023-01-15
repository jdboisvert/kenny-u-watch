package main

import (
	"bytes"
	"encoding/json"
	"log"
	"net/http"
	"reflect"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/go-co-op/gocron"
	kennyupull "github.com/jdboisvert/kenny-u-pull-go-sdk"
)

type Vehicle struct {
	Year  string `json:"year"`
	Make  string `json:"make"`
	Model string `json:"model"`
}

// TODO a temp datastore in memory for now to test. To eventually be moved to proper datastore.
var vehiclesToSearchFor = []Vehicle{}

func vehicleAlreadySubscribed(vehiclesToSearchFor []Vehicle, vehicleToAdd Vehicle) bool {
	for _, vehicle := range vehiclesToSearchFor {
		if reflect.DeepEqual(vehicle, vehicleToAdd) {
			return true
		}
	}

	return false
}

func checkVehiclesListings() {
	// TODO call the API and check for new vehicles
	log.Println("Checking for new vehicles to alert on...")
	for _, vehicle := range vehiclesToSearchFor {
		go checkForNewVehiclesPosted(vehicle)
	}
}

func checkForNewVehiclesPosted(vehicle Vehicle) {
	// TODO call the API and check for new vehicles

	// TODO if new vehicles are found, send an alert to the alert consumer
	inventorySearch := kennyupull.InventorySearch{
		Year:  vehicle.Year,
		Make:  vehicle.Make,
		Model: vehicle.Model,
	}
	// TODO make use of GetLatestInventoryListing function which will be reviewed and merged into the SDK shortly https://github.com/jdboisvert/kenny-u-pull-go-sdk/pull/4
	inventoryListings, err := kennyupull.GetInventory(inventorySearch)
	if err != nil {
		log.Println("Got an error when trying to get inventory listings: ", err)
	}

	log.Println("Got inventory listings: ", inventoryListings)
	latestListing := inventoryListings[0]
	log.Println("Latest listing: ", latestListing)

	layout := "02-01-2006"
	currentDate := time.Now()
	listingTimestamp, _ := time.Parse(layout, latestListing.DateListed)

	// TODO this needs to be smarter and handle the case where a new listing is posted multiple times a day
	if listingTimestamp == currentDate {
		// New listing found for today for the vehicle
		log.Println("New listing found for vehicle: ", vehicle)
		sendUpdateToSubscriber(latestListing)
	}
}

func sendUpdateToSubscriber(latestListing kennyupull.InventoryListing) {
	values := map[string]string{"year": latestListing.Year, "make": latestListing.Make, "model": latestListing.Model, "date_listed": latestListing.DateListed, "row_id": latestListing.RowID, "branch": latestListing.Branch, "listing_url": latestListing.ListingUrl}
	json_data, err := json.Marshal(values)

	if err != nil {
		log.Fatal(err)
	}

	// TODO move to env var or config file and need retry logic for alerting via exponential backoff.
	resp, err := http.Post("localhost:8080/v1/new-listing-consumer", "application/json",
		bytes.NewBuffer(json_data))

	if err != nil {
		log.Fatal(err)
	}

	if resp.StatusCode != http.StatusOK {
		log.Fatal("Got a non-200 status code from the alert consumer")
	}

	defer resp.Body.Close()
}

func subscribeToVehicle(c *gin.Context) {
	var newVehicle Vehicle
	if err := c.BindJSON(&newVehicle); err != nil {
		return
	}

	if !vehicleAlreadySubscribed(vehiclesToSearchFor, newVehicle) {
		// Only add the vehicle if it's not already subscribed
		vehiclesToSearchFor = append(vehiclesToSearchFor, newVehicle)
	}

	c.IndentedJSON(http.StatusCreated, newVehicle)
}

func main() {
	router := gin.Default()
	router.POST("/v1/subscribe-vehicle", subscribeToVehicle)

	router.Run("localhost:8080") // TODO move to env var or config file

	// TODO move to a separate file
	// Run the scheduler to poll the API every 30 minutes
	s := gocron.NewScheduler(time.UTC)

	// For testing purposes, run every minute
	s.Every(1).Minutes().Do(func() {
		checkVehiclesListings()
	})
	s.StartAsync()
}
