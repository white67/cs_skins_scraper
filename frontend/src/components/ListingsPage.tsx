import { useEffect, useState } from "react";
import { MantineProvider } from "@mantine/core";
import ItemCard from "./Item";
import FetchingLoad from "./FetchingLoad";

interface Listing {
  itemName: string;
  marketHashName: string;
  itemType: string;
  itemTypeCategory: string | null;
  defIndex: number | null;
  paintIndex: number | null;
  paintSeed: number | null;
  floatValue: number | null;
  iconUrl: string;
  isStatTrak: boolean;
  isSouvenir: boolean;
  rarity: string;
  wear: string | null;
  tradable: boolean;
  tradeBanDays: number | null;
  inspectLink: string | null;
  itemDescription: string | null;
  itemCollection: string | null;
  price: number;
  priceCurrency: string;
  price_currency_symbol: string;
  listingId: number;
  listingUrl: string;
  listingTimestamp: number;
  marketplace: string;
  status: string;
}

const ListingsPage = () => {
  const [items, setListings] = useState<Listing[]>([]);
  const [highlighted, setHighlighted] = useState<Set<number>>(new Set());

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8080/ws");

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const newListing: Listing = {
        itemName: data.item_name,
        marketHashName: data.market_hash_name,
        itemType: data.item_type,
        itemTypeCategory: data.item_type_category,
        defIndex: data.def_index,
        paintIndex: data.paint_index,
        paintSeed: data.paint_seed,
        floatValue: data.float_value,
        iconUrl: data.icon_url,
        isStatTrak: data.is_stattrak,
        isSouvenir: data.is_souvenir,
        rarity: data.rarity,
        wear: data.wear,
        tradable: data.tradable,
        tradeBanDays: data.trade_ban_days,
        inspectLink: data.inspect_link,
        itemDescription: data.item_description,
        itemCollection: data.item_collection,
        price: data.price,
        priceCurrency: data.price_currency,
        price_currency_symbol: data.price_currency_symbol,
        listingId: data.listing_id,
        listingUrl: data.listing_url,
        listingTimestamp: data.listing_timestamp,
        marketplace: data.marketplace,
        status: data.status,
      };
      setListings((prevListings) => {
        const updatedListings = [newListing, ...prevListings]; // Add new item at the beginning
        return updatedListings.length > 600
          ? updatedListings.slice(0, 600)
          : updatedListings;
      });

      // Highlight the new item
      setHighlighted((prev) => new Set(prev).add(newListing.listingId));

      // Remove highlight after 0.5s
      setTimeout(() => {
        setHighlighted((prev) => {
          const newSet = new Set(prev);
          newSet.delete(newListing.listingId);
          return newSet;
        });
      }, 500);
    };

    return () => ws.close();
  }, []);

  return (
    <MantineProvider
      theme={{
        fontFamily: "Roboto, sans-serif",
      }}
    >
      <div
        style={{
          backgroundColor: "#121212",
          minHeight: "100vh", // Set minimum height to 100% of the viewport height
          color: "#ffffff",
          width: "100%",
        }}
      >
        {items.length === 0 && <FetchingLoad />}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", // Auto fit with minmax for responsive design
            gap: "15px",
          }}
        >
          {items.map((item, index) => (
            <div
              key={index}
              className={highlighted.has(item.listingId) ? "flash-border" : ""} // Add flash-border class if highlighted
              style={{
                flex: "1 1 clamp(150px, 20%, 200px)", // Min width: 150px, max width: 250px
                maxWidth: "250px",
                transition: "border 0.5s ease-in-out",
              }}
            >
              <ItemCard
                imageUrl={item.iconUrl}
                itemName={item.itemName}
                marketplaceName={item.marketplace}
                price={item.price}
                currencySymbol={item.price_currency_symbol}
                floatValue={item.floatValue}
                rarity={item.rarity}
                wear={item.wear}
                inspectLink={item.inspectLink}
                listingUrl={item.listingUrl}
                isStatTrak={item.isStatTrak}
              />
            </div>
          ))}
        </div>
      </div>
    </MantineProvider>
  );
};

export default ListingsPage;
