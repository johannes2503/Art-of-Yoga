/// <reference types="nativewind/types" />

declare module "nativewind" {
  import type { ComponentType } from "react";
  import type {
    ViewProps,
    TextProps,
    ImageProps,
    TextInputProps,
  } from "react-native";

  export function styled<T extends ComponentType<any>>(Component: T): T;

  // Add className prop to React Native components
  declare module "react-native" {
    interface ViewProps {
      className?: string;
    }
    interface TextProps {
      className?: string;
    }
    interface ImageProps {
      className?: string;
    }
    interface TextInputProps {
      className?: string;
    }
    interface TouchableOpacityProps {
      className?: string;
    }
  }
}
