"use server";
import * as z from "zod";
import { NewPasswordSchema } from "@/schemas";

export const newPassword = async (values: z.infer<typeof NewPasswordSchema>, resetToken: string) => {
  const validatedFields = NewPasswordSchema.safeParse(values);

  if (!validatedFields.success) {
    return { error: "Invalid fields!" };
  }

  const { new_password } = validatedFields.data;

  // Send Data in JSON Format
  const new_pass_request = await fetch(`${process.env.BACKEND_AUTH_SERVER_URL}/api/v1/reset-password/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
        "new_password": new_password,
        "token": resetToken,
      }),
    cache: "no-store",
  });

  console.log('new_pass_request', new_pass_request.status, new_pass_request.statusText);

  if (new_pass_request.status !== 200) {
    const error = await new_pass_request.json();
    return { error: error.detail };
  }

  return { success: "Password recovery email sent" };
};
