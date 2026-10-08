import { useEffect } from "react";
import { Pressable, StyleSheet, Text, View, ActivityIndicator } from "react-native";
import { useRouter } from "expo-router";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { Image } from "expo-image";
import { LinearGradient } from "expo-linear-gradient";
import Feather from "@react-native-vector-icons/feather";

import { useAuth } from "@/src/auth";
import { useLang, tr } from "@/src/i18n";
import { LangToggle } from "@/src/LangToggle";
import { colors, radius, spacing } from "@/src/theme-exports";

const HERO =
  "https://images.unsplash.com/photo-1528759094033-e86a2379be5f?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njl8MHwxfHNlYXJjaHwxfHx1bml2ZXJzaXR5JTIwY2FtcHVzJTIwYnVpbGRpbmclMjBhYnN0cmFjdHxlbnwwfHx8fDE3OTE0MzE2Njd8MA&ixlib=rb-4.1.0&q=85";

export default function Welcome() {
  const insets = useSafeAreaInsets();
  const router = useRouter();
  const { lang } = useLang();
  const { loginGuest, session, ready } = useAuth();

  useEffect(() => {
    if (ready && session) router.replace("/dashboard");
  }, [ready, session, router]);

  const guest = async () => {
    try {
      await loginGuest();
      router.replace("/dashboard");
    } catch {}
  };

  return (
    <View style={styles.container}>
      <Image source={{ uri: HERO }} style={StyleSheet.absoluteFillObject} contentFit="cover" />
      <LinearGradient
        colors={["rgba(26,26,24,0.1)", "rgba(26,26,24,0.6)", "rgba(26,26,24,0.95)"]}
        style={StyleSheet.absoluteFillObject}
      />
      <View style={{ paddingTop: insets.top + 4, paddingRight: spacing.lg, alignItems: "flex-end" }}>
        <LangToggle absolute={false} />
      </View>

      <View style={{ flex: 1 }} />

      <View style={[styles.bottom, { paddingBottom: insets.bottom + spacing.xl }]}>
        <Text style={styles.eyebrow}>FYUGP • SEMESTER-I</Text>
        <Text testID="welcome-title" style={styles.title}>
          {tr("app_title", lang)}
        </Text>
        <Text style={styles.subtitle}>{tr("app_subtitle", lang)}</Text>

        <Pressable testID="student-access-btn" style={styles.ctaPrimary} onPress={guest}>
          <Feather name="book-open" size={18} color={colors.onBrand} />
          <Text style={styles.ctaPrimaryText}>{tr("student_access", lang)}</Text>
        </Pressable>

        <Pressable
          testID="admin-access-btn"
          style={styles.ctaSecondary}
          onPress={() => router.push("/admin-login")}
        >
          <Feather name="shield" size={18} color={colors.surface} />
          <Text style={styles.ctaSecondaryText}>{tr("admin_access", lang)}</Text>
        </Pressable>

        {!ready && <ActivityIndicator color={colors.surface} style={{ marginTop: 12 }} />}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.surfaceInverse },
  bottom: { paddingHorizontal: spacing.xl, gap: spacing.md },
  eyebrow: {
    color: "#C98276",
    fontSize: 12,
    letterSpacing: 2,
    fontWeight: "700",
  },
  title: {
    color: "#FDFBF7",
    fontSize: 36,
    lineHeight: 44,
    fontWeight: "700",
    marginTop: spacing.sm,
  },
  subtitle: { color: "#EADCD9", fontSize: 14, marginBottom: spacing.lg },
  ctaPrimary: {
    backgroundColor: colors.brand,
    paddingVertical: 16,
    borderRadius: radius.md,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 10,
  },
  ctaPrimaryText: { color: colors.onBrand, fontSize: 16, fontWeight: "700" },
  ctaSecondary: {
    borderWidth: 1,
    borderColor: colors.surface,
    paddingVertical: 15,
    borderRadius: radius.md,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 10,
  },
  ctaSecondaryText: { color: colors.surface, fontSize: 16, fontWeight: "600" },
});
