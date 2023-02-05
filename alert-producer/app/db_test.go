package app

import (
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
}

// TODO do rest of functions.
