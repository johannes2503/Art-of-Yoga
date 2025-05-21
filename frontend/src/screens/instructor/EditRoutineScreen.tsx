import React, { useState, useEffect } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ScrollView,
  Switch,
  Alert,
} from "react-native";
import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { InstructorStackParamList } from "../../types/navigation";

type Props = NativeStackScreenProps<InstructorStackParamList, "EditRoutine">;

// Temporary mock data - will be replaced with API data
const mockRoutine = {
  id: "1",
  name: "Morning Flow",
  description: "A gentle morning routine to start your day",
  duration: "30",
  difficulty: "beginner",
  assignedClients: ["1", "3"],
  isTemplate: false,
};

const mockClients = [
  { id: "1", name: "John Doe" },
  { id: "2", name: "Jane Smith" },
  { id: "3", name: "Mike Johnson" },
];

export default function EditRoutineScreen({ route, navigation }: Props) {
  const { routineId } = route.params;
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [duration, setDuration] = useState("");
  const [difficulty, setDifficulty] = useState("beginner");
  const [selectedClients, setSelectedClients] = useState<string[]>([]);
  const [isTemplate, setIsTemplate] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // TODO: Replace with actual API call
    // Simulating API call with mock data
    setTimeout(() => {
      setName(mockRoutine.name);
      setDescription(mockRoutine.description);
      setDuration(mockRoutine.duration);
      setDifficulty(mockRoutine.difficulty);
      setSelectedClients(mockRoutine.assignedClients);
      setIsTemplate(mockRoutine.isTemplate);
      setIsLoading(false);
    }, 500);
  }, [routineId]);

  const handleUpdateRoutine = async () => {
    // TODO: Implement routine update logic with API
    console.log("Updating routine:", {
      id: routineId,
      name,
      description,
      duration,
      difficulty,
      selectedClients,
      isTemplate,
    });
    navigation.goBack();
  };

  const handleDeleteRoutine = () => {
    Alert.alert(
      "Delete Routine",
      "Are you sure you want to delete this routine? This action cannot be undone.",
      [
        {
          text: "Cancel",
          style: "cancel",
        },
        {
          text: "Delete",
          style: "destructive",
          onPress: async () => {
            // TODO: Implement routine deletion logic with API
            console.log("Deleting routine:", routineId);
            navigation.goBack();
          },
        },
      ]
    );
  };

  const toggleClient = (clientId: string) => {
    setSelectedClients((prev) =>
      prev.includes(clientId)
        ? prev.filter((id) => id !== clientId)
        : [...prev, clientId]
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
        {/* Basic Information */}
        <View className="bg-white p-4 rounded-lg shadow-sm">
          <Text className="text-lg font-semibold mb-4">Basic Information</Text>

          <TextInput
            className="bg-gray-50 p-4 rounded-lg border border-gray-200 mb-4"
            placeholder="Routine Name"
            value={name}
            onChangeText={setName}
          />

          <TextInput
            className="bg-gray-50 p-4 rounded-lg border border-gray-200 mb-4"
            placeholder="Description"
            value={description}
            onChangeText={setDescription}
            multiline
            numberOfLines={3}
          />

          <TextInput
            className="bg-gray-50 p-4 rounded-lg border border-gray-200 mb-4"
            placeholder="Duration (minutes)"
            value={duration}
            onChangeText={setDuration}
            keyboardType="numeric"
          />

          <View className="flex-row space-x-4 mb-4">
            {["beginner", "intermediate", "advanced"].map((level) => (
              <TouchableOpacity
                key={level}
                className={`flex-1 p-3 rounded-lg border ${
                  difficulty === level
                    ? "bg-primary border-primary"
                    : "bg-white border-gray-200"
                }`}
                onPress={() => setDifficulty(level)}
              >
                <Text
                  className={`text-center capitalize ${
                    difficulty === level ? "text-white" : "text-gray-600"
                  }`}
                >
                  {level}
                </Text>
              </TouchableOpacity>
            ))}
          </View>

          <View className="flex-row items-center justify-between">
            <Text className="text-gray-600">Save as Template</Text>
            <Switch
              value={isTemplate}
              onValueChange={setIsTemplate}
              trackColor={{ false: "#D1D5DB", true: "#4F46E5" }}
            />
          </View>
        </View>

        {/* Client Assignment */}
        <View className="bg-white p-4 rounded-lg shadow-sm">
          <Text className="text-lg font-semibold mb-4">Assign to Clients</Text>
          {mockClients.map((client) => (
            <TouchableOpacity
              key={client.id}
              className={`p-4 rounded-lg border mb-2 ${
                selectedClients.includes(client.id)
                  ? "bg-primary border-primary"
                  : "bg-white border-gray-200"
              }`}
              onPress={() => toggleClient(client.id)}
            >
              <Text
                className={`text-center ${
                  selectedClients.includes(client.id)
                    ? "text-white"
                    : "text-gray-600"
                }`}
              >
                {client.name}
              </Text>
            </TouchableOpacity>
          ))}
        </View>

        {/* Action Buttons */}
        <View className="space-y-4">
          <TouchableOpacity
            className="bg-primary p-4 rounded-lg"
            onPress={handleUpdateRoutine}
          >
            <Text className="text-white text-center font-semibold">
              Update Routine
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            className="bg-red-500 p-4 rounded-lg"
            onPress={handleDeleteRoutine}
          >
            <Text className="text-white text-center font-semibold">
              Delete Routine
            </Text>
          </TouchableOpacity>
        </View>
      </View>
    </ScrollView>
  );
}
