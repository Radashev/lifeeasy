import { useEffect, useState } from 'react'
import './App.css'

type User = {
  id: number
  name: string
  email: string
  role: 'root' | 'admin' | 'user'
  is_active: boolean
}

function App() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [user, setUser] = useState<User | null>(null)
  const [error, setError] = useState('')

  useEffect(() => {
  const restoreSession = async () => {
    const token = localStorage.getItem('access_token')

    if (!token) {
      return
    }

    const response = await fetch(
      'http://localhost:8012/auth/me',
      {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    )

    if (!response.ok) {
      localStorage.removeItem('access_token')
      return
    }

    const userData: User = await response.json()

    setUser(userData)
  }

  restoreSession()
}, [])

  const handleSubmit = async (
    event: React.FormEvent<HTMLFormElement>,
  ) => {
    event.preventDefault()

    setError('')

    const formData = new URLSearchParams()

    formData.append('username', email)
    formData.append('password', password)

    const response = await fetch(
      'http://localhost:8012/auth/login',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData,
      },
    )

    const data = await response.json()

    if (!response.ok) {
      setError('Invalid email or password')
      return
    }

    localStorage.setItem('access_token', data.access_token)

    const token = data.access_token

    const meResponse = await fetch(
      'http://localhost:8012/auth/me',
      {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    )

    if (!meResponse.ok) {
      localStorage.removeItem('access_token')
      setError('Could not load user information')
      return
    }

    const meData: User = await meResponse.json()

    setUser(meData)
  }

  const handleLogout = () => {
  localStorage.removeItem('access_token')
  setUser(null)
  setEmail('')
  setPassword('')
  setError('')
}

  if (user?.role === 'root') {
    return (
      <main className="app-shell">
        <section className="login-card">
          <span className="brand-badge">LifeEasy</span>

          <h1>ROOT Dashboard</h1>

          <p>Full system access</p>
          <p>{user.name}</p>
          <p>{user.email}</p>
          <button
          type="button"
          onClick={handleLogout}
        >
          Logout
        </button>
        </section>
      </main>
    )
  }

  return (
    <main className="app-shell">
      <section className="login-card">
        <div className="brand-block">
          <span className="brand-badge">LifeEasy</span>

          <h1>Welcome back</h1>

          <p>
            Sign in to continue to your workspace.
          </p>
        </div>

        {error && (
          <p className="error-message">
            {error}
          </p>
        )}

        <form
          className="login-form"
          onSubmit={handleSubmit}
        >
          <label htmlFor="email">
            Email
          </label>

          <input
            id="email"
            type="email"
            placeholder="you@example.com"
            value={email}
            onChange={(event) =>
              setEmail(event.target.value)
            }
            required
          />

          <label htmlFor="password">
            Password
          </label>

          <input
            id="password"
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(event) =>
              setPassword(event.target.value)
            }
            required
          />

          <button type="submit">
            Sign in
          </button>
        </form>
      </section>
    </main>
  )
}

export default App