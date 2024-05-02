import { NextRequest, NextResponse } from "next/server";
import {
  DEFAULT_LOGIN_REDIRECT,
  apiAuthPrefix,
  authRoutes,
  publicRoutes,
} from "@/lib/routes";

export default async function middleware(req: NextRequest) {
  console.log("MIDDLEWARE.TS: PATHNAME", req.nextUrl.pathname);
  const { nextUrl } = req;

  // console.log("[nextUrl] @middleware", nextUrl);
  console.log("[nextUrl.pathname] @middleware", nextUrl.pathname);
  

  const { searchParams } = new URL(req.url);

  const redirect_uri = searchParams.get("redirect_uri");
  const response_type = searchParams.get("response_type");
  const client_id = searchParams.get("client_id");
  const scope = searchParams.get("scope");
  const state = searchParams.get("state");

  const isApiAuthRoute = nextUrl.pathname.startsWith(apiAuthPrefix);
  const isPublicRoute = publicRoutes.includes(nextUrl.pathname);
  const isAuthRoute = authRoutes.includes(nextUrl.pathname);

  console.log("[isPublicRoute] @middleware", isPublicRoute);
  console.log("[isAuthRoute] @middleware", isAuthRoute);
  

  if (isApiAuthRoute) {
    return null;
  }

  let cookies_user_data = req.cookies.get("user_data")?.value;
  let isInitialLoggedIn = !!cookies_user_data;

  console.log("[isInitialLoggedIn] BEFORE @middleware", isInitialLoggedIn);

  const response = NextResponse.next();
  if (isInitialLoggedIn) {
    let user_data = JSON.parse(cookies_user_data || "");

    if (user_data.accessTokenExpires < Date.now()) {
      try {
        const formData = new FormData();
        formData.append("refresh_token", user_data.refresh_token);
        formData.append("grant_type", "refresh_token");

        const token_response = await fetch(
          `${process.env.BACKEND_AUTH_SERVER_URL}/api/v1/oauth/token`,
          {
            method: "POST",
            body: formData,
          }
        );

        if (!token_response.ok) {
          throw new Error(
            `Failed to refresh token: ${token_response.status} ${token_response.statusText}`
          );
        }

        const refreshedTokens = await token_response.json();
        console.log(
          "[middleware] Refreshed tokens received: ",
          refreshedTokens
        );

        console.log("[middleware] Token refresh successful");
        console.log("[middleware_OLD] user_data CALLED @middleware", user_data);

        user_data.access_token = refreshedTokens.access_token;
        user_data.refresh_token = refreshedTokens.refresh_token;
        user_data.accessTokenExpires =
          Date.now() + refreshedTokens.expires_in * 1000;
        console.log("[middleware] Updated user_data with new tokens");
        console.log("[middleware_NEW] user_data CALLED @middleware", user_data);

        response.cookies.set({
          name: "user_data",
          value: JSON.stringify(user_data), // Convert object to a string
        });
        return response;
      } catch (error) {
        console.error("[middleware] Error in token refresh process: ", error);
        response.cookies.delete("user_data");
        const loginUrl = new URL("/login", req.url);
        loginUrl.searchParams.set("tokenExpired", "1");
        return response;
      }
    }
  }

  const isLoggedIn = !!req.cookies.get("user_data")?.value;

  console.log("[isLoggedIn] AFTER @middleware", isLoggedIn);

  if (isAuthRoute) {
    if (isLoggedIn) {
      if (redirect_uri && state) {
        const redirctNewUrl =
          DEFAULT_LOGIN_REDIRECT +
          `?redirect_uri=${redirect_uri}` +
          `&state=${state}` +
          `&response_type=${response_type}` +
          `&client_id=${client_id}` +
          `&scope=${scope}`;
        return NextResponse.redirect(new URL(redirctNewUrl, nextUrl));
      } 
      return NextResponse.redirect(new URL(DEFAULT_LOGIN_REDIRECT, nextUrl));
    }
    return null;
  }

  if (!isLoggedIn && !isPublicRoute) {
    let callbackUrl = nextUrl.pathname;
    if (nextUrl.search) {
      callbackUrl += nextUrl.search;
    }

    const encodedCallbackUrl = encodeURIComponent(callbackUrl);

    return NextResponse.redirect(
      new URL(`/login?callbackUrl=${encodedCallbackUrl}`, nextUrl)
    );
  }

  return response;
}

export const config = {
  matcher: ["/((?!.+\\.[\\w]+$|_next).*)", "/"],
};
