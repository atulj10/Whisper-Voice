import InitializeListener from "./components/InitializeListener";
import TranscriptList from "./components/TranscriptList";

function App() {
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <InitializeListener />
      <TranscriptList />
    </div>
  );
}

export default App;
