package app

import (
	"database/sql"
	"log"

	_ "github.com/go-sql-driver/mysql"
)

func GetDatabase() *sql.DB {
	username := GetEnv("DB_USERNAME")
	password := GetEnv("DB_PASSWORD")
	host := GetEnv("DB_HOST")
	port := GetEnv("DB_PORT")

	db, err := sql.Open("mysql", username+":"+password+"@tcp("+host+":"+port+")/alertproducer")

	if err != nil {
		log.Fatal(err)
	}

	return db
}

func GetOrCreateVehicle(db *sql.DB, manufacturer string, model string, year string) (Vehicle, error) {
	// Check if vehicle exists
	var vehicle Vehicle
	err := db.QueryRow("SELECT * FROM vehicle WHERE manufacturer_name = ? AND model_name = ? AND model_year = ?", manufacturer, model, year).Scan(&vehicle.ID, &vehicle.Manufacturer, &vehicle.Model, &vehicle.Year, &vehicle.LastRowID, &vehicle.Location)

	if err != nil {
		// Vehicle doesn't exist so create it
		res, err := db.Exec("INSERT INTO vehicle (manufacturer_name, model_name, model_year) VALUES (?, ?, ?)", manufacturer, model, year)
		if err != nil {
			log.Fatal(err)
		}

		// Get the newly created vehicle
		lastId, err := res.LastInsertId()
		if err != nil {
			log.Fatal(err)
		}
		err = db.QueryRow("SELECT * FROM vehicle WHERE id = ?", lastId).Scan(&vehicle.ID, &vehicle.Manufacturer, &vehicle.Model, &vehicle.Year, &vehicle.LastRowID, &vehicle.Location)

		if err != nil {
			log.Fatal(err)
		}

		return vehicle, nil
	}

	return vehicle, nil
}

func GetAllVehicles(db *sql.DB) []Vehicle {
	rows, err := db.Query("SELECT * FROM vehicle")
	if err != nil {
		log.Fatal(err)
	}

	var vehicles []Vehicle
	for rows.Next() {
		var vehicle Vehicle
		err = rows.Scan(&vehicle.ID, &vehicle.Manufacturer, &vehicle.Model, &vehicle.Year, &vehicle.LastRowID, &vehicle.Location)
		if err != nil {
			log.Fatal(err)
		}

		vehicles = append(vehicles, vehicle)
	}

	return vehicles
}

// Updates the last row id and location for a vehicle
func UpdateVehicle(db *sql.DB, vehicle *Vehicle) {
	_, rowIdUpdateErr := db.Exec("UPDATE vehicle SET last_row_id = ? WHERE id = ?", vehicle.LastRowID.String, vehicle.ID)
	if rowIdUpdateErr != nil {
		log.Fatal(rowIdUpdateErr)
	}
	_, locationUpdateErr := db.Exec("UPDATE vehicle SET branch_location = ? WHERE id = ?", vehicle.Location.String, vehicle.ID)
	if locationUpdateErr != nil {
		log.Fatal(locationUpdateErr)
	}
}

func GetAllSubscriptions(db *sql.DB, vehicle *Vehicle) []Subscription {
	rows, err := db.Query("SELECT * FROM subscription WHERE vehicle_id = ?", vehicle.ID)
	if err != nil {
		log.Fatal(err)
	}

	var subscribers []Subscription
	for rows.Next() {
		var subscriber Subscription
		err = rows.Scan(&subscriber.ID, &subscriber.ClientID, &subscriber.VehicleID)
		if err != nil {
			log.Fatal(err)
		}

		subscribers = append(subscribers, subscriber)
	}

	return subscribers
}

func CreateSubscription(db *sql.DB, vehicle *Vehicle, clientID string) (*Subscription, error) {
	res, err := db.Exec("INSERT INTO subscription (client_id, vehicle_id) VALUES (?, ?)", clientID, vehicle.ID)
	if err != nil {
		return nil, err
	}

	lastId, err := res.LastInsertId()
	if err != nil {
		log.Fatal(err)
	}

	var subscriber Subscription
	err = db.QueryRow("SELECT * FROM subscription WHERE id = ?", lastId).Scan(&subscriber.ID, &subscriber.ClientID, &subscriber.VehicleID)

	if err != nil {
		log.Fatal(err)
	}

	return &subscriber, nil
}

func DeleteSubscription(db *sql.DB, vehicle *Vehicle, clientId string) {
	_, err := db.Exec("DELETE FROM subscription WHERE client_id = ? AND vehicle_id = ?", clientId, vehicle.ID)
	if err != nil {
		log.Fatal(err)
	}

	return
}
