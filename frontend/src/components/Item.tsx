import React from "react";
import { Card, Image, Text, Button } from "@mantine/core";
import { FiSearch } from "react-icons/fi"; // Import magnifier icon
import BuyButton from "./BuyButton"; // Import BuyButton component

interface ItemProps {
  imageUrl: string;
  itemName: string;
  marketplaceName: string;
  price: number | string;
  currencySymbol: string;
  floatValue: number | null;
  wear: string | null;
  rarity: string;
  inspectLink?: string | null;
  listingUrl?: string;
  isStatTrak: boolean;
}

// Function to generate a valid image URL
// const getValidImageUrl = (url: string) => {
//   return "https://steamcommunity-a.akamaihd.net/economy/image/" + url;
// };

// Function to return a gradient color based on rarity
const getGradientColor = (str: string) => {
  if (str.toLowerCase().includes("consumer")) {
    return "rgb(132, 123, 110)";
  } else if (str.toLowerCase().includes("industrial")) {
    return "rgb(94, 152, 217)";
  } else if (str.toLowerCase().includes("mil-spec")) {
    return "rgb(63, 97, 255)";
  } else if (str.toLowerCase().includes("restricted")) {
    return "rgb(49, 60, 255)";
  } else if (str.toLowerCase().includes("classified")) {
    return "rgb(211, 44, 230)";
  } else if (str.toLowerCase().includes("covert")) {
    return "rgb(235, 75, 75)";
  } else if (str.toLowerCase().includes("contraband")) {
    return "rgb(228, 174, 57)";
  } else {
    return "rgb(94, 91, 86)";
  }
};

// Function to return a color for different marketplace names
const getMarketplaceColor = (marketplaceName: string) => {
  if (marketplaceName.toLowerCase().includes("csfloat")) {
    return "#237bff";
  } else if (marketplaceName.toLowerCase().includes("skinbid")) {
    return "#71b944";
  } else if (marketplaceName.toLowerCase().includes("skinport")) {
    return "#fa490a";
  } else {
    return "#2b2b2b";
  }
};

// Function to determine StatTrak color
const getStatTrakColor = (isStattrak: boolean) => {
  return isStattrak ? "rgb(255, 136, 0)" : "rgb(255, 255, 255)";
};

// Function to format float value to 6 digits
const cutFloatValue = (value: number | null | undefined) => {
  return typeof value === "number" ? value.toFixed(8) : "";
};

// Function to return an empty string if the value is null or undefined
const emptyValue = (value: string | number | null | undefined) => {
  return typeof value === "number" || typeof value === "string"
    ? value.toString()
    : "";
};

const ItemCard: React.FC<ItemProps> = ({
  imageUrl,
  itemName,
  marketplaceName,
  price,
  currencySymbol,
  floatValue,
  wear,
  rarity,
  inspectLink,
  listingUrl,
  isStatTrak,
}) => {
  return (
    <Card
      shadow="sm"
      padding="lg"
      radius="md"
      withBorder
      style={{
        width: "100%",
        borderRadius: "8px",
        background: "rgb(28, 31, 31)",
        boxSizing: "border-box",
        paddingTop: "1px",
        paddingBottom: "1px",
      }}
    >
      {/* Section with item name and condition */}
      <div style={{ margin: "0.8em" }}>
        <Text
          fw={700}
          style={{
            margin: 0,
            fontSize: "clamp(0.75rem, 2vw, 0.85rem)",
            minHeight: "1.3em",
            whiteSpace: "nowrap",
            overflow: "hidden",
            textOverflow: "ellipsis",
            color: getStatTrakColor(isStatTrak),
          }}
        >
          {itemName}
        </Text>
        <Text
          fw={400}
          style={{
            marginTop: "0",
            color: "#aaa",
            fontSize: "clamp(12px, 2vw, 12px)",
            minHeight: "12px",
          }}
        >
          <span
            style={{ display: "inline", color: getStatTrakColor(isStatTrak) }}
          >
            {isStatTrak && "StatTrak™ "}
          </span>
          <span style={{ display: "inline", color: "#aaa" }}>
            {emptyValue(wear)}
          </span>
        </Text>
      </div>

      {/* Section with image */}
      <Card.Section style={{ position: "relative", height: "100%" }}>
        <Image
          src={imageUrl}
          alt={itemName}
          fit="cover"
          style={{
            width: "100%",
            background: `linear-gradient(rgba(27, 29, 36, 0) 20%, ${getGradientColor(
              rarity
            )} 150%)`,
          }}
        />
        {inspectLink && (
          <Button
            size="xs"
            radius="xl"
            variant="filled"
            style={{
              position: "absolute",
              bottom: 8,
              right: 4,
              backgroundColor: "rgba(0, 0, 0, 0.3)",
              color: "#fff",
              fontSize: "clamp(7px, 1.5vw, 14px)",
              padding: "clamp(3px, 0.5vw, 5px)",
            }}
          >
            <FiSearch size="1.2em" color="white" />
          </Button>
        )}
        {/* Float value in the bottom-left corner */}
        <Text
          size="sm"
          style={{
            position: "absolute",
            bottom: -8,
            left: 5,
            color: "#fff",
            borderRadius: "5px",
            fontSize: "clamp(0.7rem, 1vw, 1rem)",
            opacity: 0.8,
          }}
        >
          {cutFloatValue(floatValue)}
        </Text>
      </Card.Section>

      {/* Section with additional information */}
      <div
        style={{
          margin: "0.8em",
          marginTop: 0,
          padding: 0,
          gap: "0.3em",
          display: "flex",
          flexDirection: "column",
        }}
      >
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
          }}
        >
          <Text
            size="xl"
            fw={700}
            mt="md"
            mb="xs"
            style={{ color: "#fff", fontSize: "clamp(1.3rem, 2vw, 1.5rem)" }}
          >
            {currencySymbol}
            {price}
          </Text>
        </div>

        <BuyButton
          text={"Buy on " + marketplaceName}
          color={getMarketplaceColor(marketplaceName)}
          listing_url={listingUrl}
        />
      </div>
    </Card>
  );
};

export default ItemCard;
