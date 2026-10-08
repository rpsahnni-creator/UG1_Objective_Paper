import { useQuery } from "@tanstack/react-query";
import { ActivityIndicator, FlatList, Pressable, StyleSheet, Text, View } from "react-native";
import { useRouter } from "expo-router";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import Feather from "@react-native-vector-icons/feather";

import { apiGet, useAuth } from "@/src/auth";
import { useLang, tr } from "@/src/i18n";
import { LangToggle } from "@/src/LangToggle";
import { colors, radius, spacing } from "@/src/theme-exports";

type Chapter = {
  id: string;
  name_en: string;
  name_hi: string;
  icon: string;
  description_en: string;
  description_hi: string;
  question_count: number;
};

const ICON_MAP: Record<string, string> = { cpu: "cpu", "hard-drive": "hard-drive", wifi: "wifi" };

export default function Dashboard() {
  const insets = useSafeAreaInsets();
  const router = useRouter();
  const { lang } = useLang();
  const { session, logout } = useAuth();

  const { data, isLoading, error, refetch } = useQuery<Chapter[]>({
    queryKey: ["chapters"],
    queryFn: () => apiGet<Chapter[]>("/api/chapters", session?.token),
  });

  const totalQ = (data ?? []).reduce((s, c) => s + c.question_count, 0);

  return (
    <View style={[styles.container, { paddingTop: insets.top }]}>
      <View style={styles.topRow}>
        <Pressable testID="logout-btn" onPress={async () => { await logout(); router.replace("/"); }} style={styles.iconBtn}>
          <Feather name="log-out" size={18} color={colors.onSurface} />
        </Pressable>
        <LangToggle absolute={false} />
      </View>

      <FlatList
        data={data ?? []}
        keyExtractor={(c) => c.id}
        contentContainerStyle={{ padding: spacing.xl, paddingBottom: insets.bottom + spacing.xxl }}
        ListHeaderComponent={
          <View style={{ marginBottom: spacing.xl }}>
            <Text style={styles.eyebrow}>{tr("course_overview", lang).toUpperCase()}</Text>
            <Text testID="dashboard-title" style={styles.title}>
              {tr("app_title", lang)}
            </Text>
            <View style={styles.statRow}>
              <View style={styles.statChip}>
                <Text style={styles.statNum}>{data?.length ?? 0}</Text>
                <Text style={styles.statLbl}>{tr("chapters", lang)}</Text>
              </View>
              <View style={styles.statChip}>
                <Text style={styles.statNum}>{totalQ}</Text>
                <Text style={styles.statLbl}>{tr("questions_count", lang)}</Text>
              </View>
              {session?.isAdmin && (
                <View style={[styles.statChip, { backgroundColor: colors.brand }]}>
                  <Feather name="shield" size={14} color={colors.onBrand} />
                  <Text style={[styles.statLbl, { color: colors.onBrand, marginTop: 2 }]}>
                    {tr("admin_tag", lang)}
                  </Text>
                </View>
              )}
            </View>
          </View>
        }
        renderItem={({ item }) => (
          <Pressable
            testID={`chapter-card-${item.id}`}
            style={styles.card}
            onPress={() => router.push(`/chapter/${item.id}`)}
          >
            <View style={styles.iconWrap}>
              <Feather name={ICON_MAP[item.icon] || "book"} size={24} color={colors.brand} />
            </View>
            <View style={{ flex: 1 }}>
              <Text style={styles.cardTitle}>
                {lang === "en" ? item.name_en : item.name_hi}
              </Text>
              <Text style={styles.cardDesc} numberOfLines={2}>
                {lang === "en" ? item.description_en : item.description_hi}
              </Text>
              <View style={styles.metaRow}>
                <Feather name="list" size={12} color={colors.muted} />
                <Text style={styles.meta}>
                  {item.question_count} {tr("questions_count", lang)}
                </Text>
              </View>
            </View>
            <Feather name="chevron-right" size={22} color={colors.muted} />
          </Pressable>
        )}
        ListEmptyComponent={
          isLoading ? (
            <ActivityIndicator color={colors.brand} />
          ) : error ? (
            <View style={{ alignItems: "center", padding: spacing.xl }}>
              <Text style={{ color: colors.error }}>{tr("failed", lang)}</Text>
              <Pressable onPress={() => refetch()} style={styles.retry} testID="dashboard-retry">
                <Text style={{ color: colors.onBrand, fontWeight: "600" }}>{tr("retry", lang)}</Text>
              </Pressable>
            </View>
          ) : null
        }
      />
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
  title: { fontSize: 30, lineHeight: 36, color: colors.onSurface, fontWeight: "700", marginTop: 4 },
  statRow: { flexDirection: "row", gap: spacing.md, marginTop: spacing.lg },
  statChip: {
    backgroundColor: colors.surfaceTertiary, paddingHorizontal: 16, paddingVertical: 10,
    borderRadius: radius.md, alignItems: "center", minWidth: 72,
  },
  statNum: { color: colors.brand, fontSize: 22, fontWeight: "700" },
  statLbl: { color: colors.muted, fontSize: 11, letterSpacing: 1 },
  card: {
    flexDirection: "row", alignItems: "center", gap: spacing.lg,
    backgroundColor: colors.surfaceSecondary, borderWidth: 1, borderColor: colors.border,
    borderRadius: radius.lg, padding: spacing.lg, marginBottom: spacing.md,
  },
  iconWrap: {
    width: 48, height: 48, borderRadius: 12,
    backgroundColor: colors.brandTertiary, alignItems: "center", justifyContent: "center",
  },
  cardTitle: { color: colors.onSurface, fontSize: 16, fontWeight: "700", lineHeight: 22 },
  cardDesc: { color: colors.muted, fontSize: 13, marginTop: 4, lineHeight: 18 },
  metaRow: { flexDirection: "row", alignItems: "center", gap: 4, marginTop: 8 },
  meta: { color: colors.muted, fontSize: 12 },
  retry: {
    marginTop: 12, paddingHorizontal: 20, paddingVertical: 10,
    backgroundColor: colors.brand, borderRadius: radius.md,
  },
});
