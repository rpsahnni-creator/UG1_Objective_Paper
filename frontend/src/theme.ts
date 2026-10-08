import { useMemo } from "react";
import { Appearance, StyleSheet, useColorScheme } from "react-native";

export type ColorScheme = "light" | "dark";

const light = {
  surface: "#FDFBF7",
  onSurface: "#1A1A18",
  surfaceSecondary: "#FFFFFF",
  onSurfaceSecondary: "#1A1A18",
  surfaceTertiary: "#F2EFE9",
  onSurfaceTertiary: "#1A1A18",
  surfaceInverse: "#2C2C2A",
  onSurfaceInverse: "#FDFBF7",
  muted: "#666660",

  brand: "#8C3B32",
  onBrand: "#FFFFFF",
  brandPrimary: "#8C3B32",
  onBrandPrimary: "#FFFFFF",
  brandSecondary: "#C98276",
  onBrandSecondary: "#1A1A18",
  brandTertiary: "#EADCD9",
  onBrandTertiary: "#8C3B32",

  success: "#4A7856",
  onSuccess: "#FFFFFF",
  warning: "#D49E4A",
  onWarning: "#1A1A18",
  error: "#B04A45",
  onError: "#FFFFFF",
  info: "#5C7582",
  onInfo: "#FFFFFF",

  border: "#E6E2D8",
  borderStrong: "#C2BCAC",
  divider: "#E6E2D8",
};

export type ThemeColors = typeof light;

export const defaultScheme = "light" satisfies ColorScheme;
export const themes: { light: ThemeColors; dark?: ThemeColors } = { light };

export function setColorScheme(scheme: ColorScheme | null) {
  Appearance.setColorScheme?.(scheme ?? "unspecified");
}
setColorScheme?.(themes.dark ? null : defaultScheme);

export function useTheme(): { scheme: ColorScheme; colors: ThemeColors } {
  const system = useColorScheme();
  const scheme: ColorScheme = system && themes[system] ? system : defaultScheme;
  return { scheme, colors: themes[scheme] ?? themes.light };
}

export function makeStyles<T extends StyleSheet.NamedStyles<T> | StyleSheet.NamedStyles<any>>(
  factory: (colors: ThemeColors) => T & StyleSheet.NamedStyles<any>,
): () => T {
  return function useStyles(): T {
    const { colors } = useTheme();
    return useMemo(() => StyleSheet.create(factory(colors)), [colors]);
  };
}

export const spacing = {
  xs: 4,
  sm: 8,
  md: 12,
  lg: 16,
  xl: 24,
  xxl: 32,
  xxxl: 48,
};

export const radius = {
  sm: 6,
  md: 12,
  lg: 20,
  pill: 999,
};

export const fonts = {
  display: "PlayfairDisplay_600SemiBold",
  displayBold: "PlayfairDisplay_700Bold",
  body: "System",
  bodyBold: "System",
};
