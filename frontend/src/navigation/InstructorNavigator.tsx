import React from "react";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { InstructorStackParamList } from "../types/navigation";

// Import screens (we'll create these next)
import DashboardScreen from "../screens/instructor/DashboardScreen";
import CreateRoutineScreen from "../screens/instructor/CreateRoutineScreen";
import EditRoutineScreen from "../screens/instructor/EditRoutineScreen";
import ClientListScreen from "../screens/instructor/ClientListScreen";
import ClientDetailsScreen from "../screens/instructor/ClientDetailsScreen";
import ProfileScreen from "../screens/instructor/ProfileScreen";

const Stack = createNativeStackNavigator<InstructorStackParamList>();

export default function InstructorNavigator() {
  return (
    <Stack.Navigator
      screenOptions={{
        headerShown: true,
        headerStyle: {
          backgroundColor: "#4F46E5", // primary color
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
        options={{ title: "Instructor Dashboard" }}
      />
      <Stack.Screen
        name="CreateRoutine"
        component={CreateRoutineScreen}
        options={{ title: "Create Routine" }}
      />
      <Stack.Screen
        name="EditRoutine"
        component={EditRoutineScreen}
        options={{ title: "Edit Routine" }}
      />
      <Stack.Screen
        name="ClientList"
        component={ClientListScreen}
        options={{ title: "My Clients" }}
      />
      <Stack.Screen
        name="ClientDetails"
        component={ClientDetailsScreen}
        options={{ title: "Client Details" }}
      />
      <Stack.Screen
        name="Profile"
        component={ProfileScreen}
        options={{ title: "My Profile" }}
      />
    </Stack.Navigator>
  );
}
