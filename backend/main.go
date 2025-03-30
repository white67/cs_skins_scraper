package main

import (
	"database/sql"
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/joho/godotenv"

	"github.com/gin-gonic/gin"
	_ "github.com/lib/pq"
)

var db *sql.DB

// Listing struct to map to the database
type Listing struct {
	ItemName         string   `json:"item_name"`
	MarketHashName   string   `json:"market_hash_name"`
	ItemType         string   `json:"item_type"`
	ItemTypeCategory *string  `json:"item_type_category"` // Change from `string` to `*string`
	DefIndex         *int     `json:"def_index"`
	PaintIndex       *int     `json:"paint_index"`
	PaintSeed        *int     `json:"paint_seed"`
	FloatValue       *float64 `json:"float_value"`
	IconUrl          string   `json:"icon_url"`
	IsStatTrak       *bool    `json:"is_stattrak"`
	IsSouvenir       *bool    `json:"is_souvenir"`
	Rarity           *string  `json:"rarity"`
	Wear             *string  `json:"wear"`
	Tradable         bool     `json:"tradable"`
	TradeBanDays     *int     `json:"trade_ban_days"`
	InspectLink      *string  `json:"inspect_link"`
	ItemDescription  *string  `json:"item_description"`
	ItemCollection   *string  `json:"item_collection"`
	Price            float64  `json:"price"`
	PriceCurrency    string   `json:"price_currency"`
	ListingID        int64    `json:"listing_id"`
	ListingURL       string   `json:"listing_url"`
	ListingTimestamp int64    `json:"listing_timestamp"`
}

// Initialize the database connection
func init() {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}

	// Load database configuration from environment variables
	connStr := fmt.Sprintf("postgres://%s:%s@%s:%s/%s?sslmode=disable",
		os.Getenv("POSTGRES_USER"),
		os.Getenv("POSTGRES_PASSWORD"),
		os.Getenv("DB_HOST"),
		os.Getenv("DB_PORT"),
		os.Getenv("DB_NAME"))

	// Connect to PostgreSQL
	db, err = sql.Open("postgres", connStr)
	if err != nil {
		log.Fatal("Error connecting to the database: ", err)
	}

	// Verify the connection
	err = db.Ping()
	if err != nil {
		log.Fatal("Error pinging the database: ", err)
	}
	fmt.Println("Successfully connected to the database!")
}

// Fetch all listings
func getListings(c *gin.Context) {
	rows, err := db.Query("SELECT * FROM listings")
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	defer rows.Close()

	listings := []Listing{}
	for rows.Next() {
		var listing Listing
		var id int // hold the id, even though it's not used
		if err := rows.Scan(
			&id, // Scan the id we don't even use
			&listing.ItemName,
			&listing.MarketHashName,
			&listing.ItemType,
			&listing.ItemTypeCategory,
			&listing.DefIndex,
			&listing.PaintIndex,
			&listing.PaintSeed,
			&listing.FloatValue,
			&listing.IconUrl,
			&listing.IsStatTrak,
			&listing.IsSouvenir,
			&listing.Rarity,
			&listing.Wear,
			&listing.Tradable,
			&listing.TradeBanDays,
			&listing.InspectLink,
			&listing.ItemDescription,
			&listing.ItemCollection,
			&listing.Price,
			&listing.PriceCurrency,
			&listing.ListingURL,
			&listing.ListingTimestamp,
			&listing.ListingID,
		); err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		listings = append(listings, listing)
	}

	c.JSON(http.StatusOK, listings)
}

// // Insert a new listing into the database
// func insertListing(c *gin.Context) {
// 	var newListing Listing
// 	if err := c.ShouldBindJSON(&newListing); err != nil {
// 		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
// 		return
// 	}

// 	// Prepare the SQL query to insert a new listing
// 	query := `INSERT INTO listings (item_name, market_hash_name, item_type, item_type_category, def_index, paint_index, paint_seed, float_value, icon_url, is_stattrak, is_souvenir, rarity, wear, tradable, trade_ban_days, inspect_link, item_description, item_collection, price, price_currency, listing_url, listing_timestamp)
// 		VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22) RETURNING listing_id`

// 	var listingID int64
// 	err := db.QueryRow(query, newListing.ItemName, newListing.MarketHashName, newListing.ItemType, newListing.Price, newListing.PriceCurrency, newListing.ListingURL, newListing.ListingTimestamp).Scan(&listingID)
// 	if err != nil {
// 		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
// 		return
// 	}

// 	newListing.ListingID = listingID
// 	c.JSON(http.StatusCreated, newListing)
// }

// Main function
func main() {
	r := gin.Default()

	// Define routes
	r.GET("/listings", getListings)
	// r.POST("/listings", insertListing)

	// Start the server
	r.Run(":8080")
}
