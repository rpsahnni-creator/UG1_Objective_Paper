import { useQuery } from "@tanstack/react-query";
import { ActivityIndicator, Pressable, ScrollView, StyleSheet, Text, View } from "react-native";
import { useLocalSearchParams, useRouter } from "expo-router";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import Feather from "@react-native-vector-icons/feather";

import { apiGet } from "@/src/auth";
import { AecSectionRenderer, AecSection } from "@/src/components/AecBlockRenderer";
import { colors, radius, spacing } from "@/src/theme-exports";

type AecTopic = {
  slug: string;
  unit: number;
  title: string;
  subtitle: string;
  icon?: string;
  question_count: number;
  sections: AecSection[];
};

export default function AecTopicDetail() {
  const { slug } = useLocalSearchParams<{ slug: string }>();
  const insets = useSafeAreaInsets();
  const router = useRouter();

  const topicQ = useQuery<AecTopic>({
    queryKey: ["aec-topic", slug],
    queryFn: () => apiGet<AecTopic>(`/api/aec/topics/${slug}`),
    enabled: !!slug,
  });

  return (
    <View style={[styles.container, { paddingTop: insets.top }]}>
      <View style={styles.topRow}>
        <Pressable testID="aec-back-btn" onPress={() => router.back()} style={styles.iconBtn}>
          <Feather name="chevron-left" size={22} color={colors.onSurface} />
        </Pressable>
        <View style={styles.aecBadge}>
          <Text style={styles.aecBadgeText}>AEC हिंदी</Text>
        </View>
      </View>

      {topicQ.isLoading ? (
        <ActivityIndicator color={colors.brand} style={{ marginTop: 60 }} />
      ) : !topicQ.data ? (
        <View style={{ padding: spacing.xl }}>
          <Text style={{ color: colors.error }}>कुछ गलत हुआ।</Text>
        </View>
      ) : (
        <>
          <View style={{ paddingHorizontal: spacing.xl, paddingTop: spacing.sm }}>
            <Text style={styles.eyebrow}>यूनिट {topicQ.data.unit}</Text>
            <Text testID="aec-topic-title" style={styles.title}>{topicQ.data.title}</Text>
            <Text style={styles.subtitle}>{topicQ.data.subtitle}</Text>
          </View>

          <ScrollView
            contentContainerStyle={{
              paddingHorizontal: spacing.xl, paddingBottom: insets.bottom + spacing.xxl,
            }}
          >
            <AecSectionRenderer sections={topicQ.data.sections} />
          </ScrollView>

          {topicQ.data.question_count > 0 && (
            <View style={[styles.bottomBar, { paddingBottom: insets.bottom + spacing.md }]}>
              <Pressable
                testID="aec-start-quiz-btn"
                style={styles.cta}
                onPress={() => router.push(`/quiz/${slug}`)}
              >
                <Feather name="play" size={18} color={colors.onBrand} />
                <Text style={styles.ctaText}>
                  क्विज़ शुरू करें ({topicQ.data.question_count} प्रश्न)
                </Text>
              </Pressable>
            </View>
          )}
        </>
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
  aecBadge: {
    backgroundColor: colors.brandTertiary, paddingHorizontal: 12, paddingVertical: 8,
    borderRadius: radius.pill,
  },
  aecBadgeText: { color: colors.brand, fontSize: 12, fontWeight: "700" },
  eyebrow: { color: colors.muted, fontSize: 11, letterSpacing: 2, fontWeight: "700" },
  title: { fontSize: 24, color: colors.onSurface, fontWeight: "700", marginTop: 4, lineHeight: 30 },
  subtitle: { color: colors.muted, fontSize: 13, marginTop: 6, lineHeight: 19 },
  bottomBar: {
    paddingHorizontal: spacing.xl, paddingTop: spacing.md,
    borderTopWidth: 1, borderTopColor: colors.border, backgroundColor: colors.surface,
  },
  cta: {
    backgroundColor: colors.brand, borderRadius: radius.md, paddingVertical: 16,
    flexDirection: "row", alignItems: "center", justifyContent: "center", gap: 10,
  },
  ctaText: { color: colors.onBrand, fontWeight: "700", fontSize: 15 },
});
