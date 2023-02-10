package app

import (
	"testing"

	"github.com/h2non/gock"
	kennyupull "github.com/jdboisvert/kenny-u-pull-go-sdk"
)

func TestSendUpdateToASubscriber_SendsAlertAsExpected(t *testing.T) {
	inventoryListing := kennyupull.InventoryListing{Year: "1996", Make: "Toyota", Model: "Corolla", RowID: "row1", Branch: "location1", DateListed: "2020-01-01", ListingUrl: "https://www.kennyupull.com/inventory/row1"}
	subscription := Subscription{ID: 1, ClientID: "client1", VehicleID: 1}

	testUrl := "https://alert-consumer-test.com"
	t.Setenv("MAIN_ALERT_CONSUMER_URL", testUrl)

	gock.New(testUrl).Post("").Reply(204)

	SendUpdateToASubscriber(&inventoryListing, &subscription)

	if !gock.IsDone() {
		t.Error("Expected an alert to be sent to the alert consumer")
	}
}
