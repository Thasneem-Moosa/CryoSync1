import type { ReactNode } from 'react'
import { Navigate, useLocation } from 'react-router-dom'

import { useAuthStore } from '@/store'
import { canAccessPage } from '@/lib/permissions'
import { MainLayout } from '@/components/layout'
import AccessDenied from '@/pages/AccessDenied/AccessDeniedPage'

function RequireAuth({ children }: { children: ReactNode }) {
  const user = useAuthStore((s) => s.user)
  const location = useLocation()

  // Bypass login for development
  const bypassUser = {
    id: 'dev-admin',
    username: 'admin',
    email: 'admin@dev.local',
    displayName: 'Administrator',
    title: 'Dev Admin',
    role: 'admin' as const
  }

  const currentUser = user || bypassUser

  return (
    <MainLayout>
      {canAccessPage(currentUser.role, location.pathname) ? children : <AccessDenied />}
    </MainLayout>
  )
}

export { RequireAuth }
