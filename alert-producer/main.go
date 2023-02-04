package main

import (
	"net/http"
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

	s := gocron.NewScheduler(time.UTC)
	s.Every(1).Minutes().Do(func() {
		// TODO move to env var or config file for number of minutes to check for new listings
		app.CheckVehiclesListings()
	})
	s.StartAsync()

	router.Run("localhost:8080") // TODO move to env var or config file
}
