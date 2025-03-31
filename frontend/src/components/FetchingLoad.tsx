// Component to display a loading indicator while fetching data
function FetchingLoad() {
  return (
    <div
      className="sweet-loading"
      style={{
        display: "flex",
        textAlign: "center",
        marginTop: "10vh",
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
        gap: "1rem",
      }}
    >
      <div className="loader"></div> {/* Loader animation */}
      <div>Fetching new items...</div>
    </div>
  );
}

export default FetchingLoad;
