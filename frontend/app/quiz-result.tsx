import { useLocalSearchParams, useRouter } from "expo-router";
import { Pressable, StyleSheet, Text, View } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import Feather from "@react-native-vector-icons/feather";

import { useLang, tr } from "@/src/i18n";
import { LangToggle } from "@/src/LangToggle";
import { colors, radius, spacing } from "@/src/theme-exports";

export default function QuizResult() {
  const insets = useSafeAreaInsets();
  const router = useRouter();
  const { lang } = useLang();
  const p = useLocalSearchParams<{
    total?: string; correct?: string; wrong?: string; percent?: string; chapter_id?: string;
  }>();
  const total = parseInt(p.total || "0", 10);
  const correct = parseInt(p.correct || "0", 10);
  const wrong = parseInt(p.wrong || "0", 10);
  const percent = Math.round(parseFloat(p.percent || "0"));
  const pass = percent >= 50;

  return (
    <View style={[styles.container, { paddingTop: insets.top }]}>
      <View style={styles.topRow}>
        <View style={{ width: 40 }} />
        <LangToggle absolute={false} />
      </View>

      <View style={{ flex: 1, paddingHorizontal: spacing.xl, justifyContent: "center" }}>
        <View style={styles.badgeWrap}>
          <View style={[styles.badge, { backgroundColor: pass ? "#EEF5F0" : "#FBEAE9" }]}>
            <Feather
              name={pass ? "award" : "alert-circle"}
              size={44}
              color={pass ? colors.success : colors.error}
            />
          </View>
        </View>

        <Text testID="result-title" style={styles.title}>
          {p.chapter_id === "daily" ? tr("daily_result_badge", lang) : tr("your_score", lang)}
        </Text>
        <Text testID="result-percent" style={[styles.percent, { color: pass ? colors.success : colors.error }]}>
          {percent}%
        </Text>
        <Text style={styles.sub}>
          {correct} / {total} {tr("correct", lang)}
        </Text>

        <View style={styles.statsRow}>
          <View style={[styles.stat, { backgroundColor: "#EEF5F0", borderColor: "#CFE1D4" }]}>
            <Feather name="check" size={18} color={colors.success} />
            <Text style={styles.statNum}>{correct}</Text>
            <Text style={styles.statLbl}>{tr("correct", lang)}</Text>
          </View>
          <View style={[styles.stat, { backgroundColor: "#FBEAE9", borderColor: "#EDC2BF" }]}>
            <Feather name="x" size={18} color={colors.error} />
            <Text style={styles.statNum}>{wrong}</Text>
            <Text style={styles.statLbl}>{tr("wrong", lang)}</Text>
          </View>
        </View>
      </View>

      <View style={{ paddingHorizontal: spacing.xl, paddingBottom: insets.bottom + spacing.lg }}>
        <Pressable
          testID="back-to-chapters-btn"
          style={styles.cta}
          onPress={() => router.replace("/dashboard")}
        >
          <Feather name="home" size={18} color={colors.onBrand} />
          <Text style={styles.ctaText}>{tr("back_to_chapters", lang)}</Text>
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
  badgeWrap: { alignItems: "center", marginBottom: spacing.xl },
  badge: {
    width: 108, height: 108, borderRadius: 54, alignItems: "center", justifyContent: "center",
  },
  title: {
    textAlign: "center", color: colors.muted,
    fontSize: 12, letterSpacing: 2, fontWeight: "700",
  },
  percent: {
    textAlign: "center", fontSize: 72, fontWeight: "800", marginTop: 4,
  },
  sub: { textAlign: "center", color: colors.muted, marginBottom: spacing.xl },
  statsRow: { flexDirection: "row", gap: spacing.md },
  stat: {
    flex: 1, borderWidth: 1, borderRadius: radius.md,
    padding: spacing.lg, alignItems: "center",
  },
  statNum: { fontSize: 24, fontWeight: "700", color: colors.onSurface, marginTop: 4 },
  statLbl: { fontSize: 11, letterSpacing: 1.5, color: colors.muted, fontWeight: "700" },
  cta: {
    backgroundColor: colors.brand, borderRadius: radius.md, paddingVertical: 16,
    flexDirection: "row", alignItems: "center", justifyContent: "center", gap: 10,
  },
  ctaText: { color: colors.onBrand, fontWeight: "700", fontSize: 16 },
});
