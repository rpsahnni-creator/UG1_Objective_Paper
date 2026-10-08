import { useEffect, useMemo, useRef, useState } from "react";
import { useLocalSearchParams, useRouter } from "expo-router";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  ActivityIndicator, Pressable, ScrollView, StyleSheet, Text, View,
} from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import Feather from "@react-native-vector-icons/feather";

import { apiDelete, apiGet, apiPost, useAuth } from "@/src/auth";
import { useLang, tr } from "@/src/i18n";
import { LangToggle } from "@/src/LangToggle";
import { colors, radius, spacing } from "@/src/theme-exports";

type Section = { heading_en: string; heading_hi: string; body_en: string; body_hi: string };
type Material = { chapter_id: string; title_en: string; title_hi: string; sections: Section[] };
type Chapter = { id: string; name_en: string; name_hi: string; question_count: number };
type Bookmark = { id: string; chapter_id: string; section_index: number };

export default function ChapterDetail() {
  const { id, section } = useLocalSearchParams<{ id: string; section?: string }>();
  const insets = useSafeAreaInsets();
  const router = useRouter();
  const { lang } = useLang();
  const { session } = useAuth();
  const qc = useQueryClient();
  const [tab, setTab] = useState<"study" | "quiz">("study");
  const scrollRef = useRef<ScrollView>(null);
  const sectionY = useRef<number[]>([]);
  const [scrolledToSection, setScrolledToSection] = useState(false);

  const chapterQ = useQuery<Chapter[]>({
    queryKey: ["chapters"],
    queryFn: () => apiGet<Chapter[]>("/api/chapters", session?.token),
  });
  const chapter = (chapterQ.data ?? []).find((c) => c.id === id);

  const matQ = useQuery<Material>({
    queryKey: ["study", id],
    queryFn: () => apiGet<Material>(`/api/chapters/${id}/study-material`, session?.token),
    enabled: !!id,
  });

  const bookmarksQ = useQuery<Bookmark[]>({
    queryKey: ["bookmarks"],
    queryFn: () => apiGet<Bookmark[]>("/api/bookmarks", session?.token),
    enabled: !!session?.token,
  });

  const bookmarkedSet = useMemo(
    () => new Set((bookmarksQ.data ?? []).filter((b) => b.chapter_id === id).map((b) => b.section_index)),
    [bookmarksQ.data, id],
  );

  const addBookmarkMut = useMutation({
    mutationFn: (payload: { chapter_id: string; section_index: number; heading_en: string; heading_hi: string }) =>
      apiPost("/api/bookmarks", payload, session?.token),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["bookmarks"] }),
  });
  const removeBookmarkMut = useMutation({
    mutationFn: (sectionIndex: number) => apiDelete(`/api/bookmarks/${id}/${sectionIndex}`, session?.token),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["bookmarks"] }),
  });

  const toggleBookmark = (idx: number, s: Section) => {
    if (bookmarkedSet.has(idx)) {
      removeBookmarkMut.mutate(idx);
    } else {
      addBookmarkMut.mutate({ chapter_id: String(id), section_index: idx, heading_en: s.heading_en, heading_hi: s.heading_hi });
    }
  };

  const sectionParam = section !== undefined ? parseInt(section, 10) : undefined;

  useEffect(() => {
    if (sectionParam !== undefined && !Number.isNaN(sectionParam) && matQ.data && !scrolledToSection) {
      setTab("study");
      const timer = setTimeout(() => {
        const y = sectionY.current[sectionParam];
        if (y !== undefined && scrollRef.current) {
          scrollRef.current.scrollTo({ y: Math.max(y - 16, 0), animated: true });
        }
        setScrolledToSection(true);
      }, 350);
      return () => clearTimeout(timer);
    }
  }, [sectionParam, matQ.data, scrolledToSection]);

  return (
    <View style={[styles.container, { paddingTop: insets.top }]}>
      <View style={styles.topRow}>
        <Pressable testID="back-btn" onPress={() => router.back()} style={styles.iconBtn}>
          <Feather name="chevron-left" size={22} color={colors.onSurface} />
        </Pressable>
        <LangToggle absolute={false} />
      </View>

      <View style={{ paddingHorizontal: spacing.xl, paddingTop: spacing.sm }}>
        <Text style={styles.eyebrow}>UNIT • {id?.toUpperCase()}</Text>
        <Text testID="chapter-title" style={styles.title}>
          {chapter ? (lang === "en" ? chapter.name_en : chapter.name_hi) : "…"}
        </Text>
      </View>

      <View style={styles.tabRow}>
        <Pressable
          testID="tab-study"
          onPress={() => setTab("study")}
          style={[styles.tab, tab === "study" && styles.tabActive]}
        >
          <Feather name="book-open" size={16} color={tab === "study" ? colors.onBrand : colors.onSurface} />
          <Text style={[styles.tabTxt, tab === "study" && styles.tabTxtActive]}>
            {tr("study_material", lang)}
          </Text>
        </Pressable>
        <Pressable
          testID="tab-quiz"
          onPress={() => setTab("quiz")}
          style={[styles.tab, tab === "quiz" && styles.tabActive]}
        >
          <Feather name="help-circle" size={16} color={tab === "quiz" ? colors.onBrand : colors.onSurface} />
          <Text style={[styles.tabTxt, tab === "quiz" && styles.tabTxtActive]}>
            {tr("mcq_quiz", lang)}
          </Text>
        </Pressable>
      </View>

      {tab === "study" ? (
        <ScrollView
          ref={scrollRef}
          contentContainerStyle={{
            paddingHorizontal: spacing.xl, paddingBottom: insets.bottom + spacing.xxl,
          }}
        >
          {matQ.isLoading && <ActivityIndicator color={colors.brand} style={{ marginTop: 32 }} />}
          {matQ.data?.sections.map((s, i) => {
            const bookmarked = bookmarkedSet.has(i);
            return (
              <View
                key={i}
                style={styles.section}
                onLayout={(e) => { sectionY.current[i] = e.nativeEvent.layout.y; }}
              >
                <View style={styles.sectionHeadRow}>
                  <Text style={styles.sectionHeading}>{lang === "en" ? s.heading_en : s.heading_hi}</Text>
                  <Pressable
                    testID={`bookmark-btn-${i}`}
                    onPress={() => toggleBookmark(i, s)}
                    style={styles.bookmarkBtn}
                    hitSlop={8}
                  >
                    <Feather name="bookmark" size={18} color={bookmarked ? colors.brand : colors.muted} />
                  </Pressable>
                </View>
                <Text style={styles.sectionBody}>{lang === "en" ? s.body_en : s.body_hi}</Text>
              </View>
            );
          })}
        </ScrollView>
      ) : (
        <View style={styles.quizPane}>
          <View style={styles.quizCard}>
            <View style={styles.quizIcon}>
              <Feather name="clipboard" size={28} color={colors.brand} />
            </View>
            <Text style={styles.quizCount}>{chapter?.question_count ?? 0}</Text>
            <Text style={styles.quizLbl}>{tr("questions_count", lang)}</Text>
            <Text style={styles.quizHint}>{tr("tap_option_hint", lang)}</Text>
          </View>

          <Pressable
            testID="start-quiz-btn"
            style={[styles.cta, { marginBottom: insets.bottom + spacing.lg }]}
            onPress={() => router.push(`/quiz/${id}`)}
          >
            <Feather name="play" size={18} color={colors.onBrand} />
            <Text style={styles.ctaText}>{tr("start_quiz", lang)}</Text>
          </Pressable>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.surface },
  topRow: {
    paddingHorizontal: spacing.lg, paddingTop: spacing.sm,
    flexDirection: "row", alignItems: "center", justifyContent: "space-between",
  },
  iconBtn: {
    width: 40, height: 40, borderRadius: 20, alignItems: "center", justifyContent: "center",
    backgroundColor: colors.surfaceSecondary, borderWidth: 1, borderColor: colors.border,
  },
  eyebrow: { color: colors.muted, fontSize: 11, letterSpacing: 2, fontWeight: "700" },
  title: {
    fontSize: 26, color: colors.onSurface, fontWeight: "700",
    marginTop: 4, lineHeight: 32,
  },
  tabRow: {
    flexDirection: "row", marginHorizontal: spacing.xl, marginTop: spacing.lg,
    backgroundColor: colors.surfaceTertiary, borderRadius: radius.pill, padding: 4,
  },
  tab: {
    flex: 1, flexDirection: "row", alignItems: "center", justifyContent: "center",
    gap: 8, paddingVertical: 10, borderRadius: radius.pill,
  },
  tabActive: { backgroundColor: colors.brand },
  tabTxt: { color: colors.onSurface, fontWeight: "600", fontSize: 13 },
  tabTxtActive: { color: colors.onBrand },
  section: { marginTop: spacing.xl },
  sectionHeadRow: {
    flexDirection: "row", alignItems: "flex-start", justifyContent: "space-between",
    gap: spacing.sm, marginBottom: spacing.sm,
  },
  sectionHeading: {
    fontSize: 18, fontWeight: "700", color: colors.onSurface,
    lineHeight: 26, flex: 1,
  },
  bookmarkBtn: {
    width: 32, height: 32, borderRadius: 16, alignItems: "center", justifyContent: "center",
    backgroundColor: colors.surfaceTertiary,
  },
  sectionBody: {
    fontSize: 15, color: colors.onSurface, lineHeight: 24, opacity: 0.92,
  },
  quizPane: { flex: 1, padding: spacing.xl, justifyContent: "space-between" },
  quizCard: {
    backgroundColor: colors.surfaceSecondary, borderWidth: 1, borderColor: colors.border,
    borderRadius: radius.lg, padding: spacing.xxl, alignItems: "center",
  },
  quizIcon: {
    width: 64, height: 64, borderRadius: 16, backgroundColor: colors.brandTertiary,
    alignItems: "center", justifyContent: "center", marginBottom: spacing.lg,
  },
  quizCount: { fontSize: 48, fontWeight: "700", color: colors.brand },
  quizLbl: { color: colors.muted, fontSize: 12, letterSpacing: 2, fontWeight: "700" },
  quizHint: { marginTop: spacing.lg, color: colors.muted, textAlign: "center" },
  cta: {
    backgroundColor: colors.brand, borderRadius: radius.md, paddingVertical: 16,
    alignItems: "center", justifyContent: "center", flexDirection: "row", gap: 10,
  },
  ctaText: { color: colors.onBrand, fontWeight: "700", fontSize: 16 },
});
