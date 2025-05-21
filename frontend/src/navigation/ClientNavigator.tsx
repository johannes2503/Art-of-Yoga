import React from "react";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { ClientStackParamList } from "../types/navigation";

// Import screens (we'll create these next)
import DashboardScreen from "../screens/client/DashboardScreen";
import RoutineDetailsScreen from "../screens/client/RoutineDetailsScreen";
import ProfileScreen from "../screens/client/ProfileScreen";
import ProgressScreen from "../screens/client/ProgressScreen";

const Stack = createNativeStackNavigator<ClientStackParamList>();

export default function ClientNavigator() {
  return (
    <Stack.Navigator
      screenOptions={{
        headerShown: true,
        headerStyle: {
          backgroundColor: "#10B981", // secondary color
        },
        headerTintColor: "#fff",
        headerTitleStyle: {
          fontWeight: "bold",
        },
      }}
    >
      <Stack.Screen
        name="Dashboard"
        component={DashboardScreen}
        options={{ title: "My Routines" }}
      />
      <Stack.Screen
        name="RoutineDetails"
        component={RoutineDetailsScreen}
        options={{ title: "Routine Details" }}
      />
      <Stack.Screen
        name="Profile"
        component={ProfileScreen}
        options={{ title: "My Profile" }}
      />
      <Stack.Screen
        name="Progress"
        component={ProgressScreen}
        options={{ title: "My Progress" }}
      />
    </Stack.Navigator>
  );
}
