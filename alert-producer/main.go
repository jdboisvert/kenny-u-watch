package main

import (
	"net/http"
	"reflect"

	"github.com/gin-gonic/gin"
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

func subscribeToVehicle(c *gin.Context) {
	var newVehicle Vehicle

	// Call BindJSON to bind the received JSON to
	// newAlbum.
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
}
