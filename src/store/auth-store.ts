import { create } from 'zustand'
import { createJSONStorage, persist } from 'zustand/middleware'

import type { AuthUser, UserRole } from '@/types'

const VALID_ROLES: ReadonlySet<string> = new Set<UserRole>(['collection', 'processing', 'cs', 'qa', 'admin'])

export const AUTH_STORAGE_KEY = 'labs-auth'

interface AuthState {
  token: string | null
  user: AuthUser | null
  setSession: (token: string, user: AuthUser) => void
  clearSession: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: 'dev-token',
      user: {
        id: 'dev-admin',
        username: 'admin',
        email: 'admin@dev.local',
        displayName: 'Administrator',
        title: 'Dev Admin',
        role: 'admin' as const
      },
      setSession: (token, user) => set({ token, user }),
      clearSession: () => set({ token: null, user: null }),
    }),
    {
      name: AUTH_STORAGE_KEY,
      storage: createJSONStorage(() => localStorage),
      merge: (persisted, current) => {
        return current
      },
    },
  ),
)
