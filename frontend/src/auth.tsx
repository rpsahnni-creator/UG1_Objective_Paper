import AsyncStorage from "@react-native-async-storage/async-storage";
import {
  createContext,
  ReactNode,
  useCallback,
  useContext,
  useEffect,
  useState,
} from "react";

const BASE = process.env.EXPO_PUBLIC_BACKEND_URL || "";
const KEY = "@app:auth";

export type Session = { token: string; email: string; isAdmin: boolean } | null;

type Ctx = {
  session: Session;
  ready: boolean;
  loginAdmin: (u: string, p: string) => Promise<void>;
  loginGuest: () => Promise<void>;
  logout: () => Promise<void>;
};
const AuthCtx = createContext<Ctx>({
  session: null,
  ready: false,
  loginAdmin: async () => {},
  loginGuest: async () => {},
  logout: async () => {},
});

export function AuthProvider({ children }: { children: ReactNode }) {
  const [session, setSession] = useState<Session>(null);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    (async () => {
      try {
        const raw = await AsyncStorage.getItem(KEY);
        if (raw) setSession(JSON.parse(raw));
      } finally {
        setReady(true);
      }
    })();
  }, []);

  const save = useCallback(async (s: Session) => {
    setSession(s);
    if (s) await AsyncStorage.setItem(KEY, JSON.stringify(s));
    else await AsyncStorage.removeItem(KEY);
  }, []);

  const loginAdmin = useCallback(async (username: string, password: string) => {
    const r = await fetch(`${BASE}/api/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    if (!r.ok) throw new Error("invalid");
    const data = await r.json();
    await save({ token: data.token, email: data.email, isAdmin: data.is_admin });
  }, [save]);

  const loginGuest = useCallback(async () => {
    const r = await fetch(`${BASE}/api/auth/guest`, { method: "POST" });
    if (!r.ok) throw new Error("guest-failed");
    const data = await r.json();
    await save({ token: data.token, email: data.email, isAdmin: data.is_admin });
  }, [save]);

  const logout = useCallback(async () => {
    await save(null);
  }, [save]);

  return (
    <AuthCtx.Provider value={{ session, ready, loginAdmin, loginGuest, logout }}>
      {children}
    </AuthCtx.Provider>
  );
}

export const useAuth = () => useContext(AuthCtx);

export async function apiGet<T>(path: string, token?: string): Promise<T> {
  const r = await fetch(`${BASE}${path}`, {
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  });
  if (!r.ok) throw new Error(`${r.status}`);
  return r.json();
}
export async function apiPost<T>(path: string, body: any, token?: string): Promise<T> {
  const r = await fetch(`${BASE}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: JSON.stringify(body),
  });
  if (!r.ok) throw new Error(`${r.status}`);
  return r.json();
}
