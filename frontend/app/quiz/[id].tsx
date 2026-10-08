import { useMemo, useState } from "react";
import { useLocalSearchParams, useRouter } from "expo-router";
import { useQuery } from "@tanstack/react-query";
import {
  ActivityIndicator, Pressable, ScrollView, StyleSheet, Text, View,
} from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import Feather from "@react-native-vector-icons/feather";

import { apiGet, apiPost, useAuth } from "@/src/auth";
import { useLang, tr } from "@/src/i18n";
import { LangToggle } from "@/src/LangToggle";
import { colors, radius, spacing } from "@/src/theme-exports";

type MCQ = {
  id: string;
  chapter_id: string;
  question_en: string;
  question_hi: string;
  options_en: string[];
  options_hi: string[];
  answer_index: number;
  explanation_en: string;
  explanation_hi: string;
  difficulty: string;
};

export default function Quiz() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const insets = useSafeAreaInsets();
  const router = useRouter();
  const { lang } = useLang();
  const { session } = useAuth();

  const q = useQuery<MCQ[]>({
    queryKey: ["mcqs", id],
    queryFn: () => apiGet<MCQ[]>(`/api/chapters/${id}/mcqs?limit=50`, session?.token),
    enabled: !!id,
  });

  const questions = useMemo(() => q.data ?? [], [q.data]);
  const [idx, setIdx] = useState(0);
  const [selected, setSelected] = useState<Record<string, number>>({});
  const [submitting, setSubmitting] = useState(false);

  const cur = questions[idx];
  const picked = cur ? selected[cur.id] : undefined;

  const next = async () => {
    if (idx < questions.length - 1) {
      setIdx(idx + 1);
      return;
    }
    try {
      setSubmitting(true);
      const answers = Object.entries(selected).map(([question_id, selectedIdx]) => ({
        question_id, selected: selectedIdx,
      }));
      const res = await apiPost<any>(
        "/api/quiz/submit",
        { chapter_id: id, answers },
        session?.token,
      );
      router.replace({
        pathname: "/quiz-result",
        params: {
          chapter_id: String(id),
          total: String(res.total),
          correct: String(res.correct),
          wrong: String(res.wrong),
          percent: String(res.percent),
        },
      });
    } finally {
      setSubmitting(false);
    }
  };

  if (q.isLoading) {
    return (
      <View style={[styles.container, { paddingTop: insets.top, justifyContent: "center" }]}>
        <ActivityIndicator color={colors.brand} />
      </View>
    );
  }
  if (!cur) {
    return (
      <View style={[styles.container, { paddingTop: insets.top, justifyContent: "center", alignItems: "center" }]}>
        <Text style={{ color: colors.muted }}>{tr("failed", lang)}</Text>
      </View>
    );
  }

  const pct = ((idx + 1) / questions.length) * 100;
  const correctIdx = cur.answer_index;
  const answered = picked !== undefined;

  return (
    <View style={[styles.container, { paddingTop: insets.top }]}>
      <View style={styles.topRow}>
        <Pressable testID="back-btn" onPress={() => router.back()} style={styles.iconBtn}>
          <Feather name="x" size={22} color={colors.onSurface} />
        </Pressable>
        <LangToggle absolute={false} />
      </View>

      <View style={styles.progressWrap}>
        <View style={styles.progressBg}>
          <View style={[styles.progressFill, { width: `${pct}%` }]} />
        </View>
        <Text style={styles.progressTxt}>
          {tr("question", lang)} {idx + 1} {tr("of", lang)} {questions.length}
        </Text>
      </View>

      <ScrollView
        contentContainerStyle={{
          paddingHorizontal: spacing.xl, paddingBottom: 140,
        }}
      >
        <Text style={styles.difficulty}>{cur.difficulty.toUpperCase()}</Text>
        <Text testID="question-text" style={styles.question}>
          {lang === "en" ? cur.question_en : cur.question_hi}
        </Text>

        {(lang === "en" ? cur.options_en : cur.options_hi).map((opt, i) => {
          const isPicked = picked === i;
          const isCorrect = answered && i === correctIdx;
          const isWrongPick = answered && isPicked && i !== correctIdx;
          return (
            <Pressable
              key={i}
              testID={`option-${i}`}
              disabled={answered}
              onPress={() => setSelected({ ...selected, [cur.id]: i })}
              style={[
                styles.opt,
                isPicked && !answered && styles.optPicked,
                isCorrect && styles.optCorrect,
                isWrongPick && styles.optWrong,
              ]}
            >
              <View
                style={[
                  styles.optDot,
                  isPicked && !answered && { borderColor: colors.brand, backgroundColor: colors.brand },
                  isCorrect && { borderColor: colors.success, backgroundColor: colors.success },
                  isWrongPick && { borderColor: colors.error, backgroundColor: colors.error },
                ]}
              >
                <Text style={styles.optLetter}>{String.fromCharCode(65 + i)}</Text>
              </View>
              <Text style={styles.optTxt}>{opt}</Text>
              {isCorrect && <Feather name="check" size={18} color={colors.success} />}
              {isWrongPick && <Feather name="x" size={18} color={colors.error} />}
            </Pressable>
          );
        })}

        {answered && (
          <View testID="explanation-card" style={styles.explain}>
            <Text style={styles.explainLbl}>{tr("explanation", lang)}</Text>
            <Text style={styles.explainTxt}>
              {lang === "en" ? cur.explanation_en : cur.explanation_hi}
            </Text>
          </View>
        )}
      </ScrollView>

      <View style={[styles.bottomBar, { paddingBottom: insets.bottom + spacing.md }]}>
        <Pressable
          testID="next-btn"
          onPress={next}
          disabled={!answered || submitting}
          style={[styles.cta, (!answered || submitting) && { opacity: 0.5 }]}
        >
          {submitting ? (
            <ActivityIndicator color={colors.onBrand} />
          ) : (
            <>
              <Text style={styles.ctaText}>
                {idx === questions.length - 1 ? tr("submit", lang) : tr("next", lang)}
              </Text>
              <Feather name="arrow-right" size={18} color={colors.onBrand} />
            </>
          )}
        </Pressable>
      </View>
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
  progressWrap: { paddingHorizontal: spacing.xl, paddingTop: spacing.md },
  progressBg: {
    height: 4, backgroundColor: colors.surfaceTertiary, borderRadius: 2, overflow: "hidden",
  },
  progressFill: { height: 4, backgroundColor: colors.brand },
  progressTxt: {
    marginTop: 8, color: colors.muted, fontSize: 12, letterSpacing: 1, fontWeight: "700",
  },
  difficulty: {
    marginTop: spacing.lg, color: colors.brand, fontSize: 11, letterSpacing: 2, fontWeight: "700",
  },
  question: {
    fontSize: 22, color: colors.onSurface, fontWeight: "700", lineHeight: 30,
    marginTop: spacing.sm, marginBottom: spacing.xl,
  },
  opt: {
    flexDirection: "row", alignItems: "center", gap: spacing.md,
    backgroundColor: colors.surfaceSecondary, borderWidth: 1, borderColor: colors.border,
    borderRadius: radius.md, padding: spacing.lg, marginBottom: spacing.md,
  },
  optPicked: { borderColor: colors.brand, backgroundColor: colors.brandTertiary },
  optCorrect: { borderColor: colors.success, backgroundColor: "#EEF5F0" },
  optWrong: { borderColor: colors.error, backgroundColor: "#FBEAE9" },
  optDot: {
    width: 30, height: 30, borderRadius: 15, borderWidth: 1.5,
    borderColor: colors.borderStrong, alignItems: "center", justifyContent: "center",
  },
  optLetter: { color: colors.onSurface, fontWeight: "700" },
  optTxt: { flex: 1, fontSize: 15, color: colors.onSurface, lineHeight: 22 },
  explain: {
    marginTop: spacing.md, padding: spacing.lg,
    backgroundColor: colors.brandTertiary, borderRadius: radius.md,
    borderLeftWidth: 3, borderLeftColor: colors.brand,
  },
  explainLbl: {
    color: colors.brand, fontSize: 11, letterSpacing: 2, fontWeight: "700", marginBottom: 6,
  },
  explainTxt: { color: colors.onSurface, fontSize: 14, lineHeight: 22 },
  bottomBar: {
    paddingHorizontal: spacing.xl, paddingTop: spacing.md,
    borderTopWidth: 1, borderTopColor: colors.border, backgroundColor: colors.surface,
  },
  cta: {
    backgroundColor: colors.brand, borderRadius: radius.md, paddingVertical: 16,
    flexDirection: "row", alignItems: "center", justifyContent: "center", gap: 8,
  },
  ctaText: { color: colors.onBrand, fontWeight: "700", fontSize: 16 },
});
