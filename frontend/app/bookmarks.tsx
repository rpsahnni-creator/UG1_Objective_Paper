import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { ActivityIndicator, FlatList, Pressable, StyleSheet, Text, View } from "react-native";
import { useRouter } from "expo-router";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import Feather from "@react-native-vector-icons/feather";

import { apiDelete, apiGet, useAuth } from "@/src/auth";
import { useLang, tr } from "@/src/i18n";
import { LangToggle } from "@/src/LangToggle";
import { colors, radius, spacing } from "@/src/theme-exports";

type Bookmark = {
  id: string;
  chapter_id: string;
  chapter_name_en: string;
  chapter_name_hi: string;
  section_index: number;
  heading_en: string;
  heading_hi: string;
  created_at: string;
};

export default function Bookmarks() {
  const insets = useSafeAreaInsets();
  const router = useRouter();
  const { lang } = useLang();
  const { session } = useAuth();
  const qc = useQueryClient();

  const bq = useQuery<Bookmark[]>({
    queryKey: ["bookmarks"],
    queryFn: () => apiGet<Bookmark[]>("/api/bookmarks", session?.token),
    enabled: !!session?.token,
  });

  const removeMut = useMutation({
    mutationFn: (b: Bookmark) => apiDelete(`/api/bookmarks/${b.chapter_id}/${b.section_index}`, session?.token),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["bookmarks"] }),
  });

  return (
    <View style={[styles.container, { paddingTop: insets.top }]}>
      <View style={styles.topRow}>
        <Pressable testID="back-btn" onPress={() => router.back()} style={styles.iconBtn}>
          <Feather name="chevron-left" size={22} color={colors.onSurface} />
        </Pressable>
        <LangToggle absolute={false} />
      </View>

      <View style={{ paddingHorizontal: spacing.xl, paddingTop: spacing.sm }}>
        <Text style={styles.eyebrow}>{tr("bookmarks", lang).toUpperCase()}</Text>
        <Text testID="bookmarks-title" style={styles.title}>{tr("bookmarks", lang)}</Text>
      </View>

      <FlatList
        data={bq.data ?? []}
        keyExtractor={(b) => b.id}
        contentContainerStyle={{ padding: spacing.xl, paddingBottom: insets.bottom + spacing.xxl }}
        renderItem={({ item }) => (
          <Pressable
            testID={`bookmark-item-${item.id}`}
            style={styles.card}
            onPress={() => router.push(`/chapter/${item.chapter_id}?section=${item.section_index}`)}
          >
            <View style={styles.iconWrap}>
              <Feather name="bookmark" size={18} color={colors.brand} />
            </View>
            <View style={{ flex: 1 }}>
              <Text style={styles.cardChapter}>
                {lang === "en" ? item.chapter_name_en : item.chapter_name_hi}
              </Text>
              <Text style={styles.cardTitle} numberOfLines={2}>
                {lang === "en" ? item.heading_en : item.heading_hi}
              </Text>
            </View>
            <Pressable
              testID={`remove-bookmark-${item.id}`}
              onPress={() => removeMut.mutate(item)}
              style={styles.trashBtn}
              hitSlop={8}
            >
              <Feather name="trash-2" size={16} color={colors.error} />
            </Pressable>
          </Pressable>
        )}
        ListEmptyComponent={
          bq.isLoading ? (
            <ActivityIndicator color={colors.brand} style={{ marginTop: 40 }} />
          ) : (
            <View style={{ alignItems: "center", padding: spacing.xxl }}>
              <Feather name="bookmark" size={40} color={colors.border} />
              <Text style={{ color: colors.muted, marginTop: spacing.md, textAlign: "center" }}>
                {tr("no_bookmarks", lang)}
              </Text>
            </View>
          )
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
  title: { fontSize: 26, color: colors.onSurface, fontWeight: "700", marginTop: 4, lineHeight: 32 },
  card: {
    flexDirection: "row", alignItems: "center", gap: spacing.md,
    backgroundColor: colors.surfaceSecondary, borderWidth: 1, borderColor: colors.border,
    borderRadius: radius.lg, padding: spacing.lg, marginBottom: spacing.md,
  },
  iconWrap: {
    width: 40, height: 40, borderRadius: 12,
    backgroundColor: colors.brandTertiary, alignItems: "center", justifyContent: "center",
  },
  cardChapter: { color: colors.muted, fontSize: 11, letterSpacing: 1, fontWeight: "700", marginBottom: 2 },
  cardTitle: { color: colors.onSurface, fontSize: 15, fontWeight: "700", lineHeight: 20 },
  trashBtn: {
    width: 32, height: 32, borderRadius: 16, alignItems: "center", justifyContent: "center",
    backgroundColor: "#FBEAE9",
  },
});
