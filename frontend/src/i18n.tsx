import AsyncStorage from "@react-native-async-storage/async-storage";
import { createContext, ReactNode, useCallback, useContext, useEffect, useState } from "react";

export type Lang = "en" | "hi";
const STORAGE_KEY = "@app:lang";

type Ctx = { lang: Lang; setLang: (l: Lang) => void; toggle: () => void; ready: boolean };
const LangContext = createContext<Ctx>({
  lang: "en",
  setLang: () => {},
  toggle: () => {},
  ready: false,
});

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [lang, setLangState] = useState<Lang>("en");
  const [ready, setReady] = useState(false);

  useEffect(() => {
    (async () => {
      try {
        const stored = await AsyncStorage.getItem(STORAGE_KEY);
        if (stored === "en" || stored === "hi") setLangState(stored);
      } finally {
        setReady(true);
      }
    })();
  }, []);

  const setLang = useCallback(async (l: Lang) => {
    setLangState(l);
    try {
      await AsyncStorage.setItem(STORAGE_KEY, l);
    } catch {}
  }, []);

  const toggle = useCallback(() => {
    setLang(lang === "en" ? "hi" : "en");
  }, [lang, setLang]);

  return (
    <LangContext.Provider value={{ lang, setLang, toggle, ready }}>
      {children}
    </LangContext.Provider>
  );
}

export const useLang = () => useContext(LangContext);

type Dict = Record<string, { en: string; hi: string }>;
export const t: Dict = {
  app_title: {
    en: "Introduction to Computer & IT",
    hi: "कंप्यूटर व IT का परिचय",
  },
  app_subtitle: {
    en: "FYUGP • Semester-I • SEC Course",
    hi: "FYUGP • सेमेस्टर-I • SEC पाठ्यक्रम",
  },
  student_access: { en: "Student Access", hi: "छात्र प्रवेश" },
  admin_access: { en: "Admin Access", hi: "व्यवस्थापक लॉगिन" },
  back: { en: "Back", hi: "वापस" },
  login: { en: "Login", hi: "लॉगिन" },
  logging_in: { en: "Logging in…", hi: "लॉगिन हो रहा है…" },
  username: { en: "Email / Username", hi: "ईमेल / उपयोगकर्ता नाम" },
  password: { en: "Password", hi: "पासवर्ड" },
  course_overview: { en: "Course Overview", hi: "पाठ्यक्रम सारांश" },
  chapters: { en: "Chapters", hi: "इकाइयाँ" },
  study_material: { en: "Study Material", hi: "अध्ययन सामग्री" },
  mcq_quiz: { en: "MCQ Quiz", hi: "MCQ प्रश्नोत्तरी" },
  start_quiz: { en: "Start Quiz", hi: "प्रश्नोत्तरी शुरू करें" },
  next: { en: "Next", hi: "अगला" },
  submit: { en: "Submit", hi: "सबमिट" },
  question: { en: "Question", hi: "प्रश्न" },
  of: { en: "of", hi: "/" },
  correct_answer: { en: "Correct Answer", hi: "सही उत्तर" },
  explanation: { en: "Explanation", hi: "व्याख्या" },
  your_score: { en: "Your Score", hi: "आपका स्कोर" },
  correct: { en: "Correct", hi: "सही" },
  wrong: { en: "Wrong", hi: "गलत" },
  back_to_chapters: { en: "Back to Chapters", hi: "इकाइयों पर वापस" },
  review_answers: { en: "Review Answers", hi: "उत्तर समीक्षा" },
  questions_count: { en: "Questions", hi: "प्रश्न" },
  tap_to_select: { en: "Tap an option to answer", hi: "उत्तर देने के लिए विकल्प पर टैप करें" },
  loading: { en: "Loading…", hi: "लोड हो रहा है…" },
  retry: { en: "Retry", hi: "पुनः प्रयास" },
  failed: { en: "Something went wrong.", hi: "कुछ गलत हुआ।" },
  invalid_cred: { en: "Invalid credentials. Try again.", hi: "अमान्य विवरण। पुनः प्रयास करें।" },
  continue_free: { en: "Continue as Student (Free)", hi: "छात्र के रूप में जारी रखें (मुफ्त)" },
  logout: { en: "Logout", hi: "लॉगआउट" },
  admin_tag: { en: "Admin", hi: "व्यवस्थापक" },
  tap_option_hint: { en: "Tap any option — explanation will appear.", hi: "किसी विकल्प पर टैप करें — व्याख्या दिखेगी।" },
};

export const tr = (key: keyof typeof t, lang: Lang) => t[key]?.[lang] ?? key;
