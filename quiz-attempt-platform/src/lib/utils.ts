import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

//  for console.log in dev mode used throughout the app
export function devLog(...message: unknown[]) {
  if (process.env.NODE_ENV !== 'production') {
    console.log(...message);
  }
}
