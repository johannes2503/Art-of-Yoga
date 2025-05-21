import React from "react";
import { View, Text, TouchableOpacity } from "react-native";
import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { AuthStackParamList } from "../../types/navigation";

type Props = NativeStackScreenProps<AuthStackParamList, "EmailVerification">;

export default function EmailVerificationScreen({ route, navigation }: Props) {
  const { email } = route.params;

  const handleResendVerification = async () => {
    // TODO: Implement resend verification email logic with Supabase
    console.log("Resend verification email to:", email);
  };

  return (
    <View className="flex-1 bg-background p-4">
      <View className="flex-1 justify-center">
        <View className="bg-white p-6 rounded-lg shadow-sm">
          <Text className="text-2xl font-bold text-center mb-4 text-primary">
            Verify Your Email
          </Text>

          <Text className="text-gray-600 text-center mb-6">
            We've sent a verification email to:
          </Text>
          <Text className="text-primary font-semibold text-center mb-6">
            {email}
          </Text>

          <Text className="text-gray-600 text-center mb-8">
            Please check your email and click the verification link to continue.
            If you don't see the email, check your spam folder.
          </Text>

          <TouchableOpacity
            className="bg-primary p-4 rounded-lg mb-4"
            onPress={handleResendVerification}
          >
            <Text className="text-white text-center font-semibold">
              Resend Verification Email
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            onPress={() => navigation.navigate("Login")}
            className="mt-2"
          >
            <Text className="text-primary text-center">Return to Login</Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
}
