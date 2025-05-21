import React from "react";
import { View, Text, ScrollView, TouchableOpacity } from "react-native";
import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { ClientStackParamList } from "../../types/navigation";

type Props = NativeStackScreenProps<ClientStackParamList, "Dashboard">;

// Temporary mock data - will be replaced with API data
const mockData = {
  totalRoutines: 5,
  completedRoutines: 2,
  recentRoutines: [
    {
      id: "1",
      name: "Morning Flow",
      instructor: "Sarah Johnson",
      duration: "30 min",
      difficulty: "beginner",
      lastCompleted: "2024-03-20",
      isCompleted: true,
    },
    {
      id: "2",
      name: "Evening Stretch",
      instructor: "Sarah Johnson",
      duration: "20 min",
      difficulty: "beginner",
      lastCompleted: null,
      isCompleted: false,
    },
    {
      id: "3",
      name: "Breathing Practice",
      instructor: "Sarah Johnson",
      duration: "15 min",
      difficulty: "beginner",
      lastCompleted: "2024-03-19",
      isCompleted: true,
    },
  ],
  upcomingRoutines: [
    {
      id: "4",
      name: "Weekend Flow",
      instructor: "Sarah Johnson",
      duration: "45 min",
      difficulty: "intermediate",
      scheduledFor: "2024-03-23",
    },
  ],
};

export default function DashboardScreen({ navigation }: Props) {
  return (
    <ScrollView className="flex-1 bg-background">
      <View className="p-4">
        {/* Progress Overview */}
        <View className="flex-row space-x-4 mb-6">
          <View className="flex-1 bg-white p-4 rounded-lg shadow-sm">
            <Text className="text-2xl font-bold text-primary mb-1">
              {mockData.completedRoutines}/{mockData.totalRoutines}
            </Text>
            <Text className="text-gray-600">Completed Routines</Text>
          </View>
          <View className="flex-1 bg-white p-4 rounded-lg shadow-sm">
            <Text className="text-2xl font-bold text-primary mb-1">
              {Math.round(
                (mockData.completedRoutines / mockData.totalRoutines) * 100
              )}
              %
            </Text>
            <Text className="text-gray-600">Completion Rate</Text>
          </View>
        </View>

        {/* Recent Routines */}
        <View className="bg-white rounded-lg shadow-sm p-4 mb-6">
          <Text className="text-lg font-semibold mb-4">Recent Routines</Text>
          {mockData.recentRoutines.map((routine) => (
            <TouchableOpacity
              key={routine.id}
              className="flex-row items-center justify-between py-3 border-b border-gray-100"
              onPress={() =>
                navigation.navigate("RoutineDetails", { routineId: routine.id })
              }
            >
              <View className="flex-1">
                <Text className="font-semibold">{routine.name}</Text>
                <Text className="text-gray-600 text-sm">
                  {routine.duration} • {routine.difficulty}
                </Text>
              </View>
              <View className="items-end">
                <Text
                  className={`text-sm ${
                    routine.isCompleted ? "text-secondary" : "text-gray-500"
                  }`}
                >
                  {routine.isCompleted ? "Completed" : "Pending"}
                </Text>
                {routine.lastCompleted && (
                  <Text className="text-gray-500 text-xs">
                    Last: {routine.lastCompleted}
                  </Text>
                )}
              </View>
            </TouchableOpacity>
          ))}
        </View>

        {/* Upcoming Routines */}
        <View className="bg-white rounded-lg shadow-sm p-4">
          <Text className="text-lg font-semibold mb-4">Upcoming Routines</Text>
          {mockData.upcomingRoutines.map((routine) => (
            <TouchableOpacity
              key={routine.id}
              className="flex-row items-center justify-between py-3 border-b border-gray-100"
              onPress={() =>
                navigation.navigate("RoutineDetails", { routineId: routine.id })
              }
            >
              <View className="flex-1">
                <Text className="font-semibold">{routine.name}</Text>
                <Text className="text-gray-600 text-sm">
                  {routine.duration} • {routine.difficulty}
                </Text>
              </View>
              <View className="items-end">
                <Text className="text-primary text-sm">Scheduled</Text>
                <Text className="text-gray-500 text-xs">
                  {routine.scheduledFor}
                </Text>
              </View>
            </TouchableOpacity>
          ))}
        </View>
      </View>
    </ScrollView>
  );
}
