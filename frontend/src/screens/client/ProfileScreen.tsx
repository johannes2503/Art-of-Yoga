import React, { useState, useEffect } from "react";
import {
  View,
  Text,
  ScrollView,
  TextInput,
  TouchableOpacity,
  Alert,
  Switch,
} from "react-native";
import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { ClientStackParamList } from "../../types/navigation";

type Props = NativeStackScreenProps<ClientStackParamList, "Profile">;

// Temporary mock data - will be replaced with API data
const mockProfile = {
  id: "1",
  firstName: "John",
  lastName: "Doe",
  email: "john.doe@example.com",
  phone: "+1 (555) 123-4567",
  preferences: {
    notifications: true,
    emailUpdates: true,
    darkMode: false,
  },
  instructors: [
    {
      id: "1",
      name: "Sarah Johnson",
      email: "sarah.johnson@example.com",
    },
  ],
  joinDate: "2024-01-15",
};

export default function ProfileScreen({ navigation }: Props) {
  const [profile, setProfile] = useState(mockProfile);
  const [isEditing, setIsEditing] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [editedProfile, setEditedProfile] = useState(mockProfile);

  useEffect(() => {
    // TODO: Replace with actual API call
    // Simulating API call with mock data
    setTimeout(() => {
      setProfile(mockProfile);
      setEditedProfile(mockProfile);
      setIsLoading(false);
    }, 500);
  }, []);

  const handleSaveProfile = async () => {
    // TODO: Implement profile update logic with API
    console.log("Updating profile:", editedProfile);
    setProfile(editedProfile);
    setIsEditing(false);
    Alert.alert("Success", "Profile updated successfully");
  };

  const handleLogout = () => {
    Alert.alert("Logout", "Are you sure you want to logout?", [
      {
        text: "Cancel",
        style: "cancel",
      },
      {
        text: "Logout",
        style: "destructive",
        onPress: async () => {
          // TODO: Implement logout logic
          console.log("Logging out...");
        },
      },
    ]);
  };

  if (isLoading) {
    return (
      <View className="flex-1 bg-background justify-center items-center">
        <Text className="text-gray-600">Loading profile...</Text>
      </View>
    );
  }

  return (
    <ScrollView className="flex-1 bg-background">
      <View className="p-4 space-y-4">
        {/* Profile Header */}
        <View className="bg-white p-4 rounded-lg shadow-sm">
          <View className="flex-row justify-between items-center mb-4">
            <Text className="text-2xl font-bold text-primary">My Profile</Text>
            <TouchableOpacity
              onPress={() => setIsEditing(!isEditing)}
              className="bg-primary px-4 py-2 rounded-lg"
            >
              <Text className="text-white font-semibold">
                {isEditing ? "Cancel" : "Edit"}
              </Text>
            </TouchableOpacity>
          </View>

          {/* Personal Information */}
          <View className="space-y-4">
            <View className="flex-row space-x-4">
              <View className="flex-1">
                <Text className="text-gray-600 text-sm mb-1">First Name</Text>
                {isEditing ? (
                  <TextInput
                    className="bg-gray-50 p-3 rounded-lg border border-gray-200"
                    value={editedProfile.firstName}
                    onChangeText={(text) =>
                      setEditedProfile((prev) => ({ ...prev, firstName: text }))
                    }
                  />
                ) : (
                  <Text className="font-semibold">{profile.firstName}</Text>
                )}
              </View>
              <View className="flex-1">
                <Text className="text-gray-600 text-sm mb-1">Last Name</Text>
                {isEditing ? (
                  <TextInput
                    className="bg-gray-50 p-3 rounded-lg border border-gray-200"
                    value={editedProfile.lastName}
                    onChangeText={(text) =>
                      setEditedProfile((prev) => ({ ...prev, lastName: text }))
                    }
                  />
                ) : (
                  <Text className="font-semibold">{profile.lastName}</Text>
                )}
              </View>
            </View>

            <View>
              <Text className="text-gray-600 text-sm mb-1">Email</Text>
              {isEditing ? (
                <TextInput
                  className="bg-gray-50 p-3 rounded-lg border border-gray-200"
                  value={editedProfile.email}
                  onChangeText={(text) =>
                    setEditedProfile((prev) => ({ ...prev, email: text }))
                  }
                  keyboardType="email-address"
                  autoCapitalize="none"
                />
              ) : (
                <Text className="font-semibold">{profile.email}</Text>
              )}
            </View>

            <View>
              <Text className="text-gray-600 text-sm mb-1">Phone</Text>
              {isEditing ? (
                <TextInput
                  className="bg-gray-50 p-3 rounded-lg border border-gray-200"
                  value={editedProfile.phone}
                  onChangeText={(text) =>
                    setEditedProfile((prev) => ({ ...prev, phone: text }))
                  }
                  keyboardType="phone-pad"
                />
              ) : (
                <Text className="font-semibold">{profile.phone}</Text>
              )}
            </View>
          </View>
        </View>

        {/* Preferences */}
        <View className="bg-white p-4 rounded-lg shadow-sm">
          <Text className="text-lg font-semibold mb-4">Preferences</Text>
          <View className="space-y-4">
            <View className="flex-row items-center justify-between">
              <Text className="text-gray-600">Push Notifications</Text>
              <Switch
                value={editedProfile.preferences.notifications}
                onValueChange={(value) =>
                  setEditedProfile((prev) => ({
                    ...prev,
                    preferences: { ...prev.preferences, notifications: value },
                  }))
                }
                disabled={!isEditing}
                trackColor={{ false: "#D1D5DB", true: "#4F46E5" }}
              />
            </View>
            <View className="flex-row items-center justify-between">
              <Text className="text-gray-600">Email Updates</Text>
              <Switch
                value={editedProfile.preferences.emailUpdates}
                onValueChange={(value) =>
                  setEditedProfile((prev) => ({
                    ...prev,
                    preferences: { ...prev.preferences, emailUpdates: value },
                  }))
                }
                disabled={!isEditing}
                trackColor={{ false: "#D1D5DB", true: "#4F46E5" }}
              />
            </View>
            <View className="flex-row items-center justify-between">
              <Text className="text-gray-600">Dark Mode</Text>
              <Switch
                value={editedProfile.preferences.darkMode}
                onValueChange={(value) =>
                  setEditedProfile((prev) => ({
                    ...prev,
                    preferences: { ...prev.preferences, darkMode: value },
                  }))
                }
                disabled={!isEditing}
                trackColor={{ false: "#D1D5DB", true: "#4F46E5" }}
              />
            </View>
          </View>
        </View>

        {/* Instructors */}
        <View className="bg-white p-4 rounded-lg shadow-sm">
          <Text className="text-lg font-semibold mb-4">My Instructors</Text>
          {profile.instructors.map((instructor) => (
            <View
              key={instructor.id}
              className="flex-row items-center justify-between py-3 border-b border-gray-100 last:border-0"
            >
              <View>
                <Text className="font-semibold">{instructor.name}</Text>
                <Text className="text-gray-600 text-sm">
                  {instructor.email}
                </Text>
              </View>
              <TouchableOpacity
                className="bg-gray-100 px-3 py-1 rounded-lg"
                onPress={() => {
                  // TODO: Implement instructor contact/message feature
                  console.log("Contact instructor:", instructor.id);
                }}
              >
                <Text className="text-primary text-sm">Contact</Text>
              </TouchableOpacity>
            </View>
          ))}
        </View>

        {/* Action Buttons */}
        <View className="space-y-4">
          {isEditing ? (
            <TouchableOpacity
              className="bg-primary p-4 rounded-lg"
              onPress={handleSaveProfile}
            >
              <Text className="text-white text-center font-semibold">
                Save Changes
              </Text>
            </TouchableOpacity>
          ) : null}

          <TouchableOpacity
            className="bg-red-500 p-4 rounded-lg"
            onPress={handleLogout}
          >
            <Text className="text-white text-center font-semibold">Logout</Text>
          </TouchableOpacity>
        </View>
      </View>
    </ScrollView>
  );
}
