import React, { useState, useEffect } from "react";
import { View, Text, ScrollView, TouchableOpacity } from "react-native";
import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { ClientStackParamList } from "../../types/navigation";

type Props = NativeStackScreenProps<ClientStackParamList, "Progress">;

// Temporary mock data - will be replaced with API data
const mockProgress = {
  stats: {
    totalRoutines: 5,
    completedRoutines: 2,
    totalMinutes: 75,
    streakDays: 3,
  },
  achievements: [
    {
      id: "1",
      title: "First Routine",
      description: "Completed your first yoga routine",
      date: "2024-03-15",
      icon: "🎯",
    },
    {
      id: "2",
      title: "3-Day Streak",
      description: "Completed routines for 3 consecutive days",
      date: "2024-03-20",
      icon: "🔥",
    },
  ],
  history: [
    {
      id: "1",
      routineName: "Morning Flow",
      date: "2024-03-20",
      duration: "30 min",
      difficulty: "beginner",
      feedback: {
        rating: 4,
        notes: "Great routine, felt energized after",
      },
    },
    {
      id: "2",
      routineName: "Breathing Practice",
      date: "2024-03-19",
      duration: "15 min",
      difficulty: "beginner",
      feedback: {
        rating: 5,
        notes: "Perfect for morning meditation",
      },
    },
    {
      id: "3",
      routineName: "Evening Stretch",
      date: "2024-03-18",
      duration: "20 min",
      difficulty: "beginner",
      feedback: {
        rating: 4,
        notes: "Helped with relaxation",
      },
    },
  ],
};

export default function ProgressScreen({ navigation }: Props) {
  const [progress, setProgress] = useState(mockProgress);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // TODO: Replace with actual API call
    // Simulating API call with mock data
    setTimeout(() => {
      setProgress(mockProgress);
      setIsLoading(false);
    }, 500);
  }, []);

  if (isLoading) {
    return (
      <View className="flex-1 bg-background justify-center items-center">
        <Text className="text-gray-600">Loading progress...</Text>
      </View>
    );
  }

  return (
    <ScrollView className="flex-1 bg-background">
      <View className="p-4 space-y-4">
        {/* Stats Overview */}
        <View className="flex-row flex-wrap -mx-2">
          <View className="w-1/2 px-2 mb-4">
            <View className="bg-white p-4 rounded-lg shadow-sm">
              <Text className="text-2xl font-bold text-primary mb-1">
                {progress.stats.completedRoutines}/
                {progress.stats.totalRoutines}
              </Text>
              <Text className="text-gray-600">Routines Completed</Text>
            </View>
          </View>
          <View className="w-1/2 px-2 mb-4">
            <View className="bg-white p-4 rounded-lg shadow-sm">
              <Text className="text-2xl font-bold text-primary mb-1">
                {progress.stats.totalMinutes}
              </Text>
              <Text className="text-gray-600">Total Minutes</Text>
            </View>
          </View>
          <View className="w-1/2 px-2">
            <View className="bg-white p-4 rounded-lg shadow-sm">
              <Text className="text-2xl font-bold text-primary mb-1">
                {Math.round(
                  (progress.stats.completedRoutines /
                    progress.stats.totalRoutines) *
                    100
                )}
                %
              </Text>
              <Text className="text-gray-600">Completion Rate</Text>
            </View>
          </View>
          <View className="w-1/2 px-2">
            <View className="bg-white p-4 rounded-lg shadow-sm">
              <Text className="text-2xl font-bold text-primary mb-1">
                {progress.stats.streakDays}
              </Text>
              <Text className="text-gray-600">Day Streak</Text>
            </View>
          </View>
        </View>

        {/* Achievements */}
        <View className="bg-white rounded-lg shadow-sm p-4">
          <Text className="text-lg font-semibold mb-4">Achievements</Text>
          {progress.achievements.map((achievement) => (
            <View
              key={achievement.id}
              className="flex-row items-center space-x-4 py-3 border-b border-gray-100 last:border-0"
            >
              <Text className="text-2xl">{achievement.icon}</Text>
              <View className="flex-1">
                <Text className="font-semibold">{achievement.title}</Text>
                <Text className="text-gray-600 text-sm">
                  {achievement.description}
                </Text>
                <Text className="text-gray-500 text-xs mt-1">
                  {achievement.date}
                </Text>
              </View>
            </View>
          ))}
        </View>

        {/* History */}
        <View className="bg-white rounded-lg shadow-sm p-4">
          <Text className="text-lg font-semibold mb-4">Recent History</Text>
          {progress.history.map((item) => (
            <TouchableOpacity
              key={item.id}
              className="py-3 border-b border-gray-100 last:border-0"
              onPress={() =>
                navigation.navigate("RoutineDetails", { routineId: item.id })
              }
            >
              <View className="flex-row justify-between items-start mb-2">
                <View>
                  <Text className="font-semibold">{item.routineName}</Text>
                  <Text className="text-gray-600 text-sm">
                    {item.duration} • {item.difficulty}
                  </Text>
                </View>
                <View className="flex-row items-center">
                  <Text className="text-yellow-500 mr-1">★</Text>
                  <Text className="font-semibold">
                    {item.feedback.rating}/5
                  </Text>
                </View>
              </View>
              <Text className="text-gray-600 text-sm">
                {item.feedback.notes}
              </Text>
              <Text className="text-gray-500 text-xs mt-1">{item.date}</Text>
            </TouchableOpacity>
          ))}
        </View>
      </View>
    </ScrollView>
  );
}
