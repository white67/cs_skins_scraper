import React from "react";
import { Button } from "@mantine/core";

interface BuyButtonProps {
  text: string;
  color: string;
  listing_url?: string;
}

const BuyButton: React.FC<BuyButtonProps> = ({ text, color, listing_url }) => {
  // Handle button click to open the provided URL
  const handleClick = () => {
    if (listing_url) {
      window.open(listing_url, "_blank"); // Open the URL in a new tab
    } else {
      console.error("Link is not provided"); // Log an error if no URL is provided
    }
  };

  return (
    <Button
      style={{
        backgroundColor: color,
        width: "100%",
        fontSize: "clamp(0.7rem, 2vw, 0.8rem)", // Responsive font size
      }}
      radius="md"
      size="sm"
      onClick={handleClick} // Attach click handler
    >
      {text}
    </Button>
  );
};

export default BuyButton;
