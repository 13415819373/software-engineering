import { useEffect, useState } from 'react';

const PAGES_API_BASE_URL = 'https://se-production-2cc7.up.railway.app';
const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL ||
  (import.meta.env.MODE === 'github-pages' ? PAGES_API_BASE_URL : '')
).replace(/\/+$/, '');

async function request(path, options) {
  if (import.meta.env.MODE === 'github-pages' && !API_BASE_URL) {
    throw new Error('GitHub Pages 只托管前端；请在仓库变量中配置 VITE_API_BASE_URL 指向公开 API。');
  }

  const url = API_BASE_URL ? `${API_BASE_URL}${path}` : `/api${path}`;
  const response = await fetch(url, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...options?.headers },
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `请求失败（${response.status}）`);
  }
  return response.status === 204 ? null : response.json();
}

export default function App() {
  const [events, setEvents] = useState([]);
  const [registrations, setRegistrations] = useState({});
  const [username, setUsername] = useState('user1');
  const [message, setMessage] = useState('正在加载活动…');

  async function loadData() {
    const eventList = await request('/events');
    const entries = await Promise.all(
      eventList.map(async (event) => [
        event.id,
        await request(`/events/${event.id}/registrations`),
      ]),
    );
    setEvents(eventList);
    setRegistrations(Object.fromEntries(entries));
    setMessage('数据已从服务器读取');
  }

  useEffect(() => {
    loadData().catch((error) => setMessage(`加载失败：${error.message}`));
  }, []);

  async function addRegistration(eventId) {
    try {
      await request(`/events/${eventId}/registrations`, {
        method: 'POST',
        body: JSON.stringify({ username }),
      });
      await loadData();
    } catch (error) {
      setMessage(`操作失败：${error.message}`);
    }
  }

  async function renameRegistration(eventId, registration) {
    const nextName = registration.username === 'user1' ? 'user2' : 'user1';
    try {
      await request(`/events/${eventId}/registrations/${registration.id}`, {
        method: 'PATCH',
        body: JSON.stringify({ username: nextName }),
      });
      await loadData();
    } catch (error) {
      setMessage(`修改失败：${error.message}`);
    }
  }

  async function removeRegistration(eventId, registrationId) {
    try {
      await request(`/events/${eventId}/registrations/${registrationId}`, {
        method: 'DELETE',
      });
      await loadData();
    } catch (error) {
      setMessage(`删除失败：${error.message}`);
    }
  }

  return (
    <main className="page">
      <header className="hero">
        <p className="eyebrow">活动管理 · Docker Compose 示例</p>
        <h1>活动报名</h1>
        <p>网页把请求交给 API，报名信息由 SQLite 保存。</p>
        <label className="user-picker">
          当前练习用户
          <select value={username} onChange={(event) => setUsername(event.target.value)}>
            <option>user1</option>
            <option>user2</option>
          </select>
        </label>
      </header>

      <p className="status" role="status">{message}</p>
      <section className="event-grid" aria-label="活动列表">
        {events.map((event) => (
          <article className="event-card" key={event.id}>
            <div className="card-top"><span>活动 {String(event.id).padStart(2, '0')}</span><span>开放报名</span></div>
            <h2>{event.name}</h2>
            <p className="count">{(registrations[event.id] || []).length}<span> 人已报名</span></p>
            <button onClick={() => addRegistration(event.id)}>为 {username} 报名</button>
            <ul>
              {(registrations[event.id] || []).map((registration) => (
                <li key={registration.id}>
                  <span>{registration.username}</span>
                  <div className="actions">
                    <button className="secondary" onClick={() => renameRegistration(event.id, registration)}>改名</button>
                    <button className="secondary danger" onClick={() => removeRegistration(event.id, registration.id)}>删除</button>
                  </div>
                </li>
              ))}
            </ul>
          </article>
        ))}
      </section>
      <footer>刷新页面试试：报名数据仍由服务器保存。</footer>
    </main>
  );
}
