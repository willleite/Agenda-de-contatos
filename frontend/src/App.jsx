import { useEffect, useState } from 'react';

export default function App() {
  const [contacts, setContacts] = useState([]);
  const [search, setSearch] = useState('');
  const [form, setForm] = useState({ name: '', phone: '', email: '', notes: '' });
  const [editingId, setEditingId] = useState(null);

  const API = 'http://localhost:8000/contacts/';

  const loadContacts = async (q = '') => {
    try {
      const url = q ? `${API}?q=${q}` : API;
      const res = await fetch(url);
      const data = await res.json();
      setContacts(data);
    } catch (err) {
      console.error('Erro ao carregar contatos:', err);
    }
  };

  useEffect(() => {
    loadContacts();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      if (editingId) {
        await fetch(`${API}${editingId}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(form)
        });
        setEditingId(null);
      } else {
        await fetch(API, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(form)
        });
      }

      setForm({ name: '', phone: '', email: '', notes: '' });
      loadContacts(search);
    } catch (err) {
      console.error('Erro ao salvar:', err);
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('Excluir contato?')) return;
    await fetch(`${API}${id}`, { method: 'DELETE' });
    loadContacts(search);
  };

  const handleEdit = (c) => {
    setForm({ name: c.name, phone: c.phone, email: c.email ?? '', notes: c.notes ?? '' });
    setEditingId(c.id);
  };

  return (
    <div style={{ padding: 20, maxWidth: 600, margin: '0 auto' }}>
      <h1>Agenda de Contatos</h1>

      <form onSubmit={(e) => { e.preventDefault(); loadContacts(search); }}>
        <input
          placeholder="Pesquisar por nome..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <button type="submit">Buscar</button>
        <button type="button" onClick={() => { setSearch(''); loadContacts(); }}>Limpar</button>
      </form>

      <hr />

      <form onSubmit={handleSubmit}>
        <input
          required
          placeholder="Nome"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
        />
        <input
          required
          placeholder="Telefone"
          value={form.phone}
          onChange={(e) => setForm({ ...form, phone: e.target.value })}
        />
        <input
          placeholder="Email"
          value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
        />
        <input
          placeholder="Observações"
          value={form.notes}
          onChange={(e) => setForm({ ...form, notes: e.target.value })}
        />

        <button type="submit">
          {editingId ? 'Salvar alterações' : 'Adicionar'}
        </button>
        {editingId && <button type="button" onClick={() => { setEditingId(null); setForm({ name: '', phone: '', email: '', notes: '' }); }}>Cancelar</button>}
      </form>

      <ul>
        {contacts.map((c) => (
          <li key={c.id} style={{ marginBottom: 10 }}>
            <strong>{c.name}</strong> — {c.phone} {c.email && `— ${c.email}`}
            <br />
            <button onClick={() => handleEdit(c)}>Editar</button>
            <button onClick={() => handleDelete(c.id)}>Excluir</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
