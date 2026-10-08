import { Pressable, Text, View, StyleSheet } from "react-native";
import { useLang } from "./i18n";
import { colors, radius, spacing } from "./theme-exports";

export function LangToggle({ absolute = true }: { absolute?: boolean }) {
  const { lang, toggle } = useLang();
  return (
    <Pressable
      testID="lang-toggle"
      onPress={toggle}
      style={[styles.pill, absolute && styles.absolute]}
    >
      <Text style={[styles.txt, lang === "en" && styles.active]}>A</Text>
      <Text style={styles.sep}>/</Text>
      <Text style={[styles.txt, lang === "hi" && styles.active]}>अ</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  absolute: { position: "absolute", top: 8, right: 16, zIndex: 20 },
  pill: {
    flexDirection: "row",
    alignItems: "center",
    gap: 6,
    backgroundColor: "#FFFFFF",
    borderColor: "#C2BCAC",
    borderWidth: 1,
    borderRadius: 999,
    paddingHorizontal: 14,
    paddingVertical: 8,
  },
  txt: { fontSize: 14, color: "#666660", fontWeight: "600" },
  active: { color: "#8C3B32" },
  sep: { color: "#C2BCAC", fontSize: 14 },
});
