import { NavigatorScreenParams } from "@react-navigation/native";

export type AuthStackParamList = {
  Login: undefined;
  Register: undefined;
  ForgotPassword: undefined;
  EmailVerification: { email: string };
};

export type InstructorStackParamList = {
  Dashboard: undefined;
  CreateRoutine: undefined;
  EditRoutine: { routineId: string };
  ClientList: undefined;
  ClientDetails: { clientId: string };
  Profile: undefined;
};

export type ClientStackParamList = {
  Dashboard: undefined;
  RoutineDetails: { routineId: string };
  Profile: undefined;
  Progress: undefined;
};

export type RootStackParamList = {
  Auth: NavigatorScreenParams<AuthStackParamList>;
  Instructor: NavigatorScreenParams<InstructorStackParamList>;
  Client: NavigatorScreenParams<ClientStackParamList>;
};
