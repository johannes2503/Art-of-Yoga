import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
} from "react-native";
import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { AuthStackParamList } from "../../types/navigation";

type Props = NativeStackScreenProps<AuthStackParamList, "Login">;

export default function LoginScreen({ navigation }: Props) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    // TODO: Implement login logic with Supabase
    console.log("Login attempt with:", { email, password });
  };

  return (
    <View className="flex-1 bg-background p-4">
      <View className="flex-1 justify-center">
        <Text className="text-3xl font-bold text-center mb-8 text-primary">
          Welcome Back
        </Text>

        <View className="space-y-4">
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

          <TouchableOpacity
            className="bg-primary p-4 rounded-lg"
            onPress={handleLogin}
          >
            <Text className="text-white text-center font-semibold">Log In</Text>
          </TouchableOpacity>

          <TouchableOpacity
            onPress={() => navigation.navigate("ForgotPassword")}
            className="mt-2"
          >
            <Text className="text-primary text-center">Forgot Password?</Text>
          </TouchableOpacity>
        </View>

        <View className="flex-row justify-center mt-8">
          <Text className="text-gray-600">Don't have an account? </Text>
          <TouchableOpacity onPress={() => navigation.navigate("Register")}>
            <Text className="text-primary font-semibold">Sign Up</Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
}
