package main

import (
	"log"
	"net/http"
	"strconv"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/go-co-op/gocron"
	app "github.com/jdboisvert/kenny-u-watch/alert-producer/app"
)

func subscribeToVehicle(c *gin.Context) {
	var newVehicle app.VehicleSubscription
	if err := c.BindJSON(&newVehicle); err != nil {
		return
	}

	_, err := app.SubscribeToVehicle(&newVehicle)

	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Error subscribing to vehicle"})
		return
	}

	c.IndentedJSON(http.StatusCreated, newVehicle)
}

func unsubscribeToVehicle(c *gin.Context) {
	var vehicleToUnsubscribeFrom app.VehicleSubscription
	if err := c.BindJSON(&vehicleToUnsubscribeFrom); err != nil {
		return
	}

	app.UnsubscribeFromVehicle(&vehicleToUnsubscribeFrom)

	c.IndentedJSON(http.StatusOK, vehicleToUnsubscribeFrom)
}

func main() {
	router := gin.Default()
	router.POST("/v1/subscribe-vehicle", subscribeToVehicle)
	router.DELETE("/v1/unsubscribe-from-vehicle", unsubscribeToVehicle)

	app.LoadEnv()

	numberOfMinutesToCheckForNewListingsEnv := app.GetEnv("NUMBER_OF_MINUTES_TO_CHECK_FOR_NEW_LISTINGS")
	numberOfMinutesToCheckForNewListings, err := strconv.Atoi(numberOfMinutesToCheckForNewListingsEnv)
	if err != nil {
		log.Fatal("Error parsing NUMBER_OF_MINUTES_TO_CHECK_FOR_NEW_LISTINGS env variable: ", err)
	}

	s := gocron.NewScheduler(time.UTC)
	log.Println("Checking for new listings every ", numberOfMinutesToCheckForNewListings, " minutes")
	s.Every(numberOfMinutesToCheckForNewListings).Minutes().Do(func() {
		app.CheckVehiclesListings()
	})
	s.StartAsync()

	router.Run("localhost:8080")
}
