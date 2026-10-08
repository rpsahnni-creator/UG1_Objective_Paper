import { StyleSheet, Text, View } from "react-native";
import Feather from "@react-native-vector-icons/feather";

import { colors, radius, spacing } from "@/src/theme-exports";

export type AecBlock = {
  kind: string;
  text?: string | null;
  heading?: string | null;
  items?: string[] | null;
  headers?: string[] | null;
  rows?: string[][] | null;
};

export type AecSection = { heading: string; blocks: AecBlock[] };

function Block({ block }: { block: AecBlock }) {
  switch (block.kind) {
    case "definition":
      return (
        <View style={styles.definitionBox}>
          <Text style={styles.definitionLabel}>परिभाषा</Text>
          <Text style={styles.definitionText}>{block.text}</Text>
        </View>
      );
    case "tip":
      return (
        <View style={styles.tipBox}>
          <Feather name="zap" size={14} color={colors.success} />
          <Text style={styles.tipText}>{block.text}</Text>
        </View>
      );
    case "highlight":
      return (
        <View style={styles.highlightBox}>
          <Text style={styles.highlightText}>{block.text}</Text>
        </View>
      );
    case "example":
      return (
        <View style={styles.exampleBox}>
          {block.heading && <Text style={styles.exampleHeading}>{block.heading}</Text>}
          <Text style={styles.exampleText}>{block.text}</Text>
        </View>
      );
    case "points":
      return (
        <View style={styles.listWrap}>
          {(block.items ?? []).map((item, i) => (
            <View key={i} style={styles.bulletRow}>
              <View style={styles.bulletDot} />
              <Text style={styles.listText}>{item}</Text>
            </View>
          ))}
        </View>
      );
    case "numbered":
      return (
        <View style={styles.listWrap}>
          {(block.items ?? []).map((item, i) => (
            <View key={i} style={styles.bulletRow}>
              <Text style={styles.numberLabel}>{i + 1}.</Text>
              <Text style={styles.listText}>{item}</Text>
            </View>
          ))}
        </View>
      );
    case "table":
      return (
        <View style={styles.table}>
          <View style={styles.tableHeaderRow}>
            {(block.headers ?? []).map((h, i) => (
              <Text key={i} style={styles.tableHeaderCell}>{h}</Text>
            ))}
          </View>
          {(block.rows ?? []).map((row, ri) => (
            <View key={ri} style={[styles.tableRow, ri % 2 === 1 && styles.tableRowAlt]}>
              {row.map((cell, ci) => (
                <Text key={ci} style={styles.tableCell}>{cell}</Text>
              ))}
            </View>
          ))}
        </View>
      );
    default:
      return <Text style={styles.paragraphText}>{block.text}</Text>;
  }
}

export function AecSectionRenderer({ sections }: { sections: AecSection[] }) {
  return (
    <>
      {sections.map((s, i) => (
        <View key={i} style={styles.section}>
          <Text style={styles.sectionHeading}>{s.heading}</Text>
          {s.blocks.map((b, bi) => (
            <View key={bi} style={styles.blockSpacing}>
              <Block block={b} />
            </View>
          ))}
        </View>
      ))}
    </>
  );
}

const styles = StyleSheet.create({
  section: { marginTop: spacing.xl },
  sectionHeading: {
    fontSize: 18, fontWeight: "700", color: colors.onSurface,
    marginBottom: spacing.sm, lineHeight: 26,
  },
  blockSpacing: { marginBottom: spacing.md },
  paragraphText: { fontSize: 15, color: colors.onSurface, lineHeight: 24, opacity: 0.92 },
  definitionBox: {
    backgroundColor: colors.brandTertiary, borderRadius: radius.md, padding: spacing.lg,
    borderLeftWidth: 3, borderLeftColor: colors.brand,
  },
  definitionLabel: { color: colors.brand, fontSize: 11, fontWeight: "700", letterSpacing: 1.5, marginBottom: 4 },
  definitionText: { color: colors.onSurface, fontSize: 15, lineHeight: 23 },
  tipBox: {
    flexDirection: "row", alignItems: "flex-start", gap: spacing.sm,
    backgroundColor: "#EEF5F0", borderRadius: radius.md, padding: spacing.lg,
  },
  tipText: { flex: 1, color: colors.onSurface, fontSize: 14, lineHeight: 21 },
  highlightBox: {
    backgroundColor: "#FBF0E1", borderRadius: radius.md, padding: spacing.lg,
    borderWidth: 1, borderColor: "#E8CFA0",
  },
  highlightText: { color: colors.onSurface, fontSize: 15, lineHeight: 23, fontWeight: "600" },
  exampleBox: {
    backgroundColor: colors.surfaceTertiary, borderRadius: radius.md, padding: spacing.lg,
  },
  exampleHeading: { color: colors.muted, fontSize: 11, fontWeight: "700", letterSpacing: 1, marginBottom: 6 },
  exampleText: { color: colors.onSurface, fontSize: 14, lineHeight: 22 },
  listWrap: { gap: spacing.sm },
  bulletRow: { flexDirection: "row", gap: spacing.sm, alignItems: "flex-start" },
  bulletDot: {
    width: 6, height: 6, borderRadius: 3, backgroundColor: colors.brand, marginTop: 8,
  },
  numberLabel: { color: colors.brand, fontWeight: "700", fontSize: 14, width: 20 },
  listText: { flex: 1, color: colors.onSurface, fontSize: 15, lineHeight: 23 },
  table: {
    borderWidth: 1, borderColor: colors.border, borderRadius: radius.md, overflow: "hidden",
  },
  tableHeaderRow: { flexDirection: "row", backgroundColor: colors.brandTertiary },
  tableHeaderCell: {
    flex: 1, padding: spacing.sm, fontSize: 12, fontWeight: "700", color: colors.brand,
  },
  tableRow: { flexDirection: "row", borderTopWidth: 1, borderTopColor: colors.border },
  tableRowAlt: { backgroundColor: colors.surfaceTertiary },
  tableCell: { flex: 1, padding: spacing.sm, fontSize: 13, color: colors.onSurface, lineHeight: 19 },
});
