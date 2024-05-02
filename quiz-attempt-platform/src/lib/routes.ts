/**
 * An array of routes that are accessible to the public
 * These routes do not require authentication
 * @type {string[]}
 */
export const publicRoutes = [
    "/",
    "/reset"
  ];
  
  /**
   * An array of routes that are used for authentication
   * These routes will redirect logged in users to /dashboard
   * @type {string[]}
   */
  export const authRoutes = [
    "/login",
    "/register",
    "/reset-password"
  ];
  
  /**
   * The prefix for API authentication routes
   * Routes that start with this prefix are used for API authentication purposes
   * @type {string}
   */
  export const apiAuthPrefix = "/api";
  
  /**
   * The default redirect path after logging in
   * @type {string}
   */
  export const DEFAULT_LOGIN_REDIRECT = "/dashboard";

  /**
   * default redirect after sending password reset email
   */
  export const DEFAULT_RESET_REDIRECT = "/login";
  export const DEFAULT_QUIZ_ATTEMPT_REDIRECT = "/dashboard/quiz-attempt";