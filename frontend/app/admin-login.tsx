import { useState } from "react";
import {
  View, Text, Pressable, StyleSheet, TextInput, KeyboardAvoidingView, Platform, ActivityIndicator,
} from "react-native";
import { useRouter } from "expo-router";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import Feather from "@react-native-vector-icons/feather";

import { useAuth } from "@/src/auth";
import { useLang, tr } from "@/src/i18n";
import { LangToggle } from "@/src/LangToggle";
import { colors, radius, spacing } from "@/src/theme-exports";

export default function AdminLogin() {
  const insets = useSafeAreaInsets();
  const router = useRouter();
  const { lang } = useLang();
  const { loginAdmin } = useAuth();
  const [u, setU] = useState("kijitechnology@gmail.com");
  const [p, setP] = useState("");
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  const submit = async () => {
    setErr(null);
    setLoading(true);
    try {
      await loginAdmin(u.trim(), p);
      router.replace("/dashboard");
    } catch {
      setErr(tr("invalid_cred", lang));
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === "ios" ? "padding" : undefined}
    >
      <View style={{ paddingTop: insets.top + spacing.sm }}>
        <View style={styles.topRow}>
          <Pressable testID="back-btn" onPress={() => router.back()} style={styles.backBtn}>
            <Feather name="chevron-left" size={22} color={colors.onSurface} />
          </Pressable>
          <LangToggle absolute={false} />
        </View>
      </View>

      <View style={styles.main}>
        <Text style={styles.heading}>{tr("admin_access", lang)}</Text>
        <Text style={styles.sub}>
          {lang === "en"
            ? "Free access to all content for administrators."
            : "व्यवस्थापकों के लिए सभी सामग्री तक मुफ़्त पहुँच।"}
        </Text>

        <View style={styles.field}>
          <Text style={styles.label}>{tr("username", lang)}</Text>
          <TextInput
            testID="admin-username"
            style={styles.input}
            value={u}
            onChangeText={setU}
            autoCapitalize="none"
            keyboardType="email-address"
            placeholderTextColor={colors.muted}
          />
        </View>

        <View style={styles.field}>
          <Text style={styles.label}>{tr("password", lang)}</Text>
          <TextInput
            testID="admin-password"
            style={styles.input}
            value={p}
            onChangeText={setP}
            secureTextEntry
            placeholderTextColor={colors.muted}
          />
        </View>

        {err && <Text testID="login-error" style={styles.err}>{err}</Text>}

        <Pressable testID="login-submit-btn" style={styles.cta} onPress={submit} disabled={loading}>
          {loading ? (
            <ActivityIndicator color={colors.onBrand} />
          ) : (
            <Text style={styles.ctaText}>{tr("login", lang)}</Text>
          )}
        </Pressable>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.surface },
  topRow: {
    paddingHorizontal: spacing.lg,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },
  backBtn: {
    width: 40, height: 40, borderRadius: 20, alignItems: "center",
    justifyContent: "center", backgroundColor: colors.surfaceSecondary,
    borderWidth: 1, borderColor: colors.border,
  },
  main: { flex: 1, paddingHorizontal: spacing.xl, justifyContent: "center" },
  heading: {
    fontSize: 32, fontWeight: "700", color: colors.onSurface, marginBottom: spacing.sm,
  },
  sub: { color: colors.muted, fontSize: 14, marginBottom: spacing.xxl },
  field: { marginBottom: spacing.lg },
  label: { fontSize: 12, letterSpacing: 1.5, color: colors.muted, marginBottom: 6, fontWeight: "700" },
  input: {
    backgroundColor: colors.surfaceSecondary,
    borderWidth: 1, borderColor: colors.border,
    borderRadius: radius.md, padding: 14, fontSize: 16, color: colors.onSurface,
  },
  err: { color: colors.error, marginBottom: spacing.sm, fontSize: 13 },
  cta: {
    marginTop: spacing.md,
    backgroundColor: colors.brand,
    borderRadius: radius.md,
    paddingVertical: 16,
    alignItems: "center",
  },
  ctaText: { color: colors.onBrand, fontWeight: "700", fontSize: 16 },
});
