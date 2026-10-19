import { useEffect, useState } from 'react'
import './App.css'

const API = 'http://127.0.0.1:8003'

type Registration = { id: number; event_id: number; username: string }
type EventItem = { id: number; name: string; registrations: Registration[] }

async function request(url: string, options?: RequestInit) {
  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    let msg = `请求失败（${res.status}）`
    try {
      const data = await res.json()
      if (typeof data.detail === 'string') msg = data.detail
      else if (Array.isArray(data.detail)) msg = '输入不合法：' + data.detail[0]?.msg
    } catch {
      /* 没有响应正文（如 204）就用默认提示 */
    }
    throw new Error(msg)
  }
  return res.status === 204 ? null : res.json()
}

function App() {
  const [events, setEvents] = useState<EventItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [inputs, setInputs] = useState<Record<number, string>>({})

  // 读取所有活动，并为每个活动读取报名列表
  async function loadAll() {
    try {
      setError('')
      const list: { id: number; name: string }[] = await request(`${API}/events`)
      const full = await Promise.all(
        list.map(async (e) => ({
          ...e,
          registrations: await request(`${API}/events/${e.id}/registrations`),
        })),
      )
      setEvents(full)
    } catch (e) {
      setError(e instanceof Error ? e.message : '加载失败')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadAll()
  }, [])

  // 统一处理：执行操作，成功后重新读取，失败显示错误
  async function run(action: () => Promise<unknown>) {
    try {
      setError('')
      await action()
      await loadAll()
    } catch (e) {
      setError(e instanceof Error ? e.message : '操作失败')
    }
  }

  function addRegistration(eventId: number) {
    run(async () => {
      await request(`${API}/events/${eventId}/registrations`, {
        method: 'POST',
        body: JSON.stringify({ username: inputs[eventId] ?? '' }),
      })
      setInputs((prev) => ({ ...prev, [eventId]: '' }))
    })
  }

  function editRegistration(eventId: number, reg: Registration) {
    const name = window.prompt('修改用户名', reg.username)
    if (name === null) return
    run(() =>
      request(`${API}/events/${eventId}/registrations/${reg.id}`, {
        method: 'PATCH',
        body: JSON.stringify({ username: name }),
      }),
    )
  }

  function deleteRegistration(eventId: number, reg: Registration) {
    run(() =>
      request(`${API}/events/${eventId}/registrations/${reg.id}`, {
        method: 'DELETE',
      }),
    )
  }

  if (loading) return <p>正在加载…</p>

  return (
    <main>
      <h1>活动报名</h1>
      {error && <p style={{ color: 'crimson' }}>错误：{error}</p>}

      {events.map((e) => (
        <section key={e.id}>
          <h2>
            {e.name}（{e.registrations.length} 人）
          </h2>

          <ul>
            {e.registrations.map((r) => (
              <li key={r.id}>
                {r.username}{' '}
                <button type="button" onClick={() => editRegistration(e.id, r)}>
                  修改
                </button>{' '}
                <button type="button" onClick={() => deleteRegistration(e.id, r)}>
                  删除
                </button>
              </li>
            ))}
          </ul>

          <input
            value={inputs[e.id] ?? ''}
            placeholder="用户名，如 user1"
            onChange={(ev) => setInputs((p) => ({ ...p, [e.id]: ev.target.value }))}
          />{' '}
          <button type="button" onClick={() => addRegistration(e.id)}>
            报名
          </button>
        </section>
      ))}
    </main>
  )
}

export default App