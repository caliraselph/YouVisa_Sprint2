import { useState } from "react";

const API_BASE = "http://127.0.0.1:8000";

function App() {
  const [caseId, setCaseId] = useState("VISA_1772314464");
  const [caseData, setCaseData] = useState(null);
  const [chatMessage, setChatMessage] = useState("");
  const [chatResponse, setChatResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function fetchStatus() {
    setLoading(true);
    setError("");
    setCaseData(null);
    try {
      const resp = await fetch(`${API_BASE}/cases/${caseId}`);
      if (!resp.ok) {
        throw new Error(`Erro ${resp.status}`);
      }
      const data = await resp.json();
      setCaseData(data);
    } catch (e) {
      setError(`Erro ao buscar caso: ${e.message}`);
    } finally {
      setLoading(false);
    }
  }

  async function sendChat() {
    if (!chatMessage.trim()) return;
    setChatResponse("");
    setError("");
    try {
      const form = new FormData();
      form.append("case_id", caseId);
      form.append("message", chatMessage);

      const resp = await fetch(`${API_BASE}/chat/`, {
        method: "POST",
        body: form,
      });
      if (!resp.ok) {
        throw new Error(`Erro ${resp.status}`);
      }
      const data = await resp.json();
      setChatResponse(data.mensagem || JSON.stringify(data));
    } catch (e) {
      setError(`Erro no chatbot: ${e.message}`);
    }
  }

  return (
    <div style={{ maxWidth: 800, margin: "20px auto", fontFamily: "sans-serif" }}>
      <h1>YouVisa – Acompanhamento de Processo</h1>

      <section style={{ marginBottom: 20 }}>
        <h2>1. Consultar status do caso</h2>
        <input
          value={caseId}
          onChange={(e) => setCaseId(e.target.value)}
          style={{ padding: 8, width: 260, marginRight: 8 }}
          placeholder="VISA_123..."
        />
        <button onClick={fetchStatus} style={{ padding: "8px 16px" }}>
          Ver status
        </button>

        {loading && <p>Carregando...</p>}
        {error && <p style={{ color: "red" }}>{error}</p>}

        {caseData && (
          <div
            style={{
              marginTop: 16,
              padding: 16,
              border: "1px solid #ccc",
              borderRadius: 8,
            }}
          >
            <h3>Status atual: {caseData.status}</h3>
            <p>Case ID: {caseData.case_id}</p>
            {caseData.next_states && (
              <p>Próximos estados possíveis: {caseData.next_states.join(", ")}</p>
            )}
          </div>
        )}
      </section>

      <section>
        <h2>2. Chatbot – Perguntar sobre o processo</h2>
        <input
          value={chatMessage}
          onChange={(e) => setChatMessage(e.target.value)}
          style={{ padding: 8, width: 260, marginRight: 8 }}
          placeholder="Qual o status? Falta documento?"
        />
        <button onClick={sendChat} style={{ padding: "8px 16px" }}>
          Perguntar
        </button>

        {chatResponse && (
          <div
            style={{
              marginTop: 16,
              padding: 16,
              border: "1px solid #ccc",
              borderRadius: 8,
              background: "#f7f7f7",
            }}
          >
            <strong>Resposta do chatbot:</strong>
            <p>{chatResponse}</p>
          </div>
        )}
      </section>
    </div>
  );
}

export default App;
