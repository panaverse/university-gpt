interface UserTokenData {
    access_token: string;
    token_type: string;
    expires_in: number;
    refresh_token: string;
    accessTokenExpires: number;
  }

  interface UserInfo {
    email: string;
    is_active: boolean;
    is_superuser: boolean;
    full_name: string | null;
    role: string;
    id: number;
  }