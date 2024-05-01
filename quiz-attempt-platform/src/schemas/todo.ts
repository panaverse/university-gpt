import * as z from "zod";


export const TodoSchema = z.object({
    title: z.string(),
    description: z.string(),
    completed: z.boolean(),
  });
  