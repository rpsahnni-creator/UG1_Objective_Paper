import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Stack } from "expo-router";
import { LogBox, Platform } from "react-native";
import { SafeAreaProvider } from "react-native-safe-area-context";
import { AuthProvider } from "@/src/auth";
import { LanguageProvider } from "@/src/i18n";

LogBox.ignoreAllLogs(true);
const queryClient = new QueryClient();

// Pre-warm vector icon font on web (Expo Go handles natively)
if (Platform.OS === "web") {
  try {
    // eslint-disable-next-line @typescript-eslint/no-var-requires
    require("@react-native-vector-icons/feather");
  } catch {}
}

export default function RootLayout() {
  return (
    <SafeAreaProvider>
      <QueryClientProvider client={queryClient}>
        <LanguageProvider>
          <AuthProvider>
            <Stack screenOptions={{ headerShown: false, contentStyle: { backgroundColor: "#FDFBF7" } }} />
          </AuthProvider>
        </LanguageProvider>
      </QueryClientProvider>
    </SafeAreaProvider>
  );
}
