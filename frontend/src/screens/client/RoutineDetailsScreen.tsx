import React, { useState, useEffect } from "react";
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  Image,
  Alert,
} from "react-native";
import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { ClientStackParamList } from "../../types/navigation";

type Props = NativeStackScreenProps<ClientStackParamList, "RoutineDetails">;

// Temporary mock data - will be replaced with API data
const mockRoutine = {
  id: "1",
  name: "Morning Flow",
  instructor: "Sarah Johnson",
  description:
    "A gentle morning routine to start your day with energy and focus. This sequence combines breathing exercises with basic yoga poses to awaken the body and mind.",
  duration: "30 min",
  difficulty: "beginner",
  exercises: [
    {
      id: "1",
      name: "Deep Breathing",
      type: "breathing",
      duration: "5 min",
      instructions:
        "Find a comfortable seated position. Inhale deeply through the nose for 4 counts, hold for 4 counts, exhale through the mouth for 4 counts.",
      imageUrl: "https://example.com/breathing.jpg",
    },
    {
      id: "2",
      name: "Sun Salutation A",
      type: "yoga",
      duration: "10 min",
      instructions:
        "Begin in mountain pose. Flow through a sequence of poses including forward fold, plank, and upward dog.",
      imageUrl: "https://example.com/sun-salutation.jpg",
    },
    {
      id: "3",
      name: "Guided Meditation",
      type: "meditation",
      duration: "15 min",
      instructions:
        "Lie down in savasana. Follow the guided meditation focusing on breath awareness and body relaxation.",
      imageUrl: "https://example.com/meditation.jpg",
    },
  ],
  lastCompleted: "2024-03-20",
  isCompleted: false,
};

export default function RoutineDetailsScreen({ route, navigation }: Props) {
  const { routineId } = route.params;
  const [routine, setRoutine] = useState(mockRoutine);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // TODO: Replace with actual API call
    // Simulating API call with mock data
    setTimeout(() => {
      setRoutine(mockRoutine);
      setIsLoading(false);
    }, 500);
  }, [routineId]);

  const handleMarkComplete = () => {
    Alert.alert(
      "Complete Routine",
      "Would you like to mark this routine as completed?",
      [
        {
          text: "Cancel",
          style: "cancel",
        },
        {
          text: "Complete",
          onPress: async () => {
            // TODO: Implement routine completion logic with API
            console.log("Marking routine as complete:", routineId);
            setRoutine((prev) => ({ ...prev, isCompleted: true }));
          },
        },
      ]
    );
  };

  if (isLoading) {
    return (
      <View className="flex-1 bg-background justify-center items-center">
        <Text className="text-gray-600">Loading routine...</Text>
      </View>
    );
  }

  return (
    <ScrollView className="flex-1 bg-background">
      <View className="p-4 space-y-4">
        {/* Header Information */}
        <View className="bg-white p-4 rounded-lg shadow-sm">
          <Text className="text-2xl font-bold text-primary mb-2">
            {routine.name}
          </Text>
          <Text className="text-gray-600 mb-4">{routine.description}</Text>

          <View className="flex-row space-x-4 mb-4">
            <View className="flex-1 bg-gray-50 p-3 rounded-lg">
              <Text className="text-gray-600 text-sm">Duration</Text>
              <Text className="font-semibold">{routine.duration}</Text>
            </View>
            <View className="flex-1 bg-gray-50 p-3 rounded-lg">
              <Text className="text-gray-600 text-sm">Difficulty</Text>
              <Text className="font-semibold capitalize">
                {routine.difficulty}
              </Text>
            </View>
          </View>

          <View className="flex-row items-center justify-between">
            <Text className="text-gray-600">
              Instructor: {routine.instructor}
            </Text>
            {routine.lastCompleted && (
              <Text className="text-gray-500 text-sm">
                Last completed: {routine.lastCompleted}
              </Text>
            )}
          </View>
        </View>

        {/* Exercises List */}
        <View className="bg-white rounded-lg shadow-sm p-4">
          <Text className="text-lg font-semibold mb-4">Exercises</Text>
          {routine.exercises.map((exercise, index) => (
            <View
              key={exercise.id}
              className="mb-4 pb-4 border-b border-gray-100 last:border-0 last:mb-0 last:pb-0"
            >
              <View className="flex-row items-start space-x-4">
                <View className="w-16 h-16 bg-gray-100 rounded-lg items-center justify-center">
                  <Text className="text-primary font-bold">{index + 1}</Text>
                </View>
                <View className="flex-1">
                  <View className="flex-row items-center justify-between mb-1">
                    <Text className="font-semibold">{exercise.name}</Text>
                    <Text className="text-gray-500 text-sm">
                      {exercise.duration}
                    </Text>
                  </View>
                  <Text className="text-gray-600 text-sm mb-2">
                    {exercise.instructions}
                  </Text>
                  <View className="flex-row space-x-2">
                    <View className="bg-gray-100 px-2 py-1 rounded">
                      <Text className="text-gray-600 text-xs capitalize">
                        {exercise.type}
                      </Text>
                    </View>
                  </View>
                </View>
              </View>
            </View>
          ))}
        </View>

        {/* Action Button */}
        <TouchableOpacity
          className={`p-4 rounded-lg ${
            routine.isCompleted ? "bg-secondary" : "bg-primary"
          }`}
          onPress={handleMarkComplete}
        >
          <Text className="text-white text-center font-semibold">
            {routine.isCompleted ? "Completed" : "Mark as Complete"}
          </Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}
