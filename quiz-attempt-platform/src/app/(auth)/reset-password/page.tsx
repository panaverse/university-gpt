import { NewPasswordForm } from "@/components/auth/new-password-form";
import { Suspense } from 'react'
import { cookies } from "next/headers";

const NewPasswordPage = ({
    searchParams,
  }: {
    searchParams: { [key: string]: string | string[] | undefined };
  }) => {
    
    const reset_token = searchParams.token;

    if (!reset_token || Array.isArray(reset_token) || reset_token.length === 0){
        console.error("No reset token found");
        return null;
    }

    console.log("Reset token: ", reset_token);


    return <Suspense><NewPasswordForm resetToken={reset_token} /></Suspense>;
};

export default NewPasswordPage;
