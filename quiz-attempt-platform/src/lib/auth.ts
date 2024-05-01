"use server";
import { cookies } from "next/headers";

export async function auth() {
  // Check if cookies exist
  const isCookies = cookies().has("user_data");

  if (!isCookies) {
    console.log("[auth] No cookies. Redirecting to login.");
    return null;
  }

  const cookies_user_data = cookies().get("user_data")?.value;

  if (!cookies_user_data) {
    console.log("[auth] No user data in cookies. Redirecting to login.");
    return null;
  }

  let user_data: UserTokenData = JSON.parse(cookies_user_data);
  console.log("[auth] user_data CALLED @auth");

  if (!user_data.access_token) {
    console.log("[auth] Expired Redirecting to login.");
    return null;
  }

  return user_data;
}

export async function auth_user_info() {
  // Check if cookies exist
  const isCookies = cookies().has("user_info");

  if (!isCookies) {
    console.log("[auth_user_info] No cookies. Redirecting to login.");
    return null;
  }

  const cookies_user_data = cookies().get("user_info")?.value;

  if (!cookies_user_data) {
    console.log("[auth_user_info] No user data in cookies. Redirecting to login.");
    return null;
  }

  let user_data: UserInfo = JSON.parse(cookies_user_data);
  console.log("[auth_user_info] user_data CALLED @auth_user_info");

  if (!user_data.is_active) {
    console.log("[auth_user_info] InActive User Redirecting to login.");
    return null;
  }

  return user_data;
}

export async function signOut() {
  cookies().delete("user_data");
  console.log("[signOut] User data cookie deleted. Redirecting to login.");
}
