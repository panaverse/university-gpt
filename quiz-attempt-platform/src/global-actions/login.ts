"use server";

import * as z from "zod";
import { cookies } from "next/headers";
import { LoginSchema } from "@/schemas";

export const login = async (
  values: z.infer<typeof LoginSchema>,
) => {
  const validatedFields = LoginSchema.safeParse(values);

  if (!validatedFields.success) {
    return { error: "Invalid fields!" };
  }

  const { email, password } = validatedFields.data;

  try {
    const request_form_data = new FormData();
    request_form_data.append("username", email);
    request_form_data.append("password", password);

    const user = await fetch(`${process.env.BACKEND_AUTH_SERVER_URL}/api/v1/login/access-token`, {
      method: "POST",
      body: request_form_data,
      cache: "no-store",
    });

    if (!user || user.status !== 200) {
      throw new Error(user.statusText);
    };

    const user_data = await user.json();

    // Include the token expiration time in seconds and milliseconds
    const expiresInSeconds = user_data.expires_in; // Replace with the actual key in your response
    const expiresInMilliseconds = expiresInSeconds * 1000;

    const updated_user_data: UserTokenData = {
      ...user_data,
      accessTokenExpires: Date.now() + expiresInMilliseconds,
    };

    console.log("Login Request Response To Set in Cookies");
  
    cookies().set({
      name: "user_data",
      value: JSON.stringify(updated_user_data), // Convert object to a string
      httpOnly: true,
    });

    // Make Request to get UserData and Store in Cookies
    const user_info = await fetch(`${process.env.BACKEND_AUTH_SERVER_URL}/api/v1/users/me`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${updated_user_data.access_token}`,
      },
    });

    if (!user_info || user_info.status !== 200) {
      throw new Error(user_info.statusText);
    };

    const user_info_data = await user_info.json();

    console.log("User Info Request Response To Set in Cookies");

    cookies().set({
      name: "user_info",
      value: JSON.stringify(user_info_data), // Convert object to a string
      httpOnly: true,
    });

    return { success: "Authenticated!", message: `Welcome Back` };
  } catch (error) {
    if (error instanceof Error) {
          return { error: "Invalid credentials!", message: error.message };
      }
      return { error: "Invalid credentials!", message: "Invalid credentials!" };
    }
  }

