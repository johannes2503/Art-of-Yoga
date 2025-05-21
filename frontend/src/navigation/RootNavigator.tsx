import React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { RootStackParamList } from "../types/navigation";
import { UserRole } from "../types/auth";

// Import navigators (we'll create these next)
import AuthNavigator from "./AuthNavigator";
import InstructorNavigator from "./InstructorNavigator";
import ClientNavigator from "./ClientNavigator";

const Stack = createNativeStackNavigator<RootStackParamList>();

export default function RootNavigator() {
  // TODO: Add authentication state management
  const isAuthenticated = false;
  const userRole: UserRole = "client"; // This will come from auth state

  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        {!isAuthenticated ? (
          <Stack.Screen name="Auth" component={AuthNavigator} />
        ) : userRole === "instructor" ? (
          <Stack.Screen name="Instructor" component={InstructorNavigator} />
        ) : (
          <Stack.Screen name="Client" component={ClientNavigator} />
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}
