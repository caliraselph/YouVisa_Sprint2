import React, { useCallback, useEffect, useMemo, useState } from 'react';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000';

function App() {
  const [cases, setCases] = useState([]);
  const [caseId, setCaseId] = useState('');
  const [selectedCase, setSelectedCase] = useState(null);
  const [userId, setUserId] = useState('demo-user');
  const [email, setEmail] = useState('demo@youvisa.com');
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState('');
  const [chatInput, setChatInput] = useState('');
  const [chatHistory, setChatHistory] = useState(() => ([
    { sender: 'bot', text: 'Olá! Envie um documento via formulário ou pergunte pelo status do seu caso.' }
  ]));
  const [chatSending, setChatSending] = useState(false);

  const fetchCases = useCallback(async () => {
    try {
      const response = await fetch(`${API_BASE}/cases`);
      const data = await response.json();
      setCases(Array.isArray(data) ? data : []);
    } catch (err) {
      console.warn('Falha ao obter casos', err);
    }
  }, [API_BASE]);

  useEffect(() => {
    fetchCases();
  }, [fetchCases]);

  const handleSearch = useCallback(async () => {
    if (!caseId) {
      setSelectedCase(null);
      return;
    }
    try {
      const response = await fetch(`${API_BASE}/cases/${caseId}`);
      if (!response.ok) {
        throw new Error('Caso não encontrado');
      }
      const data = await response.json();
      setSelectedCase(data);
    } catch (err) {
      setSelectedCase({ error: err.message });
    }
  }, [API_BASE, caseId]);

  const handleUpload = useCallback(async (event) => {
    event.preventDefault();
    if (!file) {
      setUploadMessage('Selecione um arquivo para enviar.');
      return;
    }
    setUploading(true);
    setUploadMessage('');
    try {
      const formData = new FormData();
      formData.append('user_id', userId);
      formData.append('email', email);
      formData.append('file', file);

      const response = await fetch(`${API_BASE}/upload`, {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data?.detail || 'Falha no upload');
      }
      setUploadMessage(`Upload concluído! Status: ${data.status}`);
      setCases((prev) => [data, ...prev]);
      setFile(null);
      event.target.reset();
      fetchCases();
    } catch (err) {
      setUploadMessage(`Erro ao enviar: ${err.message}`);
    } finally {
      setUploading(false);
    }
  }, [API_BASE, email, file, fetchCases, userId]);

  const handleSendChat = useCallback(async () => {
    if (!chatInput.trim()) {
      return;
    }
    const currentMessage = chatInput;
    setChatInput('');
    setChatHistory((prev) => [...prev, { sender: 'user', text: currentMessage }]);

    setChatSending(true);
    try {
      const response = await fetch(`${API_BASE}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          message: currentMessage,
          case_id: caseId || undefined,
        }),
      });
      const data = await response.json();
      const reply = data?.reply || 'Não consegui interpretar sua mensagem. Tente reformular.';
      setChatHistory((prev) => [...prev, { sender: 'bot', text: reply }]);
    } catch (err) {
      setChatHistory((prev) => [...prev, {
        sender: 'bot',
        text: `Não foi possível responder agora: ${err.message}`,
      }]);
    } finally {
      setChatSending(false);
    }
  }, [API_BASE, caseId, chatInput, userId]);

  const uploadDisabled = useMemo(() => uploading, [uploading]);

  return (
    <div className="app">
      <header>
        <h1>YOUVISA – Painel do Agente</h1>
        <p>Gerencie uploads, acompanhe casos e interaja pelo assistente cognitivo.</p>
      </header>

      <main>
        <section className="panel">
          <h2>Envio de Documento</h2>
          <form onSubmit={handleUpload} className="upload-form">
            <label>
              Usuário
              <input value={userId} onChange={(e) => setUserId(e.target.value)} required />
            </label>
            <label>
              E-mail
              <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
            </label>
            <label>
              Arquivo
              <input type="file" onChange={(e) => setFile(e.target.files?.[0] ?? null)} required />
            </label>
            <button type="submit" disabled={uploadDisabled}>{uploading ? 'Enviando...' : 'Enviar documento'}</button>
          </form>
          {uploadMessage && <p className="status-message">{uploadMessage}</p>}

          <div className="cases">
            <div className="cases-header">
              <h2>Casos registrados</h2>
              <button type="button" onClick={fetchCases}>Atualizar</button>
            </div>
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Email</th>
                  <th>Tipo</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {cases.length === 0 && (
                  <tr>
                    <td colSpan="4">Nenhum caso registrado ainda.</td>
                  </tr>
                )}
                {cases.map((c) => (
                  <tr key={c.id || c.case_id}>
                    <td>{c.id || c.case_id}</td>
                    <td>{c.email}</td>
                    <td>{c.tipo_doc}</td>
                    <td>{c.status}</td>
                  </tr>
                ))}
              </tbody>
            </table>

            <div className="case-search">
              <h3>Consultar caso por ID</h3>
              <input
                value={caseId}
                onChange={(e) => setCaseId(e.target.value)}
                placeholder="ID do caso"
              />
              <button type="button" onClick={handleSearch}>Buscar</button>
              {selectedCase && (
                <pre>{JSON.stringify(selectedCase, null, 2)}</pre>
              )}
            </div>
          </div>
        </section>

        <section className="chat">
          <h2>Assistente Cognitivo</h2>
          <div className="chat-window">
            {chatHistory.map((msg, index) => (
              <div key={index} className={`chat-bubble ${msg.sender}`}>
                <strong>{msg.sender === 'user' ? 'Você' : 'YOUAssistant'}</strong>
                <p>{msg.text}</p>
              </div>
            ))}
          </div>
          <div className="chat-input">
            <input
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
              placeholder="Escreva uma mensagem..."
              onKeyDown={(event) => {
                if (event.key === 'Enter') {
                  event.preventDefault();
                  handleSendChat();
                }
              }}
            />
            <button type="button" onClick={handleSendChat} disabled={chatSending}>
              {chatSending ? 'Enviando...' : 'Enviar'}
            </button>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
