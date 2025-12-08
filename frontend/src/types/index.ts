export interface User {
  id: number
  email: string
  displayName: string
  is_admin: boolean
  created_at: string
}

export interface Event {
  id: number
  title: string
  description: string
  start_time: string
  end_time: string
  location?: string
  created_by: number
  created_at: string
  updated_at: string
}

export interface EventWithCreator extends Event {
  creator: User
}
