import * as z from "zod";

export const StartQuizSchema = z.object({
  quizKey: z.string().min(1, {
    message: "Enter a Valid Quiz Key!",
  }),
  quizId: z.number().positive(),
});
  