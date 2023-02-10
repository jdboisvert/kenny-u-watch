package app

import "database/sql"

type Vehicle struct {
	ID           int            `json:"id"`
	Manufacturer string         `json:"manufacturer"`
	Model        string         `json:"model"`
	Year         string         `json:"year"`
	LastRowID    sql.NullString `json:"last_row_id"`
	Location     sql.NullString `json:"location"`
}

type Subscription struct {
	ID        int    `json:"id"`
	ClientID  string `json:"client_id"`
	VehicleID int    `json:"vehicle_id"`
}

type VehicleSubscription struct {
	Manufacturer string `json:"manufacturer"`
	Model        string `json:"model"`
	Year         string `json:"year"`
	ClientID     string `json:"client_id"`
}
