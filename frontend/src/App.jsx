import InitializeListener from "./components/InitializeListener";
import TranscriptList from "./components/TranscriptList";

function App() {
  return (
    <div style={{ fontFamily: "Arial, sans-serif", padding: "20px" }}>
      <InitializeListener />
      <TranscriptList />
    </div>
  );
}

export default App;
