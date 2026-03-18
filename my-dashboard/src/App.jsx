import { useState } from 'react'
import PrivateDashboard from './PrivateDashboard'
import PublicSchoolsDashboard from './PublicSchoolsDashboard'

export default function App() {
  const [view, setView] = useState('private')

  const btnStyle = (v) => ({
    padding: '8px 24px',
    cursor: 'pointer',
    border: 'none',
    fontWeight: 600,
    fontSize: 13,     
    background: view === v ? '#1B3A5C' : '#e2e8f0',
    color: view === v ? '#fff' : '#4a5568',
    borderRadius: v === 'private' ? '8px 0 0 8px' : '0 8px 8px 0',
  })

  return (
    <div>
      {/* Nav bar */}
      <div style={{ display: 'flex', justifyContent: 'center', padding: '16px', background: '#f4f7fb', borderBottom: '1px solid #dde3ed' }}>
        <button style={btnStyle('private')} onClick={() => setView('private')}>
          🏫 Private Schools
        </button>
        <button style={btnStyle('public')} onClick={() => setView('public')}>
          🏛️ Public Schools
        </button>
      </div>

      {/* Dashboard */}
      {view === 'private' ? <PrivateDashboard /> : <PublicSchoolsDashboard />}
    </div>
  )
}