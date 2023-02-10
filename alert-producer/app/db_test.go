package app

import (
	"database/sql"
	"errors"
	"testing"

	"github.com/DATA-DOG/go-sqlmock"
)

func TestGetOrCreateVehicle_ReturnWhenExists(t *testing.T) {
	// configure to use case sensitive SQL query matcher
	// instead of default regular expression matcher
	db, mock, err := sqlmock.New(sqlmock.QueryMatcherOption(sqlmock.QueryMatcherEqual))
	if err != nil {
		t.Fatalf("an error '%s' was not expected when opening a stub database connection", err)
	}
	defer db.Close()

	rows := sqlmock.NewRows([]string{"id", "manufacturer_name", "model_name", "model_year", "last_row_id", "branch_location"}).AddRow(1, "Ford", "F-150", "2018", "E27", "Ottawa")

	mock.ExpectQuery("SELECT * FROM vehicle WHERE manufacturer_name = ? AND model_name = ? AND model_year = ?").WithArgs("Ford", "F-150", "2018").WillReturnRows(rows)

	vehicle, err := GetOrCreateVehicle(db, "Ford", "F-150", "2018")

	if err != nil {
		t.Errorf("Expected no error, got %s", err)
	}

	if vehicle.ID != 1 {
		t.Errorf("Expected vehicle ID to be 1, got %d", vehicle.ID)
	}

	if vehicle.Manufacturer != "Ford" {
		t.Errorf("Expected vehicle manufacturer to be Ford, got %s", vehicle.Manufacturer)
	}

	if vehicle.Model != "F-150" {
		t.Errorf("Expected vehicle model to be F-150, got %s", vehicle.Model)
	}

	if vehicle.Year != "2018" {
		t.Errorf("Expected vehicle year to be 2018, got %s", vehicle.Year)
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("there were unfulfilled expectations: %s", err)
	}
}

func TestGetOrCreateVehicle_CreateWhenDoesNotExist(t *testing.T) {
	// configure to use case sensitive SQL query matcher
	// instead of default regular expression matcher
	db, mock, err := sqlmock.New(sqlmock.QueryMatcherOption(sqlmock.QueryMatcherEqual))
	if err != nil {
		t.Fatalf("an error '%s' was not expected when opening a stub database connection", err)
	}
	defer db.Close()

	emptyRows := sqlmock.NewRows([]string{"id", "manufacturer_name", "model_name", "model_year", "last_row_id", "branch_location"})

	mock.ExpectQuery("SELECT * FROM vehicle WHERE manufacturer_name = ? AND model_name = ? AND model_year = ?").WithArgs("Ford", "F-150", "2018").WillReturnRows(emptyRows)
	mock.ExpectExec("INSERT INTO vehicle (manufacturer_name, model_name, model_year) VALUES (?, ?, ?)").WithArgs("Ford", "F-150", "2018").WillReturnResult(sqlmock.NewResult(1, 1))

	actualRows := sqlmock.NewRows([]string{"id", "manufacturer_name", "model_name", "model_year", "last_row_id", "branch_location"}).AddRow(1, "Ford", "F-150", "2018", "E27", "Ottawa")
	mock.ExpectQuery("SELECT * FROM vehicle WHERE id = ?").WithArgs(1).WillReturnRows(actualRows)

	vehicle, err := GetOrCreateVehicle(db, "Ford", "F-150", "2018")

	if err != nil {
		t.Errorf("Expected no error, got %s", err)
	}

	if vehicle.ID != 1 {
		t.Errorf("Expected vehicle ID to be 1, got %d", vehicle.ID)
	}

	if vehicle.Manufacturer != "Ford" {
		t.Errorf("Expected vehicle manufacturer to be Ford, got %s", vehicle.Manufacturer)
	}

	if vehicle.Model != "F-150" {
		t.Errorf("Expected vehicle model to be F-150, got %s", vehicle.Model)
	}

	if vehicle.Year != "2018" {
		t.Errorf("Expected vehicle year to be 2018, got %s", vehicle.Year)
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("there were unfulfilled expectations: %s", err)
	}
}

func TestGetAllVehicles_NoVehiclesFound(t *testing.T) {
	// configure to use case sensitive SQL query matcher
	// instead of default regular expression matcher
	db, mock, err := sqlmock.New(sqlmock.QueryMatcherOption(sqlmock.QueryMatcherEqual))
	if err != nil {
		t.Fatalf("an error '%s' was not expected when opening a stub database connection", err)
	}
	defer db.Close()

	emptyRows := sqlmock.NewRows([]string{"id", "manufacturer_name", "model_name", "model_year", "last_row_id", "branch_location"})

	mock.ExpectQuery("SELECT * FROM vehicle").WillReturnRows(emptyRows)

	vehicles := GetAllVehicles(db)

	if len(vehicles) != 0 {
		t.Errorf("Expected no vehicles, got %d", len(vehicles))
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("there were unfulfilled expectations: %s", err)
	}
}

func TestGetAllVehicles_VehiclesFound(t *testing.T) {
	// configure to use case sensitive SQL query matcher
	// instead of default regular expression matcher
	db, mock, err := sqlmock.New(sqlmock.QueryMatcherOption(sqlmock.QueryMatcherEqual))
	if err != nil {
		t.Fatalf("an error '%s' was not expected when opening a stub database connection", err)
	}
	defer db.Close()

	rows := sqlmock.NewRows([]string{"id", "manufacturer_name", "model_name", "model_year", "last_row_id", "branch_location"}).AddRow(1, "Ford", "F-150", "2018", "E27", "Ottawa").AddRow(2, "Lexus", "IS-250", "2016", "E26", "Cornwall")

	mock.ExpectQuery("SELECT * FROM vehicle").WillReturnRows(rows)

	vehicles := GetAllVehicles(db)

	if len(vehicles) != 2 {
		t.Errorf("Expected 2 vehicles, got %d", len(vehicles))
	}

	if vehicles[0].ID != 1 {
		t.Errorf("Expected vehicle ID to be 1, got %d", vehicles[0].ID)
	}

	if vehicles[0].Manufacturer != "Ford" {
		t.Errorf("Expected vehicle manufacturer to be Ford, got %s", vehicles[0].Manufacturer)
	}

	if vehicles[0].Model != "F-150" {
		t.Errorf("Expected vehicle model to be F-150, got %s", vehicles[0].Model)
	}

	if vehicles[0].Year != "2018" {
		t.Errorf("Expected vehicle year to be 2018, got %s", vehicles[0].Year)
	}

	if vehicles[0].LastRowID.String != "E27" {
		t.Errorf("Expected vehicle last row ID to be E27, got %s", vehicles[0].LastRowID.String)
	}

	if vehicles[0].Location.String != "Ottawa" {
		t.Errorf("Expected vehicle branch location to be Ottawa, got %s", vehicles[0].Location.String)
	}

	if vehicles[1].ID != 2 {
		t.Errorf("Expected vehicle ID to be 2, got %d", vehicles[1].ID)
	}

	if vehicles[1].Manufacturer != "Lexus" {
		t.Errorf("Expected vehicle manufacturer to be Lexus, got %s", vehicles[1].Manufacturer)
	}

	if vehicles[1].Model != "IS-250" {
		t.Errorf("Expected vehicle model to be IS-250, got %s", vehicles[1].Model)
	}

	if vehicles[1].Year != "2016" {
		t.Errorf("Expected vehicle year to be 2016, got %s", vehicles[1].Year)
	}

	if vehicles[1].LastRowID.String != "E26" {
		t.Errorf("Expected vehicle last row ID to be E26, got %s", vehicles[1].LastRowID.String)
	}

	if vehicles[1].Location.String != "Cornwall" {
		t.Errorf("Expected vehicle branch location to be Cornwall, got %s", vehicles[1].Location.String)
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("there were unfulfilled expectations: %s", err)
	}

}

func TestGetAllVehicles_Error(t *testing.T) {
	// configure to use case sensitive SQL query matcher
	// instead of default regular expression matcher
	db, mock, err := sqlmock.New(sqlmock.QueryMatcherOption(sqlmock.QueryMatcherEqual))
	if err != nil {
		t.Fatalf("an error '%s' was not expected when opening a stub database connection", err)
	}
	defer db.Close()

	mock.ExpectQuery("SELECT * FROM vehicle").WillReturnError(errors.New("error"))

	vehicles := GetAllVehicles(db)

	if len(vehicles) != 0 {
		t.Errorf("Expected no vehicles, got %d", len(vehicles))
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("there were unfulfilled expectations: %s", err)
	}
}

func TestUpdateVehicle_UpdateCorrectly(t *testing.T) {
	// configure to use case sensitive SQL query matcher
	// instead of default regular expression matcher
	db, mock, err := sqlmock.New(sqlmock.QueryMatcherOption(sqlmock.QueryMatcherEqual))
	if err != nil {
		t.Fatalf("an error '%s' was not expected when opening a stub database connection", err)
	}
	defer db.Close()

	mock.ExpectExec("UPDATE vehicle SET last_row_id = ?, branch_location = ? WHERE id = ?").WithArgs("E27", "Ottawa", 1).WillReturnResult(sqlmock.NewResult(1, 1))

	vehicle := Vehicle{ID: 1, Manufacturer: "Toyota", Model: "Corolla", Year: "1996", LastRowID: sql.NullString{String: "E27", Valid: true}, Location: sql.NullString{String: "Ottawa", Valid: true}}
	UpdateVehicle(db, &vehicle)

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("there were unfulfilled expectations: %s", err)
	}
}

func TestUpdateVehicle_Error(t *testing.T) {
	// configure to use case sensitive SQL query matcher
	// instead of default regular expression matcher
	db, mock, err := sqlmock.New(sqlmock.QueryMatcherOption(sqlmock.QueryMatcherEqual))
	if err != nil {
		t.Fatalf("an error '%s' was not expected when opening a stub database connection", err)
	}
	defer db.Close()

	mock.ExpectExec("UPDATE vehicle SET last_row_id = ?, branch_location = ? WHERE id = ?").WithArgs("E27", "Ottawa", 1).WillReturnError(errors.New("error"))

	vehicle := Vehicle{ID: 1, Manufacturer: "Toyota", Model: "Corolla", Year: "1996", LastRowID: sql.NullString{String: "E27", Valid: true}, Location: sql.NullString{String: "Ottawa", Valid: true}}

	// Expects it to simply not crash.
	UpdateVehicle(db, &vehicle)

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("there were unfulfilled expectations: %s", err)
	}
}

func TestGetAllSubscriptions_NoSubscriptionsFound(t *testing.T) {
	// configure to use case sensitive SQL query matcher
	// instead of default regular expression matcher
	db, mock, err := sqlmock.New(sqlmock.QueryMatcherOption(sqlmock.QueryMatcherEqual))
	if err != nil {
		t.Fatalf("an error '%s' was not expected when opening a stub database connection", err)
	}
	defer db.Close()

	mock.ExpectQuery("SELECT id, client_id, vehicle_id FROM subscription WHERE vehicle_id = ?").WithArgs(1).WillReturnRows(sqlmock.NewRows([]string{"id", "vehicle_id", "client_id"}))

	vehicle := Vehicle{ID: 1, Manufacturer: "Toyota", Model: "Corolla", Year: "1996", LastRowID: sql.NullString{String: "E27", Valid: true}, Location: sql.NullString{String: "Ottawa", Valid: true}}
	subscriptions := GetAllSubscriptions(db, &vehicle)

	if len(subscriptions) != 0 {
		t.Errorf("Expected no subscriptions, got %d", len(subscriptions))
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("there were unfulfilled expectations: %s", err)
	}
}

func TestGetAllSubscriptions_SubscriptionsFound(t *testing.T) {
	// configure to use case sensitive SQL query matcher
	// instead of default regular expression matcher
	db, mock, err := sqlmock.New(sqlmock.QueryMatcherOption(sqlmock.QueryMatcherEqual))
	if err != nil {
		t.Fatalf("an error '%s' was not expected when opening a stub database connection", err)
	}
	defer db.Close()

	rows := sqlmock.NewRows([]string{"id", "client_id", "vehicle_id"}).AddRow(1, "client_id_1", 1).AddRow(2, "client_id_2", 1)

	mock.ExpectQuery("SELECT id, client_id, vehicle_id FROM subscription WHERE vehicle_id = ?").WithArgs(1).WillReturnRows(rows)

	vehicle := Vehicle{ID: 1, Manufacturer: "Toyota", Model: "Corolla", Year: "1996", LastRowID: sql.NullString{String: "E27", Valid: true}, Location: sql.NullString{String: "Ottawa", Valid: true}}
	subscriptions := GetAllSubscriptions(db, &vehicle)

	if len(subscriptions) != 2 {
		t.Errorf("Expected 2 subscriptions, got %d", len(subscriptions))
	}

	if subscriptions[0].ID != 1 {
		t.Errorf("Expected subscription ID to be 1, got %d", subscriptions[0].ID)
	}

	if subscriptions[0].VehicleID != 1 {
		t.Errorf("Expected subscription vehicle ID to be 1, got %d", subscriptions[0].VehicleID)
	}

	if subscriptions[0].ClientID != "client_id_1" {
		t.Errorf("Expected subscription client ID to be client_id_1, got %s", subscriptions[0].ClientID)
	}

	if subscriptions[1].ID != 2 {
		t.Errorf("Expected subscription ID to be 2, got %d", subscriptions[1].ID)
	}

	if subscriptions[1].VehicleID != 1 {
		t.Errorf("Expected subscription vehicle ID to be 1, got %d", subscriptions[1].VehicleID)
	}

	if subscriptions[1].ClientID != "client_id_2" {
		t.Errorf("Expected subscription client ID to be client_id_2, got %s", subscriptions[1].ClientID)
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("there were unfulfilled expectations: %s", err)
	}

}

func TestGetAllSubscriptions_Error(t *testing.T) {
	// configure to use case sensitive SQL query matcher
	// instead of default regular expression matcher
	db, mock, err := sqlmock.New(sqlmock.QueryMatcherOption(sqlmock.QueryMatcherEqual))
	if err != nil {
		t.Fatalf("an error '%s' was not expected when opening a stub database connection", err)
	}
	defer db.Close()

	mock.ExpectQuery("SELECT id, client_id, vehicle_id FROM subscription WHERE vehicle_id = ?").WillReturnError(errors.New("error"))

	vehicle := Vehicle{ID: 1, Manufacturer: "Toyota", Model: "Corolla", Year: "1996", LastRowID: sql.NullString{String: "E27", Valid: true}, Location: sql.NullString{String: "Ottawa", Valid: true}}
	subscriptions := GetAllSubscriptions(db, &vehicle)

	if len(subscriptions) != 0 {
		t.Errorf("Expected no subscriptions, got %d", len(subscriptions))
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("there were unfulfilled expectations: %s", err)
	}
}

func TestGetAllSubscriptions_NoVehicle(t *testing.T) {
	// configure to use case sensitive SQL query matcher
	// instead of default regular expression matcher
	db, _, err := sqlmock.New(sqlmock.QueryMatcherOption(sqlmock.QueryMatcherEqual))
	if err != nil {
		t.Fatalf("an error '%s' was not expected when opening a stub database connection", err)
	}
	defer db.Close()

	subscriptions := GetAllSubscriptions(db, nil)

	if len(subscriptions) != 0 {
		t.Errorf("Expected no subscriptions, got %d", len(subscriptions))
	}

}

func TestCreateSubscription_CreateSuccessfully(t *testing.T) {
	// configure to use case sensitive SQL query matcher
	// instead of default regular expression matcher
	db, mock, err := sqlmock.New(sqlmock.QueryMatcherOption(sqlmock.QueryMatcherEqual))
	if err != nil {
		t.Fatalf("an error '%s' was not expected when opening a stub database connection", err)
	}
	defer db.Close()

	mock.ExpectExec("INSERT INTO subscription (client_id, vehicle_id) VALUES (?, ?)").WithArgs("client_id_1", 1).WillReturnResult(sqlmock.NewResult(1, 1))
	mock.ExpectQuery("SELECT id, client_id, vehicle_id FROM subscription WHERE id = ?").WithArgs(1).WillReturnRows(sqlmock.NewRows([]string{"id", "client_id", "vehicle_id"}).AddRow(1, "client_id_1", 1))
	vehicle := Vehicle{ID: 1, Manufacturer: "Toyota", Model: "Corolla", Year: "1996", LastRowID: sql.NullString{String: "E27", Valid: true}, Location: sql.NullString{String: "Ottawa", Valid: true}}

	subscription, err := CreateSubscription(db, &vehicle, "client_id_1")

	if err != nil {
		t.Errorf("Expected no error, got %s", err)
	}

	if subscription.ID != 1 {
		t.Errorf("Expected subscription ID to be 1, got %d", subscription.ID)
	}

	if subscription.VehicleID != 1 {
		t.Errorf("Expected subscription vehicle ID to be 1, got %d", subscription.VehicleID)
	}

	if subscription.ClientID != "client_id_1" {
		t.Errorf("Expected subscription client ID to be client_id_1, got %s", subscription.ClientID)
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("there were unfulfilled expectations: %s", err)
	}

}

func TestCreateSubscription_ErrorInsert(t *testing.T) {
	// configure to use case sensitive SQL query matcher
	// instead of default regular expression matcher
	db, mock, err := sqlmock.New(sqlmock.QueryMatcherOption(sqlmock.QueryMatcherEqual))
	if err != nil {
		t.Fatalf("an error '%s' was not expected when opening a stub database connection", err)
	}
	defer db.Close()

	mock.ExpectExec("INSERT INTO subscription (client_id, vehicle_id) VALUES (?, ?)").WithArgs("client_id_1", 1).WillReturnError(errors.New("error"))

	vehicle := Vehicle{ID: 1, Manufacturer: "Toyota", Model: "Corolla", Year: "1996", LastRowID: sql.NullString{String: "E27", Valid: true}, Location: sql.NullString{String: "Ottawa", Valid: true}}

	subscription, err := CreateSubscription(db, &vehicle, "client_id_1")

	if err == nil {
		t.Errorf("Expected error, got nil")
	}

	if subscription != nil {
		t.Errorf("Expected subscription to be nil, got %v", subscription)
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("there were unfulfilled expectations: %s", err)
	}

}

func TestCreateSubscription_ErrorSelect(t *testing.T) {
	// configure to use case sensitive SQL query matcher
	// instead of default regular expression matcher
	db, mock, err := sqlmock.New(sqlmock.QueryMatcherOption(sqlmock.QueryMatcherEqual))
	if err != nil {
		t.Fatalf("an error '%s' was not expected when opening a stub database connection", err)
	}
	defer db.Close()

	mock.ExpectExec("INSERT INTO subscription (client_id, vehicle_id) VALUES (?, ?)").WithArgs("client_id_1", 1).WillReturnResult(sqlmock.NewResult(1, 1))
	mock.ExpectQuery("SELECT id, client_id, vehicle_id FROM subscription WHERE id = ?").WithArgs(1).WillReturnError(errors.New("error"))

	vehicle := Vehicle{ID: 1, Manufacturer: "Toyota", Model: "Corolla", Year: "1996", LastRowID: sql.NullString{String: "E27", Valid: true}, Location: sql.NullString{String: "Ottawa", Valid: true}}

	subscription, err := CreateSubscription(db, &vehicle, "client_id_1")

	if err == nil {
		t.Errorf("Expected error, got nil")
	}

	if subscription != nil {
		t.Errorf("Expected subscription to be nil, got %v", subscription)
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("there were unfulfilled expectations: %s", err)
	}

}

func TestDeleteDeleteSubscription_ExpectedQueriesCalled(t *testing.T) {
	// configure to use case sensitive SQL query matcher
	// instead of default regular expression matcher
	db, mock, err := sqlmock.New(sqlmock.QueryMatcherOption(sqlmock.QueryMatcherEqual))
	if err != nil {
		t.Fatalf("an error '%s' was not expected when opening a stub database connection", err)
	}
	defer db.Close()

	mock.ExpectExec("DELETE FROM subscription WHERE client_id = ? AND vehicle_id = ?").WithArgs("client_id_1", 1).WillReturnResult(sqlmock.NewResult(1, 1))

	vehicle := Vehicle{ID: 1, Manufacturer: "Toyota", Model: "Corolla", Year: "1996", LastRowID: sql.NullString{String: "E27", Valid: true}, Location: sql.NullString{String: "Ottawa", Valid: true}}

	DeleteSubscription(db, &vehicle, "client_id_1")

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("there were unfulfilled expectations: %s", err)
	}
}

// TODO do rest of functions.
