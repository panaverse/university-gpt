"use server";
import * as z from "zod";
import { StartQuizSchema } from "@/schemas/quiz";
import { auth } from "@/lib/auth";
import { redirect } from "next/navigation";

export const startQuizAction = async (values: z.infer<typeof StartQuizSchema>) => {
    const validatedFields = StartQuizSchema.safeParse(values);

    const session = await auth(); 
    if (!session) {
        console.log("[session] No cookies. Redirecting...");
        redirect('/auth/login')
    }
    const accessToken = session.access_token   

  if (!validatedFields.success) {
    return { error: "Invalid fields!" };
  }

  const { quizKey, quizId } = validatedFields.data;

  // Send Data in JSON Format
  const get_quiz_attempt = await fetch(`${process.env.QUIZ_ATTEMPT_ASSESMENT_URL}/api/v1/answersheet/attempt`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    Authorization: `Bearer ${accessToken}`,
    },
    body: JSON.stringify({
        "quiz_key": quizKey,
        "quiz_id": quizId,
      }),
    cache: "no-store",
  });

  console.log('get_quiz_attempt', get_quiz_attempt.status, get_quiz_attempt.statusText);

  if (get_quiz_attempt.status !== 200) {
    if (get_quiz_attempt.status === 422) {
        const error = await get_quiz_attempt.json();
        console.log('error', error);
        const parsed_error = error.detail[0].type + " " + error.detail[0].msg;
        console.log('parsed_error', parsed_error);
        return { error: parsed_error };
    }
    const error = await get_quiz_attempt.json();
    console.log('error', error);
    return { error: error.detail };
  }
  console.log('get_quiz_attempt', get_quiz_attempt.status, get_quiz_attempt.statusText);

  const quizData = await get_quiz_attempt.json();

  return { success: "Best of Luck for your Quiz!", data: quizData };
};
