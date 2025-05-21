import React, { useState } from "react";
import { View, Text, TextInput, TouchableOpacity } from "react-native";
import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { AuthStackParamList } from "../../types/navigation";

type Props = NativeStackScreenProps<AuthStackParamList, "ForgotPassword">;

export default function ForgotPasswordScreen({ navigation }: Props) {
  const [email, setEmail] = useState("");
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleSubmit = async () => {
    // TODO: Implement password reset logic with Supabase
    console.log("Password reset requested for:", email);
    setIsSubmitted(true);
  };

  if (isSubmitted) {
    return (
      <View className="flex-1 bg-background p-4 justify-center">
        <View className="bg-white p-6 rounded-lg shadow-sm">
          <Text className="text-xl font-semibold text-center mb-4 text-primary">
            Check Your Email
          </Text>
          <Text className="text-gray-600 text-center mb-6">
            We've sent password reset instructions to {email}
          </Text>
          <TouchableOpacity
            className="bg-primary p-4 rounded-lg"
            onPress={() => navigation.navigate("Login")}
          >
            <Text className="text-white text-center font-semibold">
              Return to Login
            </Text>
          </TouchableOpacity>
        </View>
      </View>
    );
  }

  return (
    <View className="flex-1 bg-background p-4">
      <View className="flex-1 justify-center">
        <Text className="text-3xl font-bold text-center mb-8 text-primary">
          Reset Password
        </Text>

        <View className="space-y-4">
          <Text className="text-gray-600 text-center mb-4">
            Enter your email address and we'll send you instructions to reset
            your password.
          </Text>

          <TextInput
            className="bg-white p-4 rounded-lg border border-gray-200"
            placeholder="Email"
            value={email}
            onChangeText={setEmail}
            autoCapitalize="none"
            keyboardType="email-address"
          />

          <TouchableOpacity
            className="bg-primary p-4 rounded-lg"
            onPress={handleSubmit}
          >
            <Text className="text-white text-center font-semibold">
              Send Reset Instructions
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            onPress={() => navigation.navigate("Login")}
            className="mt-2"
          >
            <Text className="text-primary text-center">Back to Login</Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
}
