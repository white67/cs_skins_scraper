package main

import (
	"database/sql"
	"fmt"
	"log"
	"net/http"
	"os"
	"path/filepath"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/gorilla/websocket"
	"github.com/joho/godotenv"
	_ "github.com/lib/pq"
)

var db *sql.DB
var clients = make(map[*websocket.Conn]bool) // Track connected WebSocket clients
var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool { return true }, // Allow all origins
}

// Listing struct to map to the database
type Listing struct {
	ItemName            string   `json:"item_name"`
	MarketHashName      string   `json:"market_hash_name"`
	ItemType            string   `json:"item_type"`
	ItemTypeCategory    *string  `json:"item_type_category"`
	DefIndex            *int     `json:"def_index"`
	PaintIndex          *int     `json:"paint_index"`
	PaintSeed           *int     `json:"paint_seed"`
	FloatValue          *float64 `json:"float_value"`
	IconUrl             string   `json:"icon_url"`
	IsStatTrak          *bool    `json:"is_stattrak"`
	IsSouvenir          *bool    `json:"is_souvenir"`
	Rarity              *string  `json:"rarity"`
	Wear                *string  `json:"wear"`
	Tradable            bool     `json:"tradable"`
	TradeBanDays        *int     `json:"trade_ban_days"`
	InspectLink         *string  `json:"inspect_link"`
	ItemDescription     *string  `json:"item_description"`
	ItemCollection      *string  `json:"item_collection"`
	Price               float64  `json:"price"`
	PriceCurrency       string   `json:"price_currency"`
	PriceCurrencySymbol string   `json:"price_currency_symbol"`
	ListingID           string   `json:"listing_id"`
	ListingURL          string   `json:"listing_url"`
	ListingTimestamp    int64    `json:"listing_timestamp"`
	Marketplace         string   `json:"marketplace"`
	ID                  int64    `json:"id"` // ID field
}

// WebSocket handler
func handleConnections(c *gin.Context) {
	conn, err := upgrader.Upgrade(c.Writer, c.Request, nil)
	if err != nil {
		log.Println("WebSocket upgrade error:", err)
		return
	}
	defer conn.Close()
	clients[conn] = true
	for {
		_, _, err := conn.ReadMessage()
		if err != nil {
			delete(clients, conn)
			break
		}
	}
}

// Broadcast new listings to all connected clients
func broadcastNewListing(listing Listing) {
	for client := range clients {
		err := client.WriteJSON(listing)
		if err != nil {
			log.Println("WebSocket error:", err)
			client.Close()
			delete(clients, client)
		}
	}
}

// Endpoint to insert a new listing and notify clients
func insertListings(c *gin.Context) {
	var newListings []Listing // Expect an array of listings
	if err := c.ShouldBindJSON(&newListings); err != nil {
		log.Println("JSON Binding Error:", err)
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	for _, listing := range newListings {
		query := `INSERT INTO listings (item_name, market_hash_name, item_type, item_type_category, def_index, paint_index, paint_seed, float_value, icon_url, is_stattrak, is_souvenir, rarity, wear, tradable, trade_ban_days, inspect_link, item_description, item_collection, price, price_currency, price_currency_symbol, listing_id, listing_url, listing_timestamp, marketplace) 
				  VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23, $24, $25) RETURNING id`

		err := db.QueryRow(query, listing.ItemName, listing.MarketHashName, listing.ItemType, listing.ItemTypeCategory, listing.DefIndex, listing.PaintIndex, listing.PaintSeed, listing.FloatValue, listing.IconUrl, listing.IsStatTrak, listing.IsSouvenir, listing.Rarity, listing.Wear, listing.Tradable, listing.TradeBanDays, listing.InspectLink, listing.ItemDescription, listing.ItemCollection, listing.Price, listing.PriceCurrency, listing.PriceCurrencySymbol, listing.ListingID, listing.ListingURL, listing.ListingTimestamp, listing.Marketplace).Scan(&listing.ID)

		if err != nil {
			log.Println("Database Insert Error:", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}

		broadcastNewListing(listing) // Notify clients for each listing
	}

	c.JSON(http.StatusCreated, gin.H{"message": "Listings inserted successfully"})
}

func loadEnvironment() {
	// Load root .env from project root
	projectRoot := filepath.Join(filepath.Dir(os.Args[0]), "..")
	_ = godotenv.Load(filepath.Join(projectRoot, ".env"))

	_ = godotenv.Overload(".env.local") // Loads .env.local from current directory
}

// Initialize the database connection
func init() {

	loadEnvironment()
	// godotenv.Overload(".env")

	// var hostname string

	// if os.Getenv("DOCKER_ENV") != "production" {
	// 	hostname = "localhost"
	// } else {
	// 	hostname = os.Getenv("DB_HOST")
	// 	if hostname == "" {
	// 		log.Fatal("DB_HOST environment variable is not set")
	// 	}
	// }

	//   postgres://user:password@host:port/dbname?sslmode=disable
	connStr := fmt.Sprintf("postgres://%s:%s@%s:%s/%s?sslmode=disable",
		os.Getenv("POSTGRES_USER"),
		os.Getenv("POSTGRES_PASSWORD"),
		os.Getenv("DB_HOST"),
		os.Getenv("DB_PORT"),
		os.Getenv("POSTGRES_DB"))

	// Connect to PostgreSQL
	var err error
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
	rows, err := db.Query("SELECT item_name, market_hash_name, item_type, item_type_category, def_index, paint_index, paint_seed, float_value, icon_url, is_stattrak, is_souvenir, rarity, wear, tradable, trade_ban_days, inspect_link, item_description, item_collection, price, price_currency, listing_url, listing_timestamp, listing_id, marketplace FROM listings ORDER BY listing_timestamp DESC LIMIT 50")
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	defer rows.Close()

	listings := []Listing{}
	for rows.Next() {
		var listing Listing
		// var id int // hold the id, even though it's not used
		if err := rows.Scan(
			// &id, // Scan the id we don't even use
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
			&listing.PriceCurrencySymbol,
			&listing.ListingURL,
			&listing.ListingTimestamp,
			&listing.ListingID,
			&listing.Marketplace,
		); err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		listings = append(listings, listing)
	}

	c.JSON(http.StatusOK, listings)
}

func main() {
	r := gin.Default()

	// WebSocket endpoint
	r.GET("/ws", func(c *gin.Context) {
		handleConnections(c)
	})

	// Enable CORS for the frontend to access the backend API
	r.Use(cors.Default()) // default CORS policy

	r.GET("/api/listings", getListings)
	r.POST("/api/listings", insertListings) // Endpoint for scraper to send new listings

	// Start the server
	r.Run(":8080")
}
