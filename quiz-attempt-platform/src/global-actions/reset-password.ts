"use server";
import * as z from "zod";
import { ResetSchema } from "@/schemas";

export const reset = async (values: z.infer<typeof ResetSchema>) => {
  const validatedFields = ResetSchema.safeParse(values);

  if (!validatedFields.success) {
    return { error: "Invalid fields!" };
  }

  const { email } = validatedFields.data;

  // Send Data in JSON Format
  const reset_pass_request = await fetch(`${process.env.BACKEND_AUTH_SERVER_URL}/api/v1/password-recovery/${email}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    cache: "no-store",
  });

  console.log('reset_pass_request', reset_pass_request.status, reset_pass_request.statusText);

  if (reset_pass_request.status !== 200) {
    const error = await reset_pass_request.json();
    return { error: error.detail };
  }

  return { success: "Password recovery email sent" };
};
