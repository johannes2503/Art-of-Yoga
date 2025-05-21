import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ScrollView,
} from "react-native";
import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { AuthStackParamList } from "../../types/navigation";
import { UserRole } from "../../types/auth";

type Props = NativeStackScreenProps<AuthStackParamList, "Register">;

export default function RegisterScreen({ navigation }: Props) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [role, setRole] = useState<UserRole>("client");

  const handleRegister = async () => {
    // TODO: Implement registration logic with Supabase
    console.log("Register attempt with:", {
      email,
      password,
      firstName,
      lastName,
      role,
    });
  };

  return (
    <ScrollView className="flex-1 bg-background">
      <View className="p-4">
        <Text className="text-3xl font-bold text-center mb-8 text-primary">
          Create Account
        </Text>

        <View className="space-y-4">
          <View className="flex-row space-x-2">
            <TextInput
              className="flex-1 bg-white p-4 rounded-lg border border-gray-200"
              placeholder="First Name"
              value={firstName}
              onChangeText={setFirstName}
            />
            <TextInput
              className="flex-1 bg-white p-4 rounded-lg border border-gray-200"
              placeholder="Last Name"
              value={lastName}
              onChangeText={setLastName}
            />
          </View>

          <TextInput
            className="bg-white p-4 rounded-lg border border-gray-200"
            placeholder="Email"
            value={email}
            onChangeText={setEmail}
            autoCapitalize="none"
            keyboardType="email-address"
          />

          <TextInput
            className="bg-white p-4 rounded-lg border border-gray-200"
            placeholder="Password"
            value={password}
            onChangeText={setPassword}
            secureTextEntry
          />

          <TextInput
            className="bg-white p-4 rounded-lg border border-gray-200"
            placeholder="Confirm Password"
            value={confirmPassword}
            onChangeText={setConfirmPassword}
            secureTextEntry
          />

          <View className="flex-row space-x-4">
            <TouchableOpacity
              className={`flex-1 p-4 rounded-lg border ${
                role === "client"
                  ? "bg-primary border-primary"
                  : "bg-white border-gray-200"
              }`}
              onPress={() => setRole("client")}
            >
              <Text
                className={`text-center font-semibold ${
                  role === "client" ? "text-white" : "text-gray-600"
                }`}
              >
                Client
              </Text>
            </TouchableOpacity>

            <TouchableOpacity
              className={`flex-1 p-4 rounded-lg border ${
                role === "instructor"
                  ? "bg-primary border-primary"
                  : "bg-white border-gray-200"
              }`}
              onPress={() => setRole("instructor")}
            >
              <Text
                className={`text-center font-semibold ${
                  role === "instructor" ? "text-white" : "text-gray-600"
                }`}
              >
                Instructor
              </Text>
            </TouchableOpacity>
          </View>

          <TouchableOpacity
            className="bg-primary p-4 rounded-lg mt-4"
            onPress={handleRegister}
          >
            <Text className="text-white text-center font-semibold">
              Create Account
            </Text>
          </TouchableOpacity>
        </View>

        <View className="flex-row justify-center mt-8">
          <Text className="text-gray-600">Already have an account? </Text>
          <TouchableOpacity onPress={() => navigation.navigate("Login")}>
            <Text className="text-primary font-semibold">Log In</Text>
          </TouchableOpacity>
        </View>
      </View>
    </ScrollView>
  );
}
