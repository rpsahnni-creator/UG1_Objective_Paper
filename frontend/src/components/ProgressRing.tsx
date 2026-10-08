import { StyleSheet, Text, View } from "react-native";
import Svg, { Circle } from "react-native-svg";

import { colors } from "@/src/theme-exports";

type Props = {
  percent: number;
  size?: number;
  strokeWidth?: number;
  showValue?: boolean;
};

export function ProgressRing({ percent, size = 48, strokeWidth = 4, showValue = true }: Props) {
  const r = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * r;
  const clamped = Math.max(0, Math.min(100, percent));
  const offset = circumference * (1 - clamped / 100);
  const color = clamped === 0 ? colors.borderStrong : clamped >= 75 ? colors.success : clamped >= 40 ? colors.brand : colors.error;

  return (
    <View style={{ width: size, height: size, alignItems: "center", justifyContent: "center" }}>
      <Svg width={size} height={size}>
        <Circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          stroke={colors.border}
          strokeWidth={strokeWidth}
          fill="none"
        />
        {clamped > 0 && (
          <Circle
            cx={size / 2}
            cy={size / 2}
            r={r}
            stroke={color}
            strokeWidth={strokeWidth}
            fill="none"
            strokeDasharray={`${circumference} ${circumference}`}
            strokeDashoffset={offset}
            strokeLinecap="round"
            transform={`rotate(-90 ${size / 2} ${size / 2})`}
          />
        )}
      </Svg>
      {showValue && (
        <View style={StyleSheet.absoluteFillObject}>
          <View style={styles.center}>
            <Text style={{ fontSize: size * 0.28, fontWeight: "700", color: colors.onSurface }}>
              {Math.round(clamped)}
            </Text>
          </View>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  center: { flex: 1, alignItems: "center", justifyContent: "center" },
});
