"use server";

import { signOut } from "@/lib/auth";

export const logout = async () => {
    await signOut();
  }
  
