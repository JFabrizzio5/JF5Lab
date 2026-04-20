import React, { createContext, useContext, useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route, Navigate, useNavigate, useLocation } from 'react-router-dom'
import LoginPage from './pages/LoginPage.jsx'
import LandingPage from './pages/LandingPage.jsx'
import DashboardPage from './pages/DashboardPage.jsx'
import EditorsPage from './pages/EditorsPage.jsx'
import ReviewsPage from './pages/ReviewsPage.jsx'
import ReviewDetailPage from './pages/ReviewDetailPage.jsx'
import PlansPage from './pages/PlansPage.jsx'
import Layout from './components/Layout.jsx'

export const AuthContext = createContext(null)

export function useAuth() {
  return useContext(AuthContext)
}

function AuthProvider({ children }) {
  const [editor, setEditor] = useState(() => {
    try { return JSON.parse(localStorage.getItem('editor')) } catch { return null }
  })
  const [token, setToken] = useState(() => localStorage.getItem('token'))

  const login = (tokenValue, editorData) => {
    localStorage.setItem('token', tokenValue)
    localStorage.setItem('editor', JSON.stringify(editorData))
    setToken(tokenValue)
    setEditor(editorData)
  }

  const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('editor')
    setToken(null)
    setEditor(null)
  }

  return (
    <AuthContext.Provider value={{ editor, token, login, logout, isAdmin: editor?.role === 'admin' }}>
      {children}
    </AuthContext.Provider>
  )
}

function PrivateRoute({ children }) {
  const { token } = useAuth()
  return token ? children : <Navigate to="/login" replace />
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route element={<PrivateRoute><Layout /></PrivateRoute>}>
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/editors" element={<EditorsPage />} />
            <Route path="/reviews" element={<ReviewsPage />} />
            <Route path="/reviews/:id" element={<ReviewDetailPage />} />
            <Route path="/plans" element={<PlansPage />} />
          </Route>
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}
