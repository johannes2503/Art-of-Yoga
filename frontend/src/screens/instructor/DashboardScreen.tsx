import React from "react";
import { View, Text, ScrollView, TouchableOpacity } from "react-native";
import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { InstructorStackParamList } from "../../types/navigation";

type Props = NativeStackScreenProps<InstructorStackParamList, "Dashboard">;

// Temporary mock data - will be replaced with API calls
const mockData = {
  totalClients: 12,
  activeRoutines: 8,
  recentActivity: [
    {
      id: 1,
      clientName: "John Doe",
      routineName: "Morning Flow",
      completed: true,
      date: "2024-03-20",
    },
    {
      id: 2,
      clientName: "Jane Smith",
      routineName: "Evening Stretch",
      completed: false,
      date: "2024-03-19",
    },
    {
      id: 3,
      clientName: "Mike Johnson",
      routineName: "Breathing Practice",
      completed: true,
      date: "2024-03-18",
    },
  ],
};

export default function DashboardScreen({ navigation }: Props) {
  return (
    <ScrollView className="flex-1 bg-background">
      <View className="p-4">
        {/* Stats Overview */}
        <View className="flex-row space-x-4 mb-6">
          <View className="flex-1 bg-white p-4 rounded-lg shadow-sm">
            <Text className="text-2xl font-bold text-primary mb-1">
              {mockData.totalClients}
            </Text>
            <Text className="text-gray-600">Total Clients</Text>
          </View>
          <View className="flex-1 bg-white p-4 rounded-lg shadow-sm">
            <Text className="text-2xl font-bold text-primary mb-1">
              {mockData.activeRoutines}
            </Text>
            <Text className="text-gray-600">Active Routines</Text>
          </View>
        </View>

        {/* Quick Actions */}
        <View className="flex-row space-x-4 mb-6">
          <TouchableOpacity
            className="flex-1 bg-primary p-4 rounded-lg"
            onPress={() => navigation.navigate("CreateRoutine")}
          >
            <Text className="text-white text-center font-semibold">
              Create Routine
            </Text>
          </TouchableOpacity>
          <TouchableOpacity
            className="flex-1 bg-secondary p-4 rounded-lg"
            onPress={() => navigation.navigate("ClientList")}
          >
            <Text className="text-white text-center font-semibold">
              View Clients
            </Text>
          </TouchableOpacity>
        </View>

        {/* Recent Activity */}
        <View className="bg-white rounded-lg shadow-sm p-4">
          <Text className="text-lg font-semibold mb-4">Recent Activity</Text>
          {mockData.recentActivity.map((activity) => (
            <View
              key={activity.id}
              className="flex-row items-center justify-between py-3 border-b border-gray-100"
            >
              <View className="flex-1">
                <Text className="font-semibold">{activity.clientName}</Text>
                <Text className="text-gray-600 text-sm">
                  {activity.routineName}
                </Text>
              </View>
              <View className="items-end">
                <Text
                  className={`text-sm ${
                    activity.completed ? "text-secondary" : "text-gray-500"
                  }`}
                >
                  {activity.completed ? "Completed" : "Pending"}
                </Text>
                <Text className="text-gray-500 text-xs">{activity.date}</Text>
              </View>
            </View>
          ))}
        </View>
      </View>
    </ScrollView>
  );
}
